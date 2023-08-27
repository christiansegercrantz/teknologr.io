from django.contrib.auth.models import User
from members.models import *
from rest_framework import status
from rest_framework.test import APITestCase

class BaseClass(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='svakar', password='teknolog')
        self.superuser = User.objects.create_superuser(username='superuser', password='teknolog')

        self.member = Member.objects.create(
            given_names='Sverker Svakar',
            preferred_name='Svakar',
            surname='von Teknolog',
            student_id='123456',
            username='vonteks1',
        )

        self.d1 = '2000-01-01'
        self.d2 = '2000-07-07'

        MemberType.objects.create(member=self.member, type='PH', begin_date=self.d1, end_date=self.d2)
        MemberType.objects.create(member=self.member, type='OM', begin_date=self.d2)

    def login_user(self):
        self.client.login(username='svakar', password='teknolog')

    def login_superuser(self):
        self.client.login(username='superuser', password='teknolog')


class TestCases:
    def test_get_for_anonymous_users(self):
        response = self.get()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_for_user(self):
        self.login_user()
        response = self.get()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_for_superuser(self):
        self.login_superuser()
        response = self.get()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if self.response is None:
            self.assertEqual(self.response, response.data)
        else:
            self.assertEqual(self.response, response.json())

class ByUsernameTestCases(TestCases):
    def get(self):
        return self.client.get(f'/api/memberTypesForMember/username/{self.username}/')

class ByStudynumberTestCases(TestCases):
    def get(self):
        return self.client.get(f'/api/memberTypesForMember/studynumber/{self.studynumber}/')


RESPONSE = {
    'given_names': [
        'Sverker',
        'Svakar',
    ],
    'surname': 'von Teknolog',
    'nickname': '',
    'preferred_name': 'Svakar',
    'membertypes': {
        'OM': [
            '2000-07-07',
            'None'
        ],
        'PH': [
            '2000-01-01',
            '2000-07-07'
        ]
    }
}

class ByInvalidUsernameTests(BaseClass, ByUsernameTestCases):
    def setUp(self):
        super().setUp()
        self.username = 'invalid'
        self.response = None

class ByValidUsernameTests(BaseClass, ByUsernameTestCases):
    def setUp(self):
        super().setUp()
        self.username = self.member.username
        self.response = RESPONSE


class ByInvalidStudynumberTests(BaseClass, ByStudynumberTestCases):
    def setUp(self):
        super().setUp()
        self.studynumber = '123321'
        self.response = None

class ByValidStudynumberTests(BaseClass, ByStudynumberTestCases):
    def setUp(self):
        super().setUp()
        self.studynumber = self.member.student_id
        self.response = RESPONSE
