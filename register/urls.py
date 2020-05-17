# -*- coding: utf-8 -*-
"""
  :synopsis: Urls for the register app.

.. module: register.urls
.. author: Chris Bartlett
"""
from django.urls import path

from register.views import UserListView
from register.views import SignUpView


urlpatterns = [
    path('', SignUpView.as_view(), name='signup'),
    path('list/', UserListView.as_view(), name='list')
]
