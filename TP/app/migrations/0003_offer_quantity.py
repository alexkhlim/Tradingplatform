# Generated by Django 3.0.10 on 2020-11-04 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20201104_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='Current quantity'),
            preserve_default=False,
        ),
    ]
