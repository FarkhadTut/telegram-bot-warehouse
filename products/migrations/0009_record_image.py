# Generated by Django 4.0.5 on 2022-06-19 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_remove_identifier_question_ru_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='image',
            field=models.CharField(blank=True, max_length=4096, null=True),
        ),
    ]
