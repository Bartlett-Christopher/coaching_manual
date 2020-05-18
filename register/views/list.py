# -*- coding: utf-8 -*-
"""
.. module:: register.views.list
   :synopsis: View to list all registered users

.. moduleauthor:: Chris Bartlett
"""
import json

from django.urls import reverse
from django.views.generic import TemplateView

from register.api.utils.make_request import make_request


class UserListView(TemplateView):
    """User list view."""
    template_name = 'register/list.html'

    def get(self, request, *args, **kwargs):
        """GET handler"""
        url = request.build_absolute_uri(reverse('api:user'))

        response = make_request(url, method='get')

        if response.status_code != 200:
            return self.render_to_response({})

        context = self.get_context_data()

        context['users'] = response.json()
        return self.render_to_response(context)
