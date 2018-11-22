import datetime
import pdb
from ldap import LDAPError

from django.test import TestCase

from .models import Member, MemberType

# Create your tests here.


class MemberModelTest(TestCase):
    """
    A test class for testing the Member model
    """
    def test_member_str(self):
        member = Member(
            given_names="Svakar",
            surname="Teknolog"
        )
        self.assertEquals("Svakar Teknolog", str(member))

    def test_get_full_name(self):
        member = Member(
            given_names="Svakar Svakarsson",
            surname="Teknolog"
        )
        self.assertEquals("Svakar Svakarsson Teknolog", member.full_name)

    def test_get_full_preferred_name(self):
        member = Member(
            given_names="Svakar",
            surname="Teknolog",
            preferred_name="Svackis",
        )
        self.assertEquals("Svackis Teknolog", member.full_preferred_name)

    def test_maiden_name(self):
        member = Member(
            given_names="Svatta",
            surname="Teknolog",
            maiden_name="Hankeit"
        )
        self.assertEquals("Svatta Teknolog", member.name)

    def test_address(self):
        member = Member(
            given_names="Svatta",
            surname="Teknolog",
            street_address="Otsvängen 22",
            postal_code="02150",
            city="Esbo",
        )
        self.assertEquals("Otsvängen 22, 02150, Esbo, Finland", member._get_full_address())

    def test_foreign_address(self):
        member = Member(
            given_names="Svatta",
            surname="Teknolog",
            street_address="Dr. Martin Luther King Boulevard #78",
            postal_code="",
            city="Williemstad",
            country="CW"
        )
        self.assertEquals("Dr. Martin Luther King Boulevard #78, Williemstad, Curaçao", member._get_full_address())

    def test_member_type(self):
        member = Member(
            given_names="Svatta",
            surname="Teknolog",
        )
        member.save()

        # test that there are no membertypes yet
        self.assertEquals("", member.current_member_type)

        # add some member types. First default member type phux
        ph = MemberType(member=member, begin_date=datetime.date(2012, 9, 1))
        ph.save()
        # A 'Phux' is not a real member type and should return ""
        self.assertEquals("", member.current_member_type)
        self.assertFalse(member.isValidMember())

        # Make our person a 'real member'
        om = MemberType(member=member, type="OM", begin_date=datetime.date(2012, 9, 27))
        om.save()
        self.assertEquals("Ordinarie Medlem", member.current_member_type)
        self.assertTrue(member.isValidMember())

        self.assertEquals("Ordinarie Medlem: 2012-09-27->", str(om))

        # Wappen kom, phuxen är inte mera phux!
        ph.end_date = datetime.date(2012, 4, 30)
        ph.save()
        self.assertEquals("Phux: 2012-09-01-2012-04-30", str(ph))
        self.assertFalse(member.shouldBeStalm())

        # Our person became JuniorStÄlM :O
        js = MemberType(member=member, type="JS", begin_date=datetime.date(2017, 10, 15))
        js.save()
        self.assertFalse(member.shouldBeStalm())

        # Our person is now finished with his/her studies
        om.end_date = datetime.date(2019, 4, 30)
        om.save()
        self.assertEquals("Ordinarie Medlem: 2012-09-27-2019-04-30", str(om))

        # member type should be nothing ("") now
        self.assertEquals("", member.current_member_type)
        # and person should become StÄlM now
        self.assertTrue(member.shouldBeStalm())

        fg = MemberType(member=member, type="FG", begin_date=datetime.date(2019, 5, 1))
        fg.save()

        st = MemberType(member=member, type="ST", begin_date=datetime.date(2019, 5, 16))
        st.save()
        self.assertEquals("StÄlM", member.current_member_type)
        self.assertFalse(member.shouldBeStalm())

    def test_saving(self):
        member = Member(
            given_names="Svatta",
            surname="Teknolog",
        )
        member.save()

        # try to cover lines missed by conditions.
        member.username = "teknosv1"
        member.student_id = "123456"
        member.email = "svatta@teknolog.fi"
        with self.assertRaises(LDAPError):
            member.save()
