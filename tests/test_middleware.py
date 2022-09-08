from __future__ import division, print_function

from django.contrib.sites.models import Site
from django.test import TestCase
from django.test.client import RequestFactory

from aldryn_redirects.middleware import RedirectFallbackMiddleware
from aldryn_redirects.models import StaticRedirect


class RedirectFallbackMiddlewareTestCase(TestCase):
    def setUp(self, *args, **kwargs):
        super(RedirectFallbackMiddlewareTestCase, self).setUp(*args, **kwargs)

        self.request = RequestFactory().get('http://example.com/path?query1=param1')
        self.site = Site.objects.get()

    def test_redirect_found(self):
        redirect = StaticRedirect.objects.create(inbound_route='/path', outbound_route='/dest?keep=this')
        redirect.sites.add(self.site)
        redirect.query_params.create(key='query1', value='param1')

        response = RedirectFallbackMiddleware().process_request(self.request)

        self.assertEquals(response.status_code, 301)
        self.assertEquals(response.url, 'http://example.com/dest?keep=this')

    def test_redirect_found_from_root(self):
        redirect = StaticRedirect.objects.create(inbound_route='/', outbound_route='/dest?keep=this')
        redirect.sites.add(self.site)
        redirect.query_params.create(key='query1', value='param1')
        request_from_root = RequestFactory().get('http://example.com/?query1=param1')

        response = RedirectFallbackMiddleware().process_request(request_from_root)

        self.assertEquals(response.status_code, 301)
        self.assertEquals(response.url, 'http://example.com/dest?keep=this')

    def test_redirect_not_found(self):
        self.assertIsNone(RedirectFallbackMiddleware().process_request(self.request))
