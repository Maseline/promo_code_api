# Generated by Django 2.0.6 on 2018-06-17 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promoCodeApi', '0002_auto_20180617_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promocode',
            name='date_created',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='expiry_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='radius_in_km',
            field=models.FloatField(),
        ),
    ]
