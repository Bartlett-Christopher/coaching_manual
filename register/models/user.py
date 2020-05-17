# -*- coding: utf-8 -*-
"""
.. module:: register.models.user
   :synopsis: User model for register app.

.. moduleauthor:: Chris Bartlett
"""
from django.db import models

from django_countries.fields import CountryField
from django_extensions.db.fields.json import JSONField


class User(models.Model):
    """User model for register app."""

    first_name = models.CharField(
        verbose_name='First name',
        max_length=255
    )

    last_name = models.CharField(
        verbose_name='Last name',
        max_length=255
    )

    email = models.EmailField(
        verbose_name='Email',
    )

    country = CountryField(
        verbose_name='Country'
    )

    price_info = JSONField(
        verbose_name='Available price information',
        blank=True,
        null=True,
        default={}
    )
