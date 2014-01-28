from django.test import TestCase, Client
from django.template.loader import render_to_string

from user_contacts.models import (
    Person,
    Phone)
from user_contacts.views import *


class ViewTest(TestCase):

    def tearDown(self):
        self.phone.delete()
        self.person.delete()

    def setUp(self):
        self.client_stub = Client()
        self.person = Person(
            first_name='TestFirst',
            last_name='TestLast')
        self.person.save()
        self.phone = Phone(
            person=self.person,
            number='12345')
        self.phone.save()

    def test_view_home_route(self):
        response = self.client_stub.get('/')
        self.assertEquals(response.status_code, 200)

    def test_view_contacts_route(self):
        response = self.client_stub.get('/all/')
        self.assertEquals(response.status_code, 200)

    def test_add_contact_route(self):
        response = self.client_stub.get('/add/')
        self.assertEquals(response.status_code, 200)

    def test_create_contact_successful_route(self):
        data = {
            'first_name': 'testFirst',
            'last_name': 'testLast',
            'email': 'test@example.com',
            'address': '123 Fake St',
            'city': 'Some Town',
            'state': 'MN',
            'country': 'USA',
            'number': '12345'}
        response = self.client_stub.post(
            '/create',
            data=data)
        self.assertEquals(response.status_code, 302)

    def test_create_fail_route(self):
        data = {
            'first_name': 'bad_@_bad',
            'last_name': 'testLast',
            'email': 'test@example.com',
            'address': '123 Fake St',
            'city': 'Some Town',
            'state': 'MN',
            'country': 'USA',
            'number': '12345'}
        response = self.client_stub.post(
            '/create',
            data=data)
        self.assertEquals(response.status_code, 200)
