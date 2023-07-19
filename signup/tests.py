from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task


class AuthenticationTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        u1 = User.objects.create_user(
            username="test_user1", password="test_user1_password"
        )
        u2 = User.objects.create_user(
            username="test_user2", password="test_user2_password"
        )
        Task.objects.create(
            user=u1,
            title="test task 1",
            text="text",
            created_at=timezone.now(),
            due_date=timezone.now() + timedelta(days=1),
            status="low_priority",
        )

    def test_login_correct(self):
        """Users that proviede correct credentials are successfully logged in"""
        c = Client()
        self.assertTrue(c.login(username="test_user1", password="test_user1_password"))
        c.logout()
        self.assertTrue(c.login(username="test_user2", password="test_user2_password"))

    def test_login_wrong(self):
        """Users that proviede wrong credentials are not logged in"""
        c = Client()
        self.assertFalse(c.login(username="test_user1", password="test_user2_password"))
        c.logout()
        self.assertFalse(c.login(username="test_user2", password="test_user1_password"))

    def test_login_required_index(self):
        """Users that are not logged in get redirected to the login page from the home page"""
        c = Client()
        response = c.get("/", follow=True)
        self.assertEqual(response.redirect_chain[0], ("/user/login?next=/", 302))

    def test_login_required_detail(self):
        """Users that are not logged in get redirected to the login page from the detail page"""
        c = Client()
        response = c.get("/task/1/", follow=True)
        self.assertIn("/user/login?next=/", response.redirect_chain[0][0])
        self.assertEqual(response.redirect_chain[0][1], 302)

    def test_login_required_edit(self):
        """Users that are not logged in get redirected to the login page from the edit page"""
        c = Client()
        response = c.get("/task/1/edit/", follow=True)
        self.assertIn("/user/login?next=/", response.redirect_chain[0][0])
        self.assertEqual(response.redirect_chain[0][1], 302)

    def test_login_required_delete(self):
        """Users that are not logged in get redirected to the login page from the delete page"""
        c = Client()
        response = c.get("/task/1/delete", follow=True)
        self.assertIn("/user/login?next=/", response.redirect_chain[2][0])
        self.assertEqual(response.redirect_chain[2][1], 302)

    def test_user_permission(self):
        """Users can't interact with other's tasks"""
        c = Client()
        c.login(username="test_user2", password="test_user2_password")
        self.assertEqual(c.get("/task/1/").status_code, 302)
        self.assertEqual(c.get("/task/1/edit/").status_code, 302)
        self.assertEqual(c.get("/task/1/delete/").status_code, 302)

    def test_access_granted(self):
        """Users can interact with their tasks"""
        c = Client()
        self.assertTrue(c.login(username="test_user1", password="test_user1_password"))
        self.assertEqual(c.get("/task/1/").status_code, 200)
        self.assertEqual(c.get("/task/1/edit/").status_code, 200)
