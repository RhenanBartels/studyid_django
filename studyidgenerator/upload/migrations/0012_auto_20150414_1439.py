# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0011_auto_20150414_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='date',
            field=models.DateField(auto_now_add=True, verbose_name=b'Date'),
            preserve_default=True,
        ),
    ]
