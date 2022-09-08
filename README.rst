** This app is the Fidelity fork of the Divio app aldryn-redirects **

Divio dropped support for the original app, this is a fork named aldryn-redirects-fil, which diverges from the original
to bring in django 3.2 support, as well as other FIL specific functionality. To simplify the releases, the app version
has been set to 1.0.0 for the release after the divergence.

################
Aldryn Redirects
################

This is a modified version of Django's ``django.contrib.redirects`` app that
supports language-dependent target URLs, using ``django-parler``.

This is useful for cases in which another middleware strips the language
prefix from the URL, like django CMS. It allows to define different urls to
redirect to, depending on the user's language.

************
Installation
************

Aldryn Platform Users
#####################

To install the addon on Aldryn, all you need to do is follow this
`installation link <https://control.aldryn.com/control/?select_project_for_addon=aldryn-redirects>`_
on the Aldryn Marketplace and follow the instructions.

Manually you can:

#. Choose a site you want to install the Addon to from the dashboard.
#. Go to Apps > Install App
#. Click Install next to the Aldryn Redirects app.
#. Redeploy the site.


Manual Installation
###################


```bash
pip install aldryn-redirects
```

Follow the `setup instructions for django-parler <http://django-parler.readthedocs.org/>`_.

```python

# settings.py

INSTALLED_APPS += [
    'parler',
    'aldryn_redirects'
]

# add the middleware somewhere near the top of MIDDLEWARE

MIDDLEWARE.insert(
    0, 'aldryn_redirects.middleware.RedirectFallbackMiddleware')
```
