# Generated by Django 4.2.5 on 2023-09-19 08:44

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('internationalization', '0005_alter_script_comments'),
    ]

    operations = [
        migrations.RenameField(
            model_name='script',
            old_name='preferred_value',
            new_name='preferred_value_script',
        ),
        migrations.RemoveField(
            model_name='language',
            name='preferred_value',
        ),
    ]
