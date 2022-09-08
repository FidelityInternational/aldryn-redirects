import re

from django.shortcuts import reverse

from cms.models import Site
from cms.test_utils.testcases import CMSTestCase

from aldryn_redirects.models import Redirect, StaticRedirect

from bs4 import BeautifulSoup


class AdminRedirectRootTestCase(CMSTestCase):
    def setUp(self):
        self.user = super().get_superuser()
        self.site = Site.objects.first()
        self.add_url = reverse("admin:aldryn_redirects_staticredirect_add")

    def decode_fancy_quotes(self, string):
        return re.sub(u'[\u201c\u201d]', '"', string)

    def test_static_redirect_allows_root(self):
        add_url = reverse("admin:aldryn_redirects_staticredirect_add")
        redirect_data = {
            "sites": [self.site.id, ],
            "inbound_route": "/",
            "outbound_route": "/test-page",
            'query_params-TOTAL_FORMS': '1',
            'query_params-INITIAL_FORMS': '0',
            'query_params-MAX_NUM_FORMS': '',
        }

        with self.login_user_context(self.user):
            response = self.client.post(add_url, data=redirect_data, follow=True)

        soup = BeautifulSoup(response.content, "html.parser")
        result = soup.find("li", {"class": "success"})
        decoded_result = self.decode_fancy_quotes(result.text)
        expected_inbound = redirect_data["inbound_route"]
        expected_outbound = redirect_data["outbound_route"]
        expected_result = f'The Static Redirect "{expected_inbound} --> {expected_outbound}" was added successfully.'

        self.assertEqual(response.status_code, 200)
        self.assertIn(expected_result, decoded_result)
        self.assertEqual(StaticRedirect.objects.all().count(), 1)

    def test_multilingual_redirect_allows_root(self):
        add_url = reverse("admin:aldryn_redirects_redirect_add")
        redirect_data = {
            "site": [self.site.id],
            "old_path": "/",
        }

        with self.login_user_context(self.user):
            response = self.client.post(add_url, data=redirect_data, follow=True)

        soup = BeautifulSoup(response.content, "html.parser")
        result = soup.find("li", {"class": "success"})
        decoded_result = self.decode_fancy_quotes(result.text)
        expected_inbound = redirect_data["old_path"]
        expected_result = f'The Multilanguage Redirect "{expected_inbound} ---> en:" was added successfully'

        self.assertEqual(response.status_code, 200)
        self.assertIn(expected_result, decoded_result)
        self.assertEqual(Redirect.objects.all().count(), 1)
