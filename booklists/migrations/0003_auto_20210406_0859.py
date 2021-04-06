# Generated by Django 3.1.7 on 2021-04-06 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booklists', '0002_auto_20210405_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='average_rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='book',
            name='ratings_count',
            field=models.IntegerField(default=0),
        ),
    ]