# -*- coding: utf-8 -*-
"""
.. module:: register.api.utils.make_request
   :synopsis: Utility function to make request to register API

.. moduleauthor:: Chris Bartlett
"""
import requests

from django.conf import settings


def make_request(url, method, data=None):
    """
    Utility function to make requests to register API.

    :param url: register API url
    :type url: str
    :param method: request method
    :type method: str
    :param data: request data or none
    :type data: dict or NoneType
    :return: response from register API
    :rtype: rest_framework.response.Response
    """
    kwargs = {
        'url': url,
        'headers': {
            'Authorization': 'Api-Key {}'.format(settings.API_KEY),
            'Content-Type': 'application/json',
        }
    }

    if data:
        kwargs['data'] = data

    handler = getattr(requests, method.lower())

    return handler(**kwargs)
