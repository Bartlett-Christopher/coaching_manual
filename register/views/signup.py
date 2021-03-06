# -*- coding: utf-8 -*-
"""
.. module:: register.views.signup
   :synopsis: View for user signup

.. moduleauthor:: Chris Bartlett
"""
import json

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from register.api.utils.make_request import make_request
from register.forms import SignUpForm


class SignUpView(TemplateView):
    """User registration view."""

    template_name = 'register/signup.html'

    def get_context(self, request, **kwargs):
        """
        Construct and return the template context.

        :param request: incoming Http request
        :type request: django.http.HttpRequest
        :return: the template context
        :rtype: dict
        """
        context = self.get_context_data(**kwargs)
        context['form'] = self.get_form(request)
        return context

    def get_form(self, request):
        """
        Return the SignUp form.

        If incoming request is POST then load form with POST data.

        :param: request: incoming Http request
        :type request: django.http.HttpRequest
        :return: the SignUpForm
        :rtype: register.forms.signup.SignUpForm
        """
        if request.method.upper() == 'POST':
            return SignUpForm(data=request.POST)

        return SignUpForm()

    def get(self, request, *args, **kwargs):
        """GET handler"""
        context = self.get_context(request, **kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        """POST handler"""
        url = request.build_absolute_uri(reverse('api:user'))

        response = make_request(
            url=url,
            method='post',
            data=json.dumps(request.POST)
        )

        if response.status_code == 400:
            context = self.get_context(request)
            context['errors'] = response.json()
            return self.render_to_response(context)

        if response.status_code == 502:
            context = self.get_context(request)
            context['gateway_error'] = response.json()
            return self.render_to_response(context)

        return render(request, 'register/complete.html', response.json())
