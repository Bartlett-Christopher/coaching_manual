# -*- coding: utf-8 -*-
"""
.. module:: register.api.urls
   :synopsis: Register API urls

.. moduleauthor:: Chris Bartlett
"""
from django.conf.urls import url

from register.api.views import UserAPIView

urlpatterns = [
    url('user/', UserAPIView.as_view(), name='user')
]
