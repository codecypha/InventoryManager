# Generated by Django 3.2.9 on 2021-11-06 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imanager', '0016_alter_itemrequest_quantity_requested'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemrequest',
            name='category',
        ),
        migrations.AlterField(
            model_name='itemrequest',
            name='item_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='itemrequest',
            name='quantity_requested',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='itemrequest',
            name='stage',
            field=models.CharField(default='pending', max_length=30),
        ),
    ]
