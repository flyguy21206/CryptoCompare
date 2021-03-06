# Generated by Django 3.2.7 on 2021-10-13 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cryptocompare', '0010_alter_crypto_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.URLField(null=True)),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('crypto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news', to='cryptocompare.crypto')),
            ],
            options={
                'verbose_name_plural': 'News',
                'ordering': ['date_added'],
            },
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
