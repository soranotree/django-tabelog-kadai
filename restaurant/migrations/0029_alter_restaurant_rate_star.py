# Generated by Django 4.2.16 on 2024-10-20 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0028_alter_menu_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='rate_star',
            field=models.FloatField(blank=True, default=0.0, null=True, verbose_name='レートスター'),
        ),
    ]