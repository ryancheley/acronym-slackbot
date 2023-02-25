# Generated by Django 4.0.2 on 2022-02-16 14:18

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("acronyms", "0003_alter_acronym_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="acronym",
            name="create_by",
            field=models.CharField(default="rcheley", max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="acronym",
            name="create_date",
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
