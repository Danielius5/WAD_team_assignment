# Generated by Django 3.1.7 on 2021-04-06 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booklists', '0003_auto_20210406_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.ImageField(default='/book_covers/picturenotfound.jpg', upload_to='book_covers'),
        ),
    ]
