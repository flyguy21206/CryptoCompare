# Generated by Django 3.2.2 on 2021-10-24 05:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cryptocompare', '0020_portfolio_image_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='portfolio',
            old_name='coin_name',
            new_name='name',
        ),
    ]
