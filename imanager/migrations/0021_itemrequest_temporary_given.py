# Generated by Django 3.2.9 on 2021-11-14 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imanager', '0020_auto_20211112_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemrequest',
            name='temporary_given',
            field=models.CharField(blank=True, default=0, max_length=150),
        ),
    ]