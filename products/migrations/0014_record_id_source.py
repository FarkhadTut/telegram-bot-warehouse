# Generated by Django 4.0.4 on 2022-06-21 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_remove_record_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='id_source',
            field=models.CharField(default=0, max_length=4096),
            preserve_default=False,
        ),
    ]
