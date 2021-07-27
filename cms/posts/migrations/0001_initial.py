# Generated by Django 3.1.12 on 2021-07-22 12:05

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0062_comment_models_and_pagesubscription'),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('categorypage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='categories.categorypage')),
                ('body', wagtail.core.fields.RichTextField(blank=True)),
                ('wp_id', models.PositiveIntegerField(null=True)),
                ('source', models.CharField(max_length=100, null=True)),
                ('wp_slug', models.TextField(blank=True, null=True)),
                ('wp_link', models.TextField(blank=True, null=True)),
                ('author', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('categories.categorypage',),
        ),
        migrations.CreateModel(
            name='PostIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.core.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
