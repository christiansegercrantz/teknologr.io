
from rest_framework import status
from api.tests import BaseAPITest

class GetPageTests():
    def test_get_for_anonymous_users(self):
        response = self.get_all()
        self.check_status_code(response, status.HTTP_302_FOUND)
        self.assertTrue(response.url.startswith('/login/'), response.url)

    def test_get_for_users(self):
        response = self.get_all()
        self.check_status_code(response, status.HTTP_302_FOUND)
        self.assertTrue(response.url.startswith('/login/'), response.url)

    def test_get_for_superusers(self):
        self.login_superuser()
        response = self.get_all()
        self.check_status_code(response, status.HTTP_200_OK)


class HomeViewTest(BaseAPITest, GetPageTests):
    def setUp(self):
        super().setUp()
        self.api_path = '/admin/members/'


class MemberViewTest(BaseAPITest, GetPageTests):
    def setUp(self):
        super().setUp()
        self.api_path = f'/admin/members/{self.m1.id}/'


class DecorationOwnershipsViewTest(BaseAPITest, GetPageTests):
    def setUp(self):
        super().setUp()
        self.api_path = f'/admin/decorations/{self.d.id}/'


class DecorationsViewTest(BaseAPITest, GetPageTests):
    def setUp(self):
        super().setUp()
        self.api_path = '/admin/decorations/'

class DecorationOwnershipsViewTest(BaseAPITest, GetPageTests):
    def setUp(self):
        super().setUp()
        self.api_path = f'/admin/decorations/{self.d.id}/'


class FunctionaryTypesViewTest(BaseAPITest, GetPageTests):
    def setUp(self):
        super().setUp()
        self.api_path = '/admin/functionarytypes/'

class FunctionariesViewTest(BaseAPITest, GetPageTests):
    def setUp(self):
        super().setUp()
        self.api_path = f'/admin/functionarytypes/{self.ft.id}/'


class GroupTypesViewTest(BaseAPITest, GetPageTests):
    def setUp(self):
        super().setUp()
        self.api_path = '/admin/grouptypes/'

class GroupsViewTest(BaseAPITest, GetPageTests):
    def setUp(self):
        super().setUp()
        self.api_path = f'/admin/grouptypes/{self.gt.id}/'

class GroupMembershipsViewTest(BaseAPITest, GetPageTests):
    def setUp(self):
        super().setUp()
        self.api_path = f'/admin/grouptypes/{self.gt.id}/{self.g.id}/'


class ApplicantsViewTest(BaseAPITest, GetPageTests):
    def setUp(self):
        super().setUp()
        self.api_path = '/admin/applicants/'

class ApplicantViewTest(BaseAPITest, GetPageTests):
    def setUp(self):
        super().setUp()
        self.api_path = f'/admin/applicants/{self.a.id}/'
