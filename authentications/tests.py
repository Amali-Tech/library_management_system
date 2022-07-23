"""Test cases for User Authentication"""
from rest_framework.test import APITestCase

class TestSetup(APITestCase):
    """Test Setup"""
    def setUp(self):
        """Setup of the test"""
        self.register_url = "/user/register/"
        self.login_url = "/user/login/"
        self.admin_register_url = "/user/list/"

        self.user_data = {
            "email_address":"test1@gmail.com",
            "username": "test1",
            "password": "test212",
        }
        return super().setUp()


class TestViews(TestSetup):
    """Unit test for views"""
    def test_user_can_register(self):
        """Test to see if user can register"""
        response = self.client.post(self.register_url, self.user_data,
        format="json")
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code, 201)

    def test_not_active_or_not_registered_user_can_login(self):
        """Test to see if user that is not active or not registered
        ca login into the system"""
        res = self.client.post(self.login_url, self.user_data,
        format="json")
        self.assertEqual(res.status_code, 401)
    def test_active_or_registered_user_can_login(self):
        """Test to see if user that is not active or not registered
        ca login into the system"""
        response = self.client.post(self.register_url, self.user_data,
        format="json")
        res = self.client.post(self.login_url, self.user_data,
        format="json")
        self.assertEqual(res.status_code, 200)

    def test_admin_register_users(self):
        """Test to see if admin can register a user"""
        response = self.client.post(self.register_url,
        data = self.user_data, format = "json")
        self.assertEqual(response.status_code, 201)
