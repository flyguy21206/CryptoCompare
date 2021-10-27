# Generated by Django 3.2.2 on 2021-10-20 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptocompare', '0011_auto_20211013_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='headline',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='article',
            field=models.URLField(blank=True, null=True),
        ),
    ]
