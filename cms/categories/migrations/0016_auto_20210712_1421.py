# Generated by Django 3.1.13 on 2021-07-12 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blogs", "0007_remove_blogindexpage_sub_site_categories"),
        ("categories", "0015_remove_publicationtype_source"),
        ("posts", "0011_remove_postindexpage_sub_site_categories"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="category",
            name="sub_site",
        ),
        migrations.DeleteModel(
            name="CategorySubSite",
        ),
    ]