# Generated by Django 4.2.5 on 2023-09-17 08:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('internationalization', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='script',
            name='source_data',
            field=models.URLField(null=True),
        ),
    ]
