# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-25 18:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0018_auto_20190525_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='reply',
            field=models.BooleanField(default=False, verbose_name='Is a Reply ?'),
        ),
    ]
