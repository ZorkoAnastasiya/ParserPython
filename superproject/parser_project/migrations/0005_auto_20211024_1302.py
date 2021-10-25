# Generated by Django 3.2.7 on 2021-10-24 10:02
from django.db import migrations, models


def add_resources_name(apps, schema_editor):
    resources_name = ['Sputnik Беларусь', 'Lenta Новости', 'Euronews', 'Другие ресурсы']
    Resources = apps.get_model('parser_project', 'Resources')
    for name in resources_name:
        resource_title = Resources(title = name)
        resource_title.save()


class Migration(migrations.Migration):

    dependencies = [
        ('parser_project', '0004_auto_20211023_1652'),
    ]

    operations = [
        migrations.RunPython(add_resources_name),
    ]