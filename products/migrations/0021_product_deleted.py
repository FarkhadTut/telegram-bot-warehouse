# Generated by Django 4.0.4 on 2022-08-11 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0020_identifier_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='deleted',
            field=models.BooleanField(default=1),
        ),
    ]
