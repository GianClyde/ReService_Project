# Generated by Django 4.2 on 2023-05-22 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_services_zipcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='services',
            name='zipcode',
        ),
    ]
