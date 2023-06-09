# Generated by Django 4.2 on 2023-05-21 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_remove_vehiclerequest_retirement_reason_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts',
            name='balance',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='driverpayment',
            name='driver',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.franchisedrivers'),
        ),
    ]
