from cms.test_utils.testcases import CMSTestCase
from cms.utils import get_current_site
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError

from aldryn_redirects.forms import StaticRedirectForm
from aldryn_redirects.models import StaticRedirect


class StaticRedirectFormTestCase(CMSTestCase):

    def setUp(self):
        self.site = get_current_site()
        self.data = {
            "sites": [str(self.site.pk)],
            "inbound_route": "/test",
            "outbound_route": "http://example.com",
        }

    def test_when_no_existing_redirect(self):
        """
        When a redirect for the given site and inbound path does not exist, the form is valid
        """
        form = StaticRedirectForm(data=self.data)
        valid = form.is_valid()

        self.assertTrue(valid)

    def test_when_redirect_already_exists_for_site(self):
        """
        When a redirect for the given site and inbound path already exists, the form is valid
        """
        redirect = StaticRedirect.objects.create(
            inbound_route=self.data["inbound_route"], outbound_route=self.data["outbound_route"],
        )
        redirect.sites.add(self.site)

        form = StaticRedirectForm(data=self.data)
        valid = form.is_valid()

        self.assertFalse(valid)
        with self.assertRaises(ValidationError):
            form.clean()

    def test_when_redirect_exists_for_another_site(self):
        """
        When a redirect exists for another site and the given path, the form is valid
        """
        other_site = Site.objects.create(domain="anothersite.example.com")
        redirect = StaticRedirect.objects.create(
            inbound_route=self.data["inbound_route"], outbound_route=self.data["outbound_route"],
        )
        redirect.sites.add(other_site)

        form = StaticRedirectForm(data=self.data)
        valid = form.is_valid()

        self.assertTrue(valid)

    def test_clean_when_redirect_for_other_site_exists_for_one_site(self):
        """
        When a redirect exists for a site, and a new redirect is added for the same path and the sites including the
        same site, the form is not valid
        """
        other_site = Site.objects.create(domain="anothersite.example.com")
        redirect = StaticRedirect.objects.create(
            inbound_route=self.data["inbound_route"], outbound_route=self.data["outbound_route"],
        )
        redirect.sites.add(self.site)
        self.data["sites"] = [self.site.pk, other_site.pk]

        form = StaticRedirectForm(data=self.data)
        valid = form.is_valid()

        self.assertFalse(valid)
        with self.assertRaises(ValidationError):
            form.clean()

    def test_when_adding_new_site_to_existing_redirect(self):
        """
        When a redirect exists for a site, and that redirect is updated to add another site, the form is valid
        """
        other_site = Site.objects.create(domain="anothersite.example.com")
        redirect = StaticRedirect.objects.create(
            inbound_route=self.data["inbound_route"], outbound_route=self.data["outbound_route"],
        )
        self.data["sites"] = [self.site.pk, other_site.pk]

        form = StaticRedirectForm(data=self.data, instance=redirect)
        valid = form.is_valid()

        self.assertTrue(valid)
