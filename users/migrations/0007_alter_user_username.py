# Generated by Django 4.1.4 on 2023-02-06 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_alter_user_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
