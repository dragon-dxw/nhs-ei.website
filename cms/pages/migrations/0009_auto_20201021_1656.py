# Generated by Django 3.1.2 on 2020-10-21 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_auto_20201021_1630'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basepage',
            old_name='template',
            new_name='wp_template',
        ),
    ]