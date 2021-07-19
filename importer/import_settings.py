import sys
import time

from cms.categories.models import Setting
from django.core.management import call_command

from .importer_cls import Importer

# the indiators from wordpress aren't nice so map them to better titles
# SOURCES = {
#     'categories': 'NHS England & Improvement',
#     'categories-aac': 'Accelerated Access Collaborative',
#     'categories-commissioning': 'Commissioning',
#     'categories-coronavirus': 'Coronavirus',
#     'categories-greenernhs': 'Greener NHS',
#     'categories-improvement-hub': 'Improvement Hub',
#     'categories-non-executive-opportunities': 'Non-executive opportunities',
#     'categories-rightcare': 'Right Care',
# }


class SettingsImporter(Importer):
    def __init__(self):
        settings = Setting.objects.all()
        # category_sub_sites = CategorySubSite.objects.all()
        if settings:
            sys.stdout.write("⚠️  Run delete_settings before running this command\n")
            sys.exit()

    def parse_results(self):
        settings = self.results
        for r in settings:
            setting = Setting(
                name=r.get("name"),
                slug=r.get("slug"),
                description=r.get("description"),
                wp_id=r.get("wp_id"),
                # source = r.get('source'),
                # sub_site = category_sub_site
            )
            setting.save()
            sys.stdout.write(".")

        if self.next:
            time.sleep(self.sleep_between_fetches)
            self.fetch_url(self.next)
            self.parse_results()
        return Setting.objects.count(), self.count
