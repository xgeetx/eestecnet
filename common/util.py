from django.core.urlresolvers import reverse_lazy
from django.test import Client
from rest_framework.renderers import JSONRenderer


__author__ = 'Sebastian Wozny'
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class Reversable(object):
    def get_absolute_url(self):
        return reverse_lazy(self._meta.model_name + '-detail', kwargs={'pk': self.pk})

class RESTCase(object):
    """
    Mixin that combines common functionality for testing the REST API.
    By default will also test the list and absolute endpoints of a resource.
    To use this mixin the child testcase must create a self.object resource.
    """
    def setUp(self):
        from apps.accounts.factories import AccountFactory
        admin = AccountFactory(email="admin@admin.de")
        admin.set_password("admin")
        admin.is_superuser = True
        admin.save()
        self.c = Client()
        self.c.post('/login/', data={'username': 'admin@admin.de', 'password': 'admin'})
        self.root = "/api"

        super(RESTCase, self).setUp()


    def assert_create(self, url, data):
        response = self.c.post(url, data)
        try:
            self.assertEqual(response.status_code, 201)
        except AssertionError:
            print response.content
            print data
            raise

    def assert_retrieve(self, url):
        response = self.c.get(url)
        try:
            self.assertEqual(response.status_code, 200)
        except AssertionError:
            print response.content
            raise

    def assert_update(self, url, data):
        json = JSONRenderer().render(data)
        response = self.c.put(path=url, data=json, content_type='application/json')
        try:
            self.assertIn(response.status_code, [200, 202, 204])
        except AssertionError:
            print response.content
            raise


    def assert_delete(self, url):
        response = self.c.delete(path=url)
        try:
            self.assertIn(response.status_code, [200, 202, 204])
        except AssertionError:
            print response.content
            raise


    def test_rest_list_resource(self):
        self.assert_retrieve(
            reverse_lazy(self.object._meta.object_name.lower() + '-list'))

    def test_rest_retrieve_resource(self):
        url = self.object.get_absolute_url()
        self.assert_retrieve(url)

    def test_rest_create_resource(self):
        url = self.object.get_absolute_url()
        self.assert_delete(url)
        data = self.serializer_class(self.object).data
        url = reverse_lazy(self.object._meta.object_name.lower() + '-list')
        self.assert_create(url, data)

    def test_rest_update_resource(self):
        data = self.serializer_class(self.object).data
        url = self.object.get_absolute_url()
        self.assert_update(url, data)

    def test_rest_delete_resource(self):
        url = self.object.get_absolute_url()
        self.assert_delete(url)
