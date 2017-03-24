# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-24 07:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hashez', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='badfiles',
            name='fileSet',
        ),
        migrations.RemoveField(
            model_name='event',
            name='badFiles',
        ),
        migrations.AddField(
            model_name='badfiles',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hashez.Event'),
        ),
        migrations.AlterField(
            model_name='event',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hashez.Client'),
        ),
    ]
