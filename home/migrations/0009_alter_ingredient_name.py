# Generated by Django 4.1.4 on 2023-01-30 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0008_rename_consist_ingredient"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredient",
            name="name",
            field=models.CharField(max_length=20),
        ),
    ]
