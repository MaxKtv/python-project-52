# Generated by Django 5.1.4 on 2024-12-19 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statuses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='status',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='status',
            unique_together=set(),
        ),
    ]
