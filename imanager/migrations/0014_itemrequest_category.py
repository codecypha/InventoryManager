# Generated by Django 3.2.9 on 2021-11-06 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imanager', '0013_alter_itemrequest_quantity_requested'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemrequest',
            name='category',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]