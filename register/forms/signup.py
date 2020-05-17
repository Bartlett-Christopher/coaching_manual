# -*- coding: utf-8 -*-
"""
.. module:: register.forms.signup
   :synopsis: User signup form.

.. moduleauthor:: Chris Bartlett
"""
from django import forms

from register.models import User


class SignUpForm(forms.ModelForm):
    """User model SignUp form."""

    class Meta:
        """Signup form Metadata"""
        model = User
        exclude = (
            'price_info',
        )
