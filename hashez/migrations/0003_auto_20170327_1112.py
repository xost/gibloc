# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-27 08:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hashez', '0002_auto_20170324_1033'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docNo', models.IntegerField()),
                ('registred', models.DateTimeField(auto_now_add=True)),
                ('title', models.TextField()),
                ('reason', models.TextField()),
                ('action', models.TextField()),
                ('badFiles', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hashez.BadFiles')),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='eventType',
            field=models.CharField(choices=[('CHECK', 'CHECK'), ('UPDATE', 'UPDATE'), ('NEWCLIENT', 'NEWCLIENT'), ('NEWFILESET', 'NEWFILESET')], max_length=32),
        ),
        migrations.AddField(
            model_name='comment',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hashez.Event'),
        ),
        migrations.AddField(
            model_name='comment',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hashez_comment_person', to=settings.AUTH_USER_MODEL),
        ),
    ]
