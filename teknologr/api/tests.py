from django.test import TestCase
from django.contrib.auth.models import User, Group
from members.models import *
from rest_framework import status
from rest_framework.test import APITestCase

class BaseAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='svakar', password='teknolog')
        self.superuser = User.objects.create_superuser(username='superuser', password='teknolog')

        self.m1 = Member.objects.create(
            country='FI',
            given_names='Sverker Svakar',
            preferred_name='Svakar',
            surname='von Teknolog',
            street_address='OK01',
            postal_code='11111',
            city='Stad1',
            phone='040-1',
            email='1@teknolog.com',
            birth_date='1999-01-01',
            student_id='111111',
            degree_programme='Energi– och miljöteknik',
            enrolment_year=2019,
            graduated=True,
            graduated_year=2022,
            dead=False,
            subscribed_to_modulen=True,
            allow_publish_info=False,
            allow_studentbladet=True,
            comment='Kommentar',
        )
        self.m2 = Member.objects.create(
            country='FI',
            given_names='Sigrid Svatta',
            preferred_name='Svatta',
            surname='von Teknolog',
            street_address='OK02',
            postal_code='22222',
            city='Stad2',
            phone='040-2',
            email='2@teknolog.com',
            birth_date='2999-02-02',
            student_id='222222',
            degree_programme='Energi– och miljöteknik',
            enrolment_year=2019,
            graduated=True,
            graduated_year=2022,
            dead=True,
            subscribed_to_modulen=True,
            allow_publish_info=True,
            allow_studentbladet=True,
            comment='Kommentar',
        )
        self.m3 = Member.objects.create(
            country='FI',
            given_names='Test',
            preferred_name='Test',
            surname='von Teknolog',
            street_address='OK03',
            postal_code='33333',
            city='Stad3',
            phone='040-3',
            email='3@teknolog.com',
            birth_date='3999-03-03',
            student_id='333333',
            degree_programme='Energi– och miljöteknik',
            enrolment_year=2019,
            graduated=True,
            graduated_year=2022,
            dead=False,
            subscribed_to_modulen=True,
            allow_publish_info=True,
            allow_studentbladet=True,
            comment='Kommentar',
        )

        self.d = Decoration.objects.create(name="My decoration")
        self.do = DecorationOwnership.objects.create(decoration=self.d, member=self.m1, acquired=datetime.date.today())

        self.ft = FunctionaryType.objects.create(name="My functionarytype")
        self.f = Functionary.objects.create(functionarytype=self.ft, member=self.m1, begin_date=datetime.date.today(), end_date=datetime.date.today())

        self.gt = GroupType.objects.create(name="My grouptype")
        self.g = Group.objects.create(grouptype=self.gt, begin_date=datetime.date.today(), end_date=datetime.date.today())
        self.gm = GroupMembership.objects.create(group=self.g, member=self.m1)

        self.ms = [self.m1, self.m2, self.m3]

    def login_user(self):
        self.client.login(username='svakar', password='teknolog')

    def login_superuser(self):
        self.client.login(username='superuser', password='teknolog')

    def get_all(self):
        return self.client.get(self.api_path)

    def get_one(self, obj):
        return self.client.get(f'{self.api_path}{obj.id}/')
    
    def post(self):
        return self.client.post(self.api_path, self.post_data)


'''
Test implementation classes that implements all the tests. The test case classes then sets up their own test data and extends from these classes to get the sutiable tests.
'''

class GetAllMethodTests():
    def test_get_all_for_anonymous_users(self):
        response = self.get_all()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_for_user(self):
        self.login_user()
        response = self.get_all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), self.n_all)

    def test_get_all_for_superuser(self):
        self.login_superuser()
        response = self.get_all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), self.n_all)

class GetOneMethodTests():
    def test_get_one_for_anonymous_users(self):
        response = self.get_one(self.item)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_one_for_user(self):
        self.login_user()
        response = self.get_one(self.item)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        for column in self.columns_partial:
            self.assertTrue(column in data, f"Column '{column}' not in {data}")
        self.assertEqual(len(data), len(self.columns_partial), f'Length not {len(self.columns_partial)}: {data}')

    def test_get_one_for_superuser(self):
        self.login_superuser()
        response = self.get_one(self.item)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        for column in self.columns_full:
            self.assertTrue(column in data, f"Column '{column}' not in {data}")
        self.assertEqual(len(data), len(self.columns_full), f'Length not {len(self.columns_full)}: {data}')

class PostMethodTests():
    def test_post_for_anonymous_users(self):
        response = self.post()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_for_user(self):
        self.login_user()
        response = self.post()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_for_superuser(self):
        self.login_superuser()
        response = self.post()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


'''
Test case classes that extends one or many test implementation classes. Each test case class sets up their own custom test data.
'''

# MEMBERS

all_member_columns = ['id', 'country', 'created', 'modified', 'given_names', 'preferred_name', 'surname', 'street_address', 'postal_code', 'city', 'phone', 'email', 'birth_date', 'student_id', 'degree_programme', 'enrolment_year', 'graduated', 'graduated_year', 'dead', 'subscribed_to_modulen', 'allow_publish_info', 'allow_studentbladet', 'comment', 'username', 'bill_code']

