from django.contrib import admin
from django.shortcuts import reverse

from cms.models import Site
from cms.test_utils.testcases import CMSTestCase

from aldryn_redirects.models import StaticRedirect

from bs4 import BeautifulSoup


class StaticRedirectRootTestCase(CMSTestCase):
    def setUp(self):
        self.user = super().get_superuser()
        self.site = admin.AdminSite()
        self.add_url = reverse("admin:aldryn_redirects_staticredirect_add")

    def test_static_redirect_allows_root(self):
        add_url = reverse("admin:aldryn_redirects_staticredirect_add")
        redirect_data = {
            "sites": [Site.objects.first().id, ],
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
        expected_inbound = redirect_data["inbound_route"]
        expected_outbound = redirect_data["outbound_route"]
        expected_result = f'The Static Redirect “{expected_inbound} --> {expected_outbound}” was added successfully.'

        self.assertEqual(response.status_code, 200)
        self.assertIn(expected_result, result.text)
        self.assertEqual(StaticRedirect.objects.all().count(), 1)
