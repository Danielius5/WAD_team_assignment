# Generated by Django 3.2 on 2021-04-07 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booklists', '0007_auto_20210406_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='slug',
            field=models.SlugField(default='', null=True, unique=True),
        ),
    ]