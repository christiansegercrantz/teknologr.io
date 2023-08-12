from django.contrib.auth.models import User
from members.models import *
from rest_framework import status
from rest_framework.test import APITestCase

class BaseClass(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='svakar', password='teknolog')
        self.superuser = User.objects.create_superuser(username='superuser', password='teknolog')

        self.m1 = Member.objects.create(
            given_names='Sverker Svakar',
            preferred_name='Svakar',
            surname='von Teknolog',
            student_id='123456',
            username='vonteks1',
        )
        self.m2 = Member.objects.create(
            given_names='Svatta',
            surname='von Teknolog',
            student_id='654321',
            username='vonteks2',
        )
        self.m3 = Member.objects.create(
            given_names='Simon',
            surname='von Teknolog',
        )

        d1 = '2000-01-01'
        d2 = '2010-01-01'

        MemberType.objects.create(member=self.m1, type='PH', begin_date=d1, end_date=d2)
        MemberType.objects.create(member=self.m1, type='OM', begin_date=d2)
        MemberType.objects.create(member=self.m1, type='JS', begin_date=d1)

        MemberType.objects.create(member=self.m2, type='PH', begin_date=d1, end_date=d2)
        MemberType.objects.create(member=self.m2, type='OM', begin_date=d2)
        MemberType.objects.create(member=self.m2, type='ST', begin_date=d1)
        MemberType.objects.create(member=self.m2, type='ST', begin_date=d2)

        MemberType.objects.create(member=self.m3, type='JS', begin_date=d1)
        MemberType.objects.create(member=self.m3, type='ST', begin_date=d2)
        MemberType.objects.create(member=self.m3, type='ST', begin_date=d2)

    def login_superuser(self):
        self.client.login(username='superuser', password='teknolog')

class GenerikeyTestCases():
    def test_get_for_anonymous_users(self):
        response = self.get('PH')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_for_user(self):
        self.client.login(username='svakar', password='teknolog')
        response = self.get('PH')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_not_found(self):
        self.login_superuser()
        response = self.get('XXX')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_invalid(self):
        self.login_superuser()
        response = self.get('XX')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])

    def test_get_all_ended(self):
        self.login_superuser()
        response = self.get('PH')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])

    def test_get_normal(self):
        self.login_superuser()
        response = self.get('OM')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), self.normal)

    def test_get_null(self):
        self.login_superuser()
        response = self.get('JS')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), self.null)

    def test_get_double(self):
        self.login_superuser()
        response = self.get('ST')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), self.double)


class GenerikeyStudynumbersTestCases(BaseClass, GenerikeyTestCases):
    normal = ['123456', '654321']
    null = ['123456', None]
    double = ['654321', None]

    def get(self, type):
        return self.client.get(f'/api/membersByMemberType/{type}/')


class GenerikeyUsernamesTestCases(BaseClass, GenerikeyTestCases):
    normal = ['vonteks1', 'vonteks2']
    null = ['vonteks1', None]
    double = ['vonteks2', None]

    def get(self, type):
        return self.client.get(f'/api/membersByMemberType/{type}/usernames')
