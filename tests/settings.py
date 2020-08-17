#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division


class DisableMigrations(object):
    """
    Django-cms disables all migrations when they run their tests.
    It would be better to not do it. Right now we are forced to disable our
    migrations because we inherit one of our models from django-cms.
    The error in question is due to an incompability of sqlite3 and
    with atomic transactions.

    Error: "django.db.utils.NotSupportedError: Renaming the 'cms_title' table while in a
    transaction is not supported on SQLite because it would break referential integrity.
    Try adding `atomic = False` to the Migration class.
    """
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


HELPER_SETTINGS = {
    'MIDDLEWARE': [
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
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
    'MIGRATION_MODULES': DisableMigrations(),
}


def run():
    from djangocms_helper import runner
    runner.cms('aldryn_redirects')


if __name__ == '__main__':
    run()
