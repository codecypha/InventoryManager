# Generated by Django 3.2.9 on 2021-11-16 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imanager', '0027_alter_items_pending_approval'),
    ]

    operations = [
        migrations.AddField(
            model_name='managerapproval',
            name='decision',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
