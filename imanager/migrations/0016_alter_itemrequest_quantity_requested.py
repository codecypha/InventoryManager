# Generated by Django 3.2.9 on 2021-11-06 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imanager', '0015_auto_20211106_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemrequest',
            name='quantity_requested',
            field=models.IntegerField(),
        ),
    ]
