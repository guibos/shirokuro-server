# Generated by Django 4.2.5 on 2023-09-19 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('internationalization', '0006_rename_preferred_value_script_preferred_value_script_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='preferred_value_language',
            field=models.ForeignKey(null=True,
                                    on_delete=django.db.models.deletion.RESTRICT,
                                    to='internationalization.language'),
        ),
    ]
