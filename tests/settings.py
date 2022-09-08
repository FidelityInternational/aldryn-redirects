#!/usr/bin/env python
from __future__ import division, print_function


HELPER_SETTINGS = {
    'MIDDLEWARE': [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'aldryn_redirects.middleware.RedirectFallbackMiddleware',
    ],
    'INSTALLED_APPS': [
    ],
    'ALLOWED_HOSTS': [
        'localhost'
    ],
    'CMS_LANGUAGES': {
        1: [{
            'code': 'en',
            'name': 'English',
        }],
        2: [{
            'code': 'pt-br',
            'name': 'Brazilian Portugues',
        }],
    },
    'LANGUAGE_CODE': 'en',
    'LANGUAGES': [
        ('en', 'English'),
        ('pt-br', 'Brazilian Portugues'),
    ],
    'SILENCED_SYSTEM_CHECKS': ['admin.E130'],
}


def run():
    from app_helper import runner
    runner.cms('aldryn_redirects')


if __name__ == '__main__':
    run()
