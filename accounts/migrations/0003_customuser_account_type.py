# Generated by Django 4.2 on 2024-09-15 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customuser_expiry'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='account_type',
            field=models.IntegerField(blank=True, choices=[(0, '選択してください'), (1, 'ユーザー会員'), (2, '店舗オーナー'), (3, 'システム管理者')], default=0, null=True, verbose_name='アカウント種別'),
        ),
    ]