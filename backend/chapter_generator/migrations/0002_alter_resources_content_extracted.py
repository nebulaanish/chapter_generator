# Generated by Django 5.1.3 on 2024-11-23 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chapter_generator", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="resources",
            name="content_extracted",
            field=models.TextField(null=True),
        ),
    ]
