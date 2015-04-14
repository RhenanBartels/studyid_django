# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0003_auto_20150414_0619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='owner',
            field=models.ForeignKey(default=12345, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
