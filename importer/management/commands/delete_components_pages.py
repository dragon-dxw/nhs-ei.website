import sys

from django.core.management.base import BaseCommand
from cms.pages.models import ComponentsPage


class Command(BaseCommand):
    help = "Deletes base pages (bulk action)"

    def handle(self, *args, **options):
        # depth order to start at deepest pages, seems sensible
        pages = ComponentsPage.objects.all().order_by("-depth")

        if not pages:
            sys.stdout.write("✅ Component Pages is empty\n")
        else:
            pages_length = pages.count()

            sys.stdout.write(
                "Component Pages to delete: {} this can take a while to complete\n".format(
                    pages_length
                )
            )

            for page in pages:
                page.delete()
                sys.stdout.write("-")

            sys.stdout.write("\n✅ Component Pages is now empty\n")
