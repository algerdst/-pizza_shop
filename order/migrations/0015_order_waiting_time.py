# Generated by Django 4.1.4 on 2023-02-22 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0014_alter_order_content"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="waiting_time",
            field=models.SmallIntegerField(default=0),
        ),
    ]
