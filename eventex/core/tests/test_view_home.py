from django.test import TestCase
from django.shortcuts import resolve_url as r

# Create your tests here.
class HomeTest(TestCase): #TestCase já vem com o Django
    def setUp(self):
        self.response = self.client.get(r('home'))  # client já vem no TestCase do Django

    def test_get(self):
        """GET / must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use index.html"""
        self.assertTemplateUsed(self.response, 'index.html')

    def test_subscription_link(self):
        """"""
        expected='href="{}"'.format(r('subscriptions:new'))
        self.assertContains(self.response, expected )
