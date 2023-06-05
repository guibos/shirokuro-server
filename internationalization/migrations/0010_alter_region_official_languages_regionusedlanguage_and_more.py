# Generated by Django 4.2.5 on 2023-09-19 13:11

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('internationalization', '0009_region_regionofficiallanguage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='official_languages',
            field=models.ManyToManyField(related_name='RegionOfficialLanguage',
                                         through='internationalization.RegionOfficialLanguage',
                                         to='internationalization.language'),
        ),
        migrations.CreateModel(
            name='RegionUsedLanguage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language',
                 models.ForeignKey(on_delete=django.db.models.fields.related.ForeignKey,
                                   to='internationalization.language')),
                ('region',
                 models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='internationalization.region')),
            ],
        ),
        migrations.AddField(
            model_name='region',
            name='used_languages',
            field=models.ManyToManyField(related_name='RegionUsedLanguage',
                                         through='internationalization.RegionUsedLanguage',
                                         to='internationalization.language'),
        ),
        migrations.AddConstraint(
            model_name='regionusedlanguage',
            constraint=models.UniqueConstraint(fields=('region', 'language'), name='uq_region_used_language'),
        ),
    ]
