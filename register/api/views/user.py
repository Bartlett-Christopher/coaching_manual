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

from register.api.serializers import UserSerializer


class UserAPIView(APIView):
    """User model API handler."""
    price_api_url = \
        'https://us-central1-development-1300.cloudfunctions.net/' \
        'BETechnicalTest'

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
            params={'int_country_code': serializer.data['country']},
        )

        if price_response.status_code != 200:
            return Response(
                price_response.json(),
                status=status.HTTP_502_BAD_GATEWAY
            )

        price_info = price_response.json()
        serializer.save(price_info=price_info['data'])

        response_data = {'price_info': price_info['data']}
        response_data.update(serializer.data)
        return Response(response_data)
