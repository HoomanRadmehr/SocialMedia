# Generated by Django 3.1.5 on 2021-01-22 17:03

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
