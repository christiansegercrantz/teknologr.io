
from rest_framework import status
from api.tests import BaseAPITest

class GetPageTests():
    def test_get_for_anonymous_users(self):
        response = self.get_all()
        self.check_status_code(response, status.HTTP_200_OK)


class RegistrationViewTest(BaseAPITest, GetPageTests):
    def setUp(self):
        super().setUp()
        self.api_path = '/registration/#collapse-info'
