# Generated by Django 4.2.5 on 2023-09-17 13:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('internationalization', '0003_languagescope_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='iso_639_1',
            field=models.CharField(max_length=2, unique=True),
        ),
        migrations.AlterField(
            model_name='language',
            name='iso_639_2',
            field=models.CharField(max_length=3, unique=True),
        ),
        migrations.AlterField(
            model_name='language',
            name='iso_639_3',
            field=models.CharField(max_length=3, unique=True),
        ),
        migrations.AlterField(
            model_name='language',
            name='iso_639_5',
            field=models.CharField(max_length=3, unique=True),
        ),
        migrations.AlterField(
            model_name='language',
            name='subtag',
            field=models.CharField(max_length=4, unique=True),
        ),
        migrations.AlterField(
            model_name='languagescope',
            name='description',
            field=models.TextField(unique=True),
        ),
        migrations.AlterField(
            model_name='script',
            name='subtag',
            field=models.CharField(max_length=4, unique=True),
        ),
    ]
