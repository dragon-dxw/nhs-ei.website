# Generated by Django 3.1.1 on 2020-11-29 22:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('wagtailcore', '0052_pagelogentry'),
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('wagtailnhsukfrontendsettings', '0005_remove_emergency_alert'),
        ('home', '0008_merge_20201129_1742'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DemoPage',
        ),
    ]