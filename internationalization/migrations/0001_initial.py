# Generated by Django 4.2.5 on 2023-09-17 08:00

import django.db.models.deletion
from django.db import migrations, models

import internationalization.models.abstract.main_fields


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Script',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('added', models.DateTimeField()),
                ('deprecated', models.DateTimeField(null=True)),
                ('description',
                 models.JSONField(default=list,
                                  validators=[internationalization.models.abstract.main_fields._validator])),
                ('subtag', models.CharField(max_length=4)),
                ('comments', models.TextField()),
                ('preferred_value',
                 models.ForeignKey(null=True,
                                   on_delete=django.db.models.deletion.RESTRICT,
                                   to='internationalization.script')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
