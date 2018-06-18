# Generated by Django 2.0.6 on 2018-06-15 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255)),
                ('value', models.IntegerField()),
                ('radius', models.IntegerField()),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Deactivated', 'Deactivated')], default='Active', max_length=50)),
                ('expiry_date', models.DateTimeField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('venue_name', models.CharField(max_length=255)),
            ],
        ),
    ]
