# Generated by Django 4.2 on 2023-05-18 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_remove_driverpayment_user_driverpayment_driver'),
    ]

    operations = [
        migrations.AddField(
            model_name='driverpayment',
            name='franchise',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.franchise'),
        ),
    ]
