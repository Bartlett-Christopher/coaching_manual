# -*- coding: utf-8 -*-
"""
.. module:: register.tests.api.views.test_user
   :synopsis: Test suite for Register API User view

.. moduleauthor:: Chris Bartlett
"""
from unittest.mock import Mock, patch

from rest_framework import status

from django.test import TestCase
from django.urls import reverse

from register.api.views import UserAPIView
from register.models import User


class TestUserAPIView(TestCase):
    """Test suite for Register API User view."""

    @classmethod
    def setUpClass(cls):
        super(TestUserAPIView, cls).setUpClass()
        cls.price_info = [{
            'active': True,
            'billing_interval': 'MONTH',
            'currency': 'GBP',
            'frequency': 'Triannualy',
            'plan': 'gbp_triannual_referrer_spec_1',
            'price': '5.00',
            'price_per_unit': 500,
            'trial_period': 0
        },
        {
            'active': True,
            'billing_interval': 'MONTH',
            'currency': 'GBP',
            'frequency': 'Quarterly',
            'pk': 54,
            'plan': 'gbp_quarter_referrer_spec_2',
            'price': '5.00',
            'price_per_unit': 500,
            'trial_period': 0
        }]
        cls.url = reverse('api:user')

    @patch('register.api.views.user.HasAPIKey.has_permission')
    def test_get(self, mock_perms):
        mock_perms.return_value = True

        user = User.objects.create(
            first_name='Chris',
            last_name='Bartlett',
            email='chris@test.com',
            country='GB',
            price_info=self.price_info
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(len(data), 1)
        user_data = data[0]
        self.assertIn('first_name', user_data)
        self.assertEqual(user_data['first_name'], 'Chris')

    @patch('register.api.views.user.HasAPIKey.has_permission')
    def test_post__invalid_data(self, mock_perms):
        mock_perms.return_value = True

        response = self.client.post(
            self.url,
            data={
                'first_name': 'Chris',
                'last_name': 'Bartlett',
                'email': 'chris@test.com',
            }
        )

        self.assertEqual(response.status_code, 400)
        data = response.json()

        self.assertIn('country', data)
        self.assertEqual(data['country'], ['This field is required.'])

    @patch('register.api.views.user.requests.get')
    @patch('register.api.views.user.HasAPIKey.has_permission')
    def test_post__external_api_error(self, mock_perms, mock_external):
        mock_perms.return_value = True
        external_response = Mock(**{
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'json.return_value': {'Oops, something wrong here'}
        })

        mock_external.return_value = external_response

        response = self.client.post(
            self.url,
            data={
                'first_name': 'Chris',
                'last_name': 'Bartlett',
                'email': 'chris@test.com',
                'country': 'GB'
            }
        )

        self.assertEqual(response.status_code, 502)
        data = response.json()
        self.assertEqual(data, ['Oops, something wrong here'])
        mock_external.assert_called_once_with(
            UserAPIView.price_api_url,
            params={'int_country_code': 'GB'}
        )

    @patch('register.api.views.user.requests.get')
    @patch('register.api.views.user.HasAPIKey.has_permission')
    def test_post__success(self, mock_perms, mock_external):
        mock_perms.return_value = True
        external_response = Mock(**{
            'status_code': status.HTTP_200_OK,
            'json.return_value': {'data': self.price_info}
        })
        mock_external.return_value = external_response

        response = self.client.post(
            self.url,
            data={
                'first_name': 'Chris',
                'last_name': 'Bartlett',
                'email': 'chris@test.com',
                'country': 'GB'
            }
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('first_name', data)
        self.assertEqual(data['first_name'], 'Chris')
        self.assertIn('last_name', data)
        self.assertEqual(data['last_name'], 'Bartlett')
        self.assertIn('email', data)
        self.assertEqual(data['email'], 'chris@test.com')
        self.assertIn('country', data)
        self.assertEqual(data['country'], 'GB')
        self.assertIn('price_info', data)
        self.assertEqual(data['price_info'], self.price_info)
        mock_external.assert_called_once_with(
            UserAPIView.price_api_url,
            params={'int_country_code': 'GB'}
        )
