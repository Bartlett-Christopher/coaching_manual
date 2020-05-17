# -*- coding: utf-8 -*-
"""
.. module:: register.api.views.user
   :synopsis: API handler for User model.

.. moduleauthor:: Chris Bartlett
"""
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from register.api.serializers import UserSerializer


class UserAPIView(APIView):
    """User model API handler."""

    def post(self, request, *args, **kwargs):
        """Create a new User."""
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # call external API
        price_info = {}

        serializer.save(price_info=price_info)

        response_data = {'price_info': price_info}
        response_data.update(serializer.data)
        return Response(response_data)
