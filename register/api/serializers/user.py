# -*- coding: utf-8 -*-
"""
.. module:: register.api.serializers.user
   :synopsis: User serializer for the API app.

.. moduleauthor:: Chris Bartlett
"""
from rest_framework import serializers

from register.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    class Meta:
        """User serializer Metadata."""
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'country',
        )
