# Generated by Django 5.1.4 on 2024-12-16 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0003_alter_label_options_alter_label_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterUniqueTogether(
            name='label',
            unique_together={('name',)},
        ),
    ]
