# Generated by Django 4.0.4 on 2022-06-20 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_record_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='index',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
