# Generated by Django 5.1.2 on 2024-10-28 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0003_alter_publication_image_commentaire'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='titre',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]