# Generated by Django 3.2.9 on 2021-11-04 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imanager', '0004_auto_20211104_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=250),
        ),
    ]