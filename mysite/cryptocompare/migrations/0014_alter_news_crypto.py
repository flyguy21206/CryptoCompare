# Generated by Django 3.2.2 on 2021-10-20 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptocompare', '0013_auto_20211019_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='crypto',
            field=models.ManyToManyField(to='cryptocompare.Crypto'),
        ),
    ]