# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-30 18:22
from __future__ import unicode_literals

import apps.models_view.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '0002_auto_20170530_1812'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('favored_by', models.ManyToManyField(related_name='favorite_quotes', to='login.Users')),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posted_quotes', to='login.Users')),
            ],
            bases=(models.Model, apps.models_view.models.ModelsViewMixin),
        ),
    ]
