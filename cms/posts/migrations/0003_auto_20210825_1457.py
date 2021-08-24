# Generated by Django 3.1.13 on 2021-08-25 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20210812_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='source',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='wp_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]