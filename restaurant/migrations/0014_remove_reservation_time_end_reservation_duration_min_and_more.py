# Generated by Django 4.2 on 2024-09-23 04:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0013_restaurant_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='time_end',
        ),
        migrations.AddField(
            model_name='reservation',
            name='duration_min',
            field=models.IntegerField(blank=True, null=True, verbose_name='制限時間（分）'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='dining_table',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='restaurant.diningtable', verbose_name='卓情報'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='time_start',
            field=models.TimeField(choices=[('', '選択してください'), ('12:00', '12:00'), ('13:00', '13:00'), ('14:00', '14:00'), ('15:00', '15:00'), ('18:00', '18:00'), ('19:00', '19:00'), ('20:00', '20:00'), ('21:00', '21:00'), ('22:00', '22:00')], default='', verbose_name='予約開始時間'),
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='メニュー名')),
                ('description', models.TextField(verbose_name='メニュー説明')),
                ('price', models.IntegerField(verbose_name='価格（一名分）')),
                ('available_from', models.TimeField(verbose_name='提供開始時間')),
                ('available_end', models.TimeField(verbose_name='提供終了時間')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='', verbose_name='写真')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurant')),
            ],
        ),
        migrations.AddField(
            model_name='reservation',
            name='menu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='restaurant.menu', verbose_name='メニュー'),
        ),
    ]
