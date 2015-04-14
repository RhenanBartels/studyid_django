# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0006_auto_20150414_0652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True),
            preserve_default=True,
        ),
    ]
