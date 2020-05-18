# -*- coding: utf-8 -*-
"""
.. module:: register.api.exceptions
   :synopsis: Register API exceptions

.. moduleauthor:: Chris Bartlett
"""


class RegisterAPIException(Exception):
    """Generic Register API exception"""


class RegisterAPIDown(RegisterAPIException):
    """Raised when requests can't connect to the API"""
