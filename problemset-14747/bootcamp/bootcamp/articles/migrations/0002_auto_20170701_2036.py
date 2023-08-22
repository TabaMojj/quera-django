# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-07-01 20:36
from __future__ import unicode_literals

# import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        # migrations.AlterField(
        #     model_name='article',
        #     name='slug',
        #     # field=autoslug.fields.AutoSlugField(default='null value', editable=False, populate_from='title'),
        #     preserve_default=False,
        # ),
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[('D', 'Draft'), ('P', 'Published')], default='D', max_length=1),
        ),
    ]
