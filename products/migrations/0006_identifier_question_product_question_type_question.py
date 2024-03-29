# Generated by Django 4.0.5 on 2022-06-19 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_type_poll_alter_record_units'),
    ]

    operations = [
        migrations.AddField(
            model_name='identifier',
            name='question',
            field=models.TextField(default=0, max_length=4096),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='question',
            field=models.TextField(default=90, max_length=4096),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='type',
            name='question',
            field=models.TextField(blank=True, max_length=4096, null=True),
        ),
    ]
