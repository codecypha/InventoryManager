# Generated by Django 3.2.9 on 2021-11-16 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imanager', '0026_auto_20211114_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='pending_approval',
            field=models.CharField(default=0, max_length=250),
        ),
    ]