class MembersAPITest(BaseAPITest, GetAllMethodTests, PostMethodTests):
    def setUp(self):
        super().setUp()
        self.api_path = '/api/members/'
        self.n_all = len(self.ms)
        self.post_data = {}

class MemberHiddenAPITest(BaseAPITest, GetOneMethodTests):
    def setUp(self):
        super().setUp()
        self.api_path = '/api/members/'
        self.item = self.m1
        self.columns_partial = ['id', 'given_names', 'preferred_name', 'surname', 'degree_programme', 'enrolment_year', 'graduated', 'graduated_year']
        self.columns_full = all_member_columns

class MemberDeadAPITest(BaseAPITest, GetOneMethodTests):
    def setUp(self):
        super().setUp()
        self.api_path = '/api/members/'
        self.item = self.m2
        self.columns_partial = ['id', 'given_names', 'preferred_name', 'surname', 'degree_programme', 'enrolment_year', 'graduated', 'graduated_year']
        self.columns_full = all_member_columns

class MemberNormalAPITest(BaseAPITest, GetOneMethodTests):
    def setUp(self):
        super().setUp()
        self.api_path = '/api/members/'
        self.item = self.m3
        self.columns_partial = ['id', 'given_names', 'preferred_name', 'surname', 'street_address', 'postal_code', 'city', 'country', 'phone', 'email', 'degree_programme', 'enrolment_year', 'graduated', 'graduated_year']
        self.columns_full = all_member_columns


# DECORATIONS

class DecorationsAPITest(BaseAPITest, GetOneMethodTests, GetAllMethodTests, PostMethodTests):
    def setUp(self):
        super().setUp()
        self.api_path = '/api/decorations/'
        self.item = self.d
        self.columns_partial = ['id', 'name', 'comment']
        self.columns_full = self.columns_partial + ['created', 'modified']
        self.n_all = 1
        self.post_data = {'name': 'test'}

class DecorationMembershipsAPITest(BaseAPITest, GetOneMethodTests, GetAllMethodTests, PostMethodTests):
    def setUp(self):
        super().setUp()
        self.api_path = '/api/decorationownerships/'
        self.item = self.do
        self.columns_partial = ['id', 'decoration', 'member', 'acquired']
        self.columns_full = self.columns_partial + ['created', 'modified']
        self.n_all = 1
        self.post_data = {
            'decoration': self.d.id,
            'member': self.m2.id,
            'acquired': datetime.date.today().isoformat(),
        }


# FUNCTIONARIES

class FunctionaryTypesAPITest(BaseAPITest, GetOneMethodTests, GetAllMethodTests, PostMethodTests):
    def setUp(self):
        super().setUp()
        self.api_path = '/api/functionarytypes/'
        self.item = self.ft
        self.columns_partial = ['id', 'name', 'comment']
        self.columns_full = self.columns_partial + ['created', 'modified']
        self.n_all = 1
        self.post_data = {'name': 'test'}

class FunctionariesAPITest(BaseAPITest, GetOneMethodTests, GetAllMethodTests, PostMethodTests):
    def setUp(self):
        super().setUp()
        self.api_path = '/api/functionaries/'
        self.item = self.f
        self.columns_partial = ['id', 'functionarytype', 'member', 'begin_date', 'end_date']
        self.columns_full = self.columns_partial + ['created', 'modified']
        self.n_all = 1
        self.post_data = {
            'functionarytype': self.ft.id,
            'member': self.m2.id,
            'begin_date': datetime.date.today().isoformat(),
            'end_date': datetime.date.today().isoformat(),
        }


# GROUPS

class GroupTypesAPITest(BaseAPITest, GetOneMethodTests, GetAllMethodTests, PostMethodTests):
    def setUp(self):
        super().setUp()
        self.api_path = '/api/grouptypes/'
        self.item = self.gt
        self.columns_partial = ['id', 'name', 'comment']
        self.columns_full = self.columns_partial + ['created', 'modified']
        self.n_all = 1
        self.post_data = {'name': 'test'}

class GroupsAPITest(BaseAPITest, GetOneMethodTests, GetAllMethodTests, PostMethodTests):
    def setUp(self):
        super().setUp()
        self.api_path = '/api/groups/'
        self.item = self.g
        self.columns_partial = ['id', 'grouptype', 'begin_date', 'end_date']
        self.columns_full = self.columns_partial + ['created', 'modified']
        self.n_all = 1
        self.post_data = {
            'grouptype': self.gt.id,
            'begin_date': datetime.date.today().isoformat(),
            'end_date': datetime.date.today().isoformat(),
        }

class GroupMembershipsAPITest(BaseAPITest, GetOneMethodTests, GetAllMethodTests, PostMethodTests):
    def setUp(self):
        super().setUp()
        self.api_path = '/api/groupmemberships/'
        self.item = self.gm
        self.columns_partial = ['id', 'group', 'member']
        self.columns_full = self.columns_partial + ['created', 'modified']
        self.n_all = 1
        self.post_data = {
            'group': self.g.id,
            'member': self.m2.id,
        }
