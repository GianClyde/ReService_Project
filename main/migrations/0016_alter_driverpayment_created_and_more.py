# Generated by Django 4.2 on 2023-05-22 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_accounts_reservation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverpayment',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='reservation_status',
            field=models.CharField(choices=[('PENDING', 'pending'), ('SUCCESSFULL', 'successfull'), ('DECLINED', 'declined'), ('CANCELED', 'canceled')], default='PENDING', max_length=100),
        ),
    ]
