# -*- coding: utf-8 -*-
"""
.. module:: register.views
   :synopsis: Views module for register app.

.. moduleauthor:: Chris Bartlett
"""
from register.views.list import UserListView
from register.views.signup import SignUpView

__all__ = [
    'UserListView',
    'SignUpView'
]
