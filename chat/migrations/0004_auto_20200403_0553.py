# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2020-04-03 05:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20200402_0410'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='minimum',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='games_minimum', to='chat.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='next_to_bid',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='games_next_to_bid', to='chat.Player'),
        ),
        migrations.AddField(
            model_name='room',
            name='owner',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]
