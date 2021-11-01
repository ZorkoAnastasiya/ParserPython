# Generated by Django 3.2.7 on 2021-11-01 10:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('parser_project', '0007_alter_articles_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='owner',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='my_article',
                to=settings.AUTH_USER_MODEL),
        ),
    ]