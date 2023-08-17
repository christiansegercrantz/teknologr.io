
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


class SearchTests(BaseAPITest):
    path1 = '/search/?q=Svakar'
    path2 = '/search/?q=Sverker'

    def test_search_for_user(self):
        # Test redirect if only one Member was found
        self.api_path = self.path1
        self.login_user()
        response = self.get_all()
        self.check_status_code(response, status.HTTP_302_FOUND)
        self.assertEqual(f'/members/{self.m1.id}/', response.url)

    def test_search_for_superuser(self):
        self.api_path = self.path1
        self.login_superuser()
        response = self.get_all()
        self.check_status_code(response, status.HTTP_302_FOUND)
        self.assertEqual(f'/members/{self.m1.id}/', response.url)

    def test_search_hidden_name_for_user(self):
        # Test that hidden Members are not found by their non-preferred given name
        self.api_path = self.path2
        self.login_user()
        response = self.get_all()
        self.check_status_code(response, status.HTTP_200_OK)
        self.assertNotContains(response, "Svakar")
        self.assertNotContains(response, "Sverker")

    def test_search_hidden_name_for_superuser(self):
        self.api_path = self.path2
        self.login_superuser()
        response = self.get_all()
        self.check_status_code(response, status.HTTP_200_OK)
        self.assertNotContains(response, "Svakar")
        self.assertNotContains(response, "Sverker")
