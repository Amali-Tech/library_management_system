"""Test cases for Book and Catalog Views"""
from rest_framework.test import APITestCase


class TestSetup(APITestCase):
    """Test Setup"""
    def setUp(self):
        """Setup of the test"""
        self.catalog_url = "/api/catalog/"
        self.books_url = "/api/books/"

        self.catalog_data = {
            "category":"Programming"
        }
        return super().setUp()


class TestViews(TestSetup):
    """Testing of the catalog view endpoints"""
    def test_not_admin_add_category(self):
        """Testing to see if unauthenticated users can add category"""
        response = self.client.post(self.catalog_url,
        self.catalog_data, format="json")
        self.assertEqual(response.status_code, 401)

    def test_get_all_books(self):
        """Test to see if ananymous users see all books in the database"""
        response = self.client.get(self.books_url)
        self.assertEqual(response.status_code, 401)
