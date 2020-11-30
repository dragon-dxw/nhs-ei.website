# Generated by Django 3.1.2 on 2020-10-13 21:06

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_auto_20201006_1212'),
        ('posts', '0004_auto_20201013_0952'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='categories',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, related_name='categories', to='categories.Category'),
        ),
    ]