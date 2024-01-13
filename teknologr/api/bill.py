import requests
import re
import json
from getenv import env


class BILLException(Exception):
    pass


class BILLAccountManager:
    ERROR_ACCOUNT_DOES_NOT_EXIST = "BILL account does not exist"

    def __init__(self):
        self.api_url = env("BILL_API_URL")
        self.user = env("BILL_API_USER")
        self.password = env("BILL_API_PW")

    def admin_url(self, bill_code):
        if not self.api_url:
            return ''
        return f'{"/".join(self.api_url.split("/")[:-2])}/admin/userdata?id={bill_code}'

    def __request(self, path):
        try:
            r = requests.post(self.api_url + path, auth=(self.user, self.password))
        except:
            raise BILLException("Could not connect to BILL server")

        if r.status_code != 200:
            raise BILLException(f"BILL returned status code {r.status_code}")

        # Not a number, return as text
        try:
            number = int(r.text)
        except ValueError:
            return r.text

        # A negative number means an error code
        if number == -3:
            raise BILLException(BILLAccountManager.ERROR_ACCOUNT_DOES_NOT_EXIST)
        if number < 0:
            raise BILLException(f"BILL returned error code: {number}")

        return number

    def create_bill_account(self, username):
        if not re.search(r'^[A-Za-z0-9]+$', username):
            raise BILLException("Can not create a BILL account using an LDAP username containing anything other than letters and numbers")

        result = self.__request(f"add?type=user&id={username}")
        if type(result) == int:
            return result
        raise BILLException(f"BILL returned error: {result}")

    def delete_bill_account(self, bill_code):
        info = self.get_account_by_code(bill_code)

        # If the BILL account does not exist all is ok
        if not info:
            return

        result = self.__request(f"del?type=user&acc={bill_code}")

        if result != 0:
            raise BILLException(f"BILL returned error: {result}")

    def get_account_by_username(self, username):
        '''
        Get the info for a certain BILL account. Returns None if the account does not exist.
        '''
        try:
            result = self.__request(f"get?type=user&id={username}")
            return json.loads(result)
        except BILLException as e:
            s = str(e)
            if s == BILLAccountManager.ERROR_ACCOUNT_DOES_NOT_EXIST:
                return None
            raise e

    def get_account_by_code(self, bill_code):
        '''
        Get the info for a certain BILL account. Returns None if the account does not exist.
        '''
        try:
            result = self.__request(f"get?type=user&acc={bill_code}")
            return json.loads(result)
        except BILLException as e:
            s = str(e)
            if s == BILLAccountManager.ERROR_ACCOUNT_DOES_NOT_EXIST:
                return None
            raise e
