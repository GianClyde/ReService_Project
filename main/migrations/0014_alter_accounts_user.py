# Generated by Django 4.2 on 2023-05-22 13:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_remove_services_zipcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
