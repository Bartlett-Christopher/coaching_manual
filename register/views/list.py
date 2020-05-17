# -*- coding: utf-8 -*-
"""
.. module:: register.views.list
   :synopsis: View to list all registered users

.. moduleauthor:: Chris Bartlett
"""
import json

import requests

from django.urls import reverse
from django.views.generic import TemplateView


class UserListView(TemplateView):
    """User list view."""
    template_name = 'register/list.html'

    def get(self, request, *args, **kwargs):
        """GET handler"""
        url = request.build_absolute_uri(reverse('api:user'))
        response = requests.get(url)

        if response.status_code != 200:
            return self.render_to_response({})

        context = self.get_context_data()

        users = response.json()
        for user in users:
            user['price_info'] = json.loads(user['price_info'])

        context['users'] = users
        return self.render_to_response(context)
