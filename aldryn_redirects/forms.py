from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from tablib import Dataset

from .importers import RedirectImporter, StaticRedirectImporter
from .models import StaticRedirect


class RedirectsImportForm(forms.Form):
    importer_class = RedirectImporter

    csv_file = forms.FileField(label=_('csv file'), required=True)

    def __init__(self, *args, **kwargs):
        super(RedirectsImportForm, self).__init__(*args, **kwargs)
        self.importer = self.importer_class()

    def clean_csv_file(self, *args, **kwargs):
        csv_file = self.cleaned_data['csv_file']
        csv_file.seek(0)
        dataset = Dataset().load(csv_file.read().decode('utf-8'), format='csv')

        for idx, row in enumerate(dataset, start=2):
            try:
                self.importer.validate_row(row)
            except ValidationError as e:
                raise forms.ValidationError('Line {}: {}'.format(idx, '\n'.join(e.messages)))

        return csv_file

    def do_import(self):
        csv_file = self.cleaned_data['csv_file']
        csv_file.seek(0)
        dataset = Dataset().load(csv_file.read().decode('utf-8'), format='csv')
        self.importer.import_from_dataset(dataset)


class StaticRedirectsImportForm(RedirectsImportForm):
    importer_class = StaticRedirectImporter


class StaticRedirectForm(forms.ModelForm):

    def clean(self):
        """
        Adds validation to ensure that a StaticRedirect is unique between sites and the inbound_route
        """
        cleaned_data = super().clean()
        sites = cleaned_data.get("sites")
        inbound_route = cleaned_data.get("inbound_route")

        existing_redirects = StaticRedirect.objects.filter(sites__in=sites, inbound_route=inbound_route).distinct()
        if not existing_redirects:
            return cleaned_data

        other_redirects = existing_redirects.exclude(pk=self.instance.pk).distinct()
        if not other_redirects:
            return cleaned_data

        sites = ", ".join(list(other_redirects.values_list("sites__domain", flat=True)))
        raise ValidationError(f"Redirect already exists from '{inbound_route}' and the selected sites: {sites}")

    class Meta:
        model = StaticRedirect
        fields = ["sites", "inbound_route", "outbound_route"]
