# Generated by Django 4.2.5 on 2023-09-19 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internationalization', '0004_alter_language_iso_639_1_alter_language_iso_639_2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='script',
            name='comments',
            field=models.TextField(null=True),
        ),
    ]
