# Generated by Django 3.1.6 on 2021-02-11 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
