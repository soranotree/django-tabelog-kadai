# Generated by Django 4.2.16 on 2024-10-11 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0023_reservation_is_dependent'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='rate_star',
            field=models.FloatField(default=0.0, verbose_name='レートスター'),
        ),
    ]
