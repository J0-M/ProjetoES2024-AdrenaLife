# Generated by Django 5.1.4 on 2025-02-25 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_adrenalife', '0009_alter_evento_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='valor',
            field=models.FloatField(),
        ),
    ]
