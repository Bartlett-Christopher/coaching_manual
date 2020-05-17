# -*- coding: utf-8 -*-
"""
.. module:: register.views.signup
   :synopsis: View for user signup

.. moduleauthor:: Chris Bartlett
"""
from django.shortcuts import render
from django.views.generic import TemplateView

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

    def get_price_information(self, country):
        """
        Call an external API to get the current price information for the
        supplied ISO country code.

        :param country: 2 character ISO country code
        :type country: str
        :return: price information for supplied country
        :rtype: dict
        """
        # TODO: call external API
        return {'data': []}

    def get(self, request, *args, **kwargs):
        """GET handler"""
        context = self.get_context(request, **kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        """POST handler"""
        # collect and check POST data
        form = self.get_form(request)

        if not form.is_valid():
            context = self.get_context(request)
            return self.render_to_response(context)

        # call external API
        price_info = self.get_price_information(form.cleaned_data['country'])

        if not price_info:
            context = self.get_context(request)
            context['api_error'] = True
            return self.render_to_response(context)

        # save data
        user = form.instance
        user.price_info = price_info
        user.save()

        # return response
        return render(request, 'register/complete.html', form.cleaned_data)
