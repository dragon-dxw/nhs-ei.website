import sys
import time
from cms.atlascasestudies.models import (
    AtlasCaseStudy,
    AtlasCaseStudyIndexPage,
    AtlasCaseStudySettingRelationship,
    AtlasCaseStudyRegionRelationship,
)

from cms.categories.models import (
    Category,
    Region,
    Setting,
    CategoryPageCategoryRelationship,
)
from wagtail.core.models import Page

from .importer_cls import Importer
import logging

logger = logging.getLogger("importer")


class AtlasCaseStudiesImporter(Importer):
    def __init__(self):
        atlas_case_studies = AtlasCaseStudy.objects.all()
        if atlas_case_studies:
            sys.stdout.write(
                "⚠️  Run delete_atlascasestudies before running this command\n"
            )
            sys.exit()

    def parse_results(self):
        atlas_case_studies = self.results
        home_page = Page.objects.filter(title="Home")[0]

        # we need categories to exist before importing atlas case studies
        categories = Category.objects.all()
        if not categories:
            sys.exit("\n😲Cannot continue... did you import the categories first?")

        # we need settings to exist before importing atlas case studies
        settings = Setting.objects.all()
        if not settings:
            sys.exit("\n😲Cannot continue... did you import the settings first?")

        # we need categories to exist before importing atlas case studies
        regions = Region.objects.all()
        if not regions:
            sys.exit("\n😲Cannot continue... did you import the regions first?")

        # make a atlas case study index page for the whole site, only one to exist ...
        # make a news index page if not already in place
        try:
            # a parent for all atlas case study pages
            atlas_case_study_index_page = AtlasCaseStudyIndexPage.objects.get(
                title="Atlas Case Study Items Base"
            )
        except Page.DoesNotExist:
            atlas_case_study_index_page = AtlasCaseStudyIndexPage(
                title="Atlas Case Study Items Base",
                body="theres a place here for some text",
                show_in_menus=True,
                slug="atlas-case-study-items-base",
            )
            home_page.add_child(instance=atlas_case_study_index_page)
            revision = atlas_case_study_index_page.save_revision()
            revision.publish()
            sys.stdout.write(".")

        for atlas_case_study in atlas_case_studies:

            first_published_at = atlas_case_study.get("date")
            last_published_at = atlas_case_study.get("modified")
            latest_revision_created_at = atlas_case_study.get("modified")
            page_title = atlas_case_study.get("title")
            if not page_title:
                page_title = "page has no title"
                logger.warn(
                    "Page with wp_id %s has no title", atlas_case_study.get("wp_id")
                )
            elif len(page_title) > 250:
                logger.warn("Long page_title, %s", page_title)

            obj = AtlasCaseStudy(
                title=page_title,
                body=atlas_case_study.get("content"),
                show_in_menus=True,
                wp_id=atlas_case_study.get("wp_id"),
                wp_slug=atlas_case_study.get("wp_slug"),
                wp_link=atlas_case_study.get("wp_link"),
            )
            atlas_case_study_index_page.add_child(instance=obj)
            rev = obj.save_revision()  # this needs to run here
            rev.publish()

            obj.first_published_at = first_published_at
            obj.last_published_at = last_published_at
            obj.latest_revision_created_at = latest_revision_created_at
            obj.save()
            rev.publish()
            sys.stdout.write(".")

            # add the categories as related many to many, found this needs to be after the save above
            # some categories are blank
            if not not atlas_case_study.get("categories"):
                category_ids = atlas_case_study.get("categories").split(" ")
                # list of category wp_id's
                for category in category_ids:
                    category_object = Category.objects.get(
                        source="categories",
                        wp_id=int(category),
                    )

                    CategoryPageCategoryRelationship.objects.create(
                        category_page=obj, category=category_object
                    )
                sys.stdout.write(".")

            # Tag the Atlas Case Studies as such.
            atlas_category, _ = Category.objects.get_or_create(
                name="Atlas Case Studies",
                slug="atlas-case-studies",
                description="Atlas of Shared Learning: Case Studies",
                wp_id=None,
                source=None,
            )
            CategoryPageCategoryRelationship.objects.create(
                category_page=obj, category=atlas_category
            )

            # add the settings as related many to many, found this needs to be after the save above
            # some settings are blank
            if not not atlas_case_study.get("settings"):
                settings = atlas_case_study.get("settings").split(
                    " "
                )  # list of setting wp_id's
                settings_objects = Setting.objects.filter(wp_id__in=settings)
                for setting in settings_objects:
                    rel = AtlasCaseStudySettingRelationship.objects.create(
                        atlas_case_study=obj, setting=setting
                    )
                sys.stdout.write(".")

            # add the regions as related many to many, found this needs to be after the save above
            # some regions are blank
            if not not atlas_case_study.get("regions"):
                regions = atlas_case_study.get("regions").split(
                    " "
                )  # list of category wp_id's

                regions_objects = Region.objects.filter(wp_id__in=regions)
                for region in regions_objects:
                    rel = AtlasCaseStudyRegionRelationship.objects.create(
                        atlas_case_study=obj, region=region
                    )
                sys.stdout.write(".")

        if self.next:
            time.sleep(self.sleep_between_fetches)
            self.fetch_url(self.next)
            self.parse_results()
        return AtlasCaseStudy.objects.count(), self.count
