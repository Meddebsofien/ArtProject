# Generated by Django 5.1.2 on 2024-10-26 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
