from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTestsHaris(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_super_user(
                email='haris.np@gmail.com',
                password='12345'
            )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@haris.com',
            password='12345',
            name='Test user Full Name'
            )

    def test_user_listed(self):
        """
        Test for the user lsited
        """
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """
        Testing the user change page
        """
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEquals(res.status_code, 200)

    def test_create_user_page(self):
        """
        Testing for the user create page works
        """
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEquals(res.status_code, 200)
