# Generated by Django 4.0.2 on 2022-02-16 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("acronyms", "0005_acronym_approved"),
    ]

    operations = [
        migrations.AlterField(
            model_name="acronym",
            name="approved",
            field=models.BooleanField(),
        ),
    ]