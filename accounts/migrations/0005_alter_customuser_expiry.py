# Generated by Django 4.2 on 2024-09-18 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_customuser_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='expiry',
            field=models.CharField(blank=True, help_text='YYYY-MM形式で入力してください', max_length=7, null=True, verbose_name='カード有効期限'),
        ),
    ]
