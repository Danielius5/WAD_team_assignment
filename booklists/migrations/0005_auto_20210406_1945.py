# Generated by Django 3.1.7 on 2021-04-06 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booklists', '0004_auto_20210406_1717'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created']},
        ),
    ]
