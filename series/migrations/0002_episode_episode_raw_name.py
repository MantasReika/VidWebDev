# Generated by Django 2.0.7 on 2018-08-18 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='episode_raw_name',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]