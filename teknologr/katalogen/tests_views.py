
from rest_framework import status
from api.tests import BaseAPITest

class GetPageTests():
    def test_get_for_anonymous_users(self):
        response = self.get_all()
        self.check_status_code(response, status.HTTP_302_FOUND)
        self.assertTrue(response.url.startswith('/login/'), response.url)

    def test_get_for_user(self):
        self.login_user()
        response = self.get_all()
        self.check_status_code(response, status.HTTP_200_OK)


class HomeViewTest(BaseAPITest, GetPageTests):
    def setUp(self):
        super().setUp()
        self.api_path = ''


class MembersEmptySearchViewTest(BaseAPITest, GetPageTests):
    def setUp(self):
        super().setUp()
        self.api_path = '/search/?q='

class MembersStartsWithViewTest(BaseAPITest, GetPageTests):
    def setUp(self):
        super().setUp()
        self.api_path = '/A/'

class MemberViewTest(BaseAPITest, GetPageTests):
    def setUp(self):
        super().setUp()
        self.api_path = f'/members/{self.m1.id}/'


class DecorationOwnershipsViewTest(BaseAPITest, GetPageTests):
    def setUp(self):
        super().setUp()
        self.api_path = f'/decorations/{self.d.id}/'


class DecorationsViewTest(BaseAPITest, GetPageTests):
    def setUp(self):
        super().setUp()
        self.api_path = '/decorations/'

class DecorationOwnershipsViewTest(BaseAPITest, GetPageTests):
    def setUp(self):
        super().setUp()
        self.api_path = f'/decorations/{self.d.id}/'


class FunctionaryTypesViewTest(BaseAPITest, GetPageTests):
    def setUp(self):
        super().setUp()
        self.api_path = '/functionaries/'

class FunctionariesViewTest(BaseAPITest, GetPageTests):
    def setUp(self):
        super().setUp()
        self.api_path = f'/functionaries/{self.ft.id}/'


class GroupTypesViewTest(BaseAPITest, GetPageTests):
    def setUp(self):
        super().setUp()
        self.api_path = '/groups/'

class GroupsViewTest(BaseAPITest, GetPageTests):
    def setUp(self):
        super().setUp()
        self.api_path = f'/groups/{self.gt.id}/'

class GroupMembershipsViewTest(BaseAPITest, GetPageTests):
    def setUp(self):
        super().setUp()
        self.api_path = f'/groupmemberships/{self.gt.id}/'


class YearsViewTest(BaseAPITest, GetPageTests):
    def setUp(self):
        super().setUp()
        self.api_path = '/years/'

class YearViewTest(BaseAPITest, GetPageTests):
    def setUp(self):
        super().setUp()
        self.api_path = f'/years/2023/'

class Year0ViewTest(BaseAPITest, GetPageTests):
    def setUp(self):
        super().setUp()
        self.api_path = f'/years/0/'
