# -*- coding: utf-8 -*-
"""
.. module:: register.api.views.user
   :synopsis: API handler for User model.

.. moduleauthor:: Chris Bartlett
"""
import requests

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from register.api.serializers import UserSerializer
from register.models import User


class UserAPIView(APIView):
    """User model API handler."""

    permission_classes = [HasAPIKey]

    price_api_url = \
        'https://us-central1-development-1300.cloudfunctions.net/' \
        'BETechnicalTest'

    def get(self, request, *args, **kwargs):
        """Get all registered users."""
        users = User.objects.order_by('id')

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """Create a new User."""
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # call external API
        price_response = requests.get(
            self.price_api_url,
            params={'int_country_code': request.data['country']},
        )

        if price_response.status_code != 200:
            return Response(
                price_response.json(),
                status=status.HTTP_502_BAD_GATEWAY
            )

        price_data = price_response.json()
        active_plans = [plan for plan in price_data['data'] if plan['active']]
        serializer.save(price_info=active_plans)
        return Response(serializer.data)
