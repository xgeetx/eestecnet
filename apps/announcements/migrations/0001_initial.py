# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

import common.util


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('confirmable_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='common.Confirmable')),
                ('name', models.CharField(max_length=300)),
                ('description', models.TextField(max_length=300)),
            ],
            options={
                'abstract': False,
            },
            bases=('common.confirmable', common.util.Reversable),
        ),
        migrations.CreateModel(
            name='CareerOffer',
            fields=[
                ('announcement_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='announcements.Announcement')),
            ],
            options={
                'abstract': False,
            },
            bases=('announcements.announcement',),
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('announcement_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='announcements.Announcement')),
            ],
            options={
                'abstract': False,
            },
            bases=('announcements.announcement',),
        ),
        migrations.AddField(
            model_name='announcement',
            name='owner',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
