# Generated by Django 4.2 on 2023-05-22 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_serviceroute'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='zipcode',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
