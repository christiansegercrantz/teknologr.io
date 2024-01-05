import ldap
import ldap.modlist
from getenv import env

import time

'''All methods here can throw ldap.LDAPError'''

def LDAPError_to_string(e):
    if not isinstance(e, ldap.LDAPError):
        return str(e)
    data = e.args[0]
    s = f"{data.get('desc' , '')} [{data.get('result')}]"
    info = data.get('info')
    if info:
        s += f' ({info})'
    return s

def get_ldap_account(username):
    '''
    Get the info for a certain LDAP account. Does never throw LDAPError.
    '''
    result = {
        'username': username,
        'exists': False,
        'groups': [],
    }
    if not username:
        return result
    try:
        with LDAPAccountManager() as lm:
            exists = lm.check_account(username)
            groups = lm.get_ldap_groups(username)
            result['exists'] = exists
            result['groups'] = groups
    except ldap.LDAPError as e:
        result['error'] = LDAPError_to_string(e)
    return result

class LDAPAccountManager:
    def __init__(self):
        # Don't require certificates
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        # Attempts no connection, simply initializes the object.
        self.ldap = ldap.initialize(env("LDAP_SERVER_URI", "ldaps://localhost:45671"))

    def __enter__(self):
        self.ldap.simple_bind_s(
            env("LDAP_ADMIN_BIND_DN", "admin"),
            env("LDAP_ADMIN_PW", "hunter2")
        )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.ldap.unbind_s()

    def add_account(self, member, username, password):
        # Adds new account for the given member with the given username and password
        dn = env("LDAP_USER_DN_TEMPLATE") % {'user': username}

        uidnumber = self.get_next_uidnumber()
        nt_pw = self.get_samba_password(password)

        # Everything has to be byte string because why the fuck not?
        attrs = {}
        attrs['uid'] = [username.encode('utf-8')]
        attrs['cn'] = [member.common_name.encode('utf-8')]
        homedir = '/rhome/%s' % username
        attrs['homeDirectory'] = [homedir.encode('utf-8')]
        attrs['uidNumber'] = [str(uidnumber).encode('utf-8')]
        attrs['mailHost'] = [b'smtp.ayy.fi']
        attrs['gidNumber'] = [b'1000']
        attrs['sn'] = [member.surname.encode('utf-8')]
        attrs['givenName'] = [member.get_preferred_name().encode('utf-8')]
        attrs['loginShell'] = [b'/bin/bash']
        attrs['objectClass'] = [
            b'kerberosSecurityObject',
            b'inetOrgPerson',
            b'posixAccount',
            b'shadowAccount',
            b'inetLocalMailRecipient',
            b'top',
            b'person',
            b'organizationalPerson',
            b'billAccount',
            b'sambaSamAccount'
        ]
        attrs['krbName'] = [username.encode('utf-8')]
        attrs['mail'] = [member.email.encode('utf-8')]
        attrs['userPassword'] = [self.hash_user_password(password)]
        sambasid = "S-1-0-0-%s" % str(uidnumber*2+1000)
        attrs['sambaSID'] = [sambasid.encode('utf-8')]
        attrs['sambaNTPassword'] = [nt_pw.encode('utf-8')]
        attrs['sambaPwdLastSet'] = [str(int(time.time())).encode('utf-8')]

        # Add the user to LDAP
        ldif = ldap.modlist.addModlist(attrs)
        self.ldap.add_s(dn, ldif)

        # Add user to Members group
        group_dn = env("LDAP_MEMBER_GROUP_DN")
        self.ldap.modify_s(group_dn, [(ldap.MOD_ADD, 'memberUid', username.encode('utf-8'))])

    def get_next_uidnumber(self):
        # Returns the next free uidnumber greater than 1000
        output = self.ldap.search_s(env("LDAP_USER_DN"), ldap.SCOPE_ONELEVEL, attrlist=['uidNumber'])
        uidnumbers = [int(user[1]['uidNumber'][0]) for user in output]
        uidnumbers.sort()

        # Find first free uid over 1000.
        last = 1000
        for uid in uidnumbers:
            if uid > last + 1:
                break
            last = uid
        return last + 1

    def check_account(self, username):
        '''
        Check if a certain LDAP account exists.
        '''
        try:
            dn = env("LDAP_USER_DN_TEMPLATE") % {'user': username}
            self.ldap.search_s(dn, ldap.SCOPE_BASE)
            return True
        except ldap.LDAPError as e:
            # Result code 32 = noSuchObject
            if e.args[0].get('result') == 32:
                return False
            raise e

    def delete_account(self, username):
        # Remove user from members group
        group_dn = env("LDAP_MEMBER_GROUP_DN")
        self.ldap.modify_s(group_dn, [(ldap.MOD_DELETE, 'memberUid', username.encode('utf-8'))])

        # Remove user, if it exists
        if self.check_account(username):
            dn = env("LDAP_USER_DN_TEMPLATE") % {'user': username}
            self.ldap.delete_s(dn)

    def change_password(self, username, password):
        # Changes both the user password and the samba password
        dn = env("LDAP_USER_DN_TEMPLATE") % {'user': username}
        nt_pw = self.get_samba_password(password)
        mod_attrs = [
            (ldap.MOD_REPLACE, 'userPassword', self.hash_user_password(password)),
            (ldap.MOD_REPLACE, 'sambaNTPassword', nt_pw.encode('utf-8'))
        ]
        self.ldap.modify_s(dn, mod_attrs)

    def change_email(self, username, email):
        # Changes the email address for the given user
        dn = env("LDAP_USER_DN_TEMPLATE") % {'user': username}
        mod_attrs = [
            (ldap.MOD_REPLACE, 'mail', email.encode('utf-8')),
        ]
        self.ldap.modify_s(dn, mod_attrs)

    def get_samba_password(self, password):
        # The password needs to be stored in a different format for samba
        import codecs
        import hashlib
        return codecs.encode(
            hashlib.new('md4', password.encode('utf-16le')).digest(), 'hex_codec'
        ).decode('utf-8').upper()

    def hash_user_password(self, password):
        import random
        import string
        import hashlib
        import base64
        import binascii
        salt = "".join([random.choice(string.ascii_uppercase) for i in range(4)])
        digest = hashlib.md5((password + salt).encode('utf-8')).hexdigest()
        return b"{SMD5}" + base64.b64encode(binascii.unhexlify(digest) + salt.encode('utf-8'))

    def get_ldap_groups(self, username):
        dn = env("LDAP_GROUP_DN")
        query = "(&(objectClass=posixGroup)(memberUid=%s))" % username
        output = self.ldap.search_s(dn, ldap.SCOPE_SUBTREE, query, ['cn', ])
        return [group[1]['cn'][0].decode('utf-8') for group in output]
