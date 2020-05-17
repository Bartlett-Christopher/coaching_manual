# -*- coding: utf-8 -*-
"""
.. module:: register.tests.views.signup
   :synopsis: Unit test module for Signup View

.. moduleauthor:: Chris Bartlett
"""
from __future__ import unicode_literals

from unittest.mock import DEFAULT, patch

from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django.urls import reverse

from register.forms.signup import SignUpForm
from register.models import User
from register.views.signup import SignUpView


class TestSignUpView(TestCase):
    """ Test case for SignUpView."""

    @classmethod
    def setUpClass(cls):
        super(TestSignUpView, cls).setUpClass()
        cls.rf = RequestFactory()
        cls.url = reverse('register:signup')
        cls.view = SignUpView()
        cls.price_info = {'data': []}

    def test_get_context__context_has_form(self):
        request = self.rf.get(self.url)

        with patch.object(self.view, 'get_form') as mock:
            mock.return_value = SignUpForm()
            context = self.view.get_context(request)

        self.assertIsInstance(context, dict)
        self.assertIn('form', context)
        self.assertIsInstance(context['form'], SignUpForm)
        mock.assert_called_once_with(request)

    def test_get_form__post_request_returns_bound_form(self):
        request = self.rf.post(
            self.url,
            data={'first_name': 'chris'}
        )

        form = self.view.get_form(request)

        self.assertIsInstance(form, SignUpForm)
        self.assertTrue(form.is_bound)

    def test_get_form__get_request_returns_unbound_form(self):
        request = self.rf.get(self.url)

        form = self.view.get_form(request)

        self.assertIsInstance(form, SignUpForm)
        self.assertFalse(form.is_bound)

    def test_get_price_information__api_error(self):
        self.fail('Method not implemented yet.')

    def test_get_price_information__api_success(self):
        self.fail('Method not implemented yet.')

    def test_get__returns_response(self):
        request = self.rf.get(self.url)
        context = {'form': SignUpForm}

        with patch.multiple(
                self.view,
                get_context=DEFAULT,
                render_to_response=DEFAULT) as mocks:
            mocks['get_context'].return_value = context
            mocks['render_to_response'].return_value = HttpResponse()
            response = self.view.get(request)

        mocks['get_context'].assert_called_once_with(request)
        mocks['render_to_response'].assert_called_once_with(context)

    def test_post__data_invalid(self):
        request = self.rf.post(self.url, data={})

        with patch.multiple(
                self.view,
                get_form=DEFAULT,
                get_context=DEFAULT,
                render_to_response=DEFAULT
        ) as mocks:
            mocks['get_form'].return_value = SignUpForm(data={})
            mocks['get_context'].return_value = {}
            mocks['render_to_response'].return_value = HttpResponse()

            response = self.view.post(request)

        self.assertIsInstance(response, HttpResponse)
        mocks['get_form'].assert_called_once_with(request)
        mocks['get_context'].assert_called_once_with(request)
        mocks['render_to_response'].assert_called_once_with({})

    def test_post__external_api_error(self):
        data = {
            'first_name': 'Chris',
            'last_name': 'Bartlett',
            'email': 'bartlett.christopher.p@gmail.com',
            'country': 'GB',
        }
        request = self.rf.post(self.url, data=data)

        with patch.multiple(
                self.view,
                get_form=DEFAULT,
                get_price_information=DEFAULT,
                get_context=DEFAULT,
                render_to_response=DEFAULT
        ) as mocks:
            mocks['get_form'].return_value = SignUpForm(data=data)
            mocks['get_price_information'].return_value = {}
            mocks['get_context'].return_value = {}
            mocks['render_to_response'].return_value = HttpResponse()

            response = self.view.post(request)

        self.assertIsInstance(response, HttpResponse)
        mocks['get_form'].assert_called_once_with(request)
        mocks['get_price_information'].assert_called_once_with('GB')
        mocks['get_context'].assert_called_once_with(request)
        mocks['render_to_response'].assert_called_once_with(
            {'api_error': True}
        )

    @patch('register.views.signup.render')
    def test_post__success_saves_data(self, mock_render):
        data = {
            'first_name': 'Chris',
            'last_name': 'Bartlett',
            'email': 'bartlett.christopher.p@gmail.com',
            'country': 'GB',
        }
        request = self.rf.post(self.url, data=data)

        self.assertEqual(User.objects.count(), 0)

        with patch.multiple(
                self.view,
                get_form=DEFAULT,
                get_price_information=DEFAULT,
        ) as mocks:
            mocks['get_form'].return_value = SignUpForm(data=data)
            mocks['get_price_information'].return_value = self.price_info

            self.view.post(request)

        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.first_name, 'Chris')
        self.assertEqual(user.last_name, 'Bartlett'),
        self.assertEqual(user.email, 'bartlett.christopher.p@gmail.com')
        self.assertEqual(user.country, 'GB')
        self.assertDictEqual(user.price_info, self.price_info)
        mocks['get_form'].assert_called_once_with(request)
        mocks['get_price_information'].assert_called_once_with('GB')
        mock_render.assert_called_once_with(
            request,
            'register/complete.html',
            data
        )
