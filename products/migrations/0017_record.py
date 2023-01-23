# Generated by Django 4.0.4 on 2022-06-21 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_delete_record'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_id', models.IntegerField()),
                ('question_id', models.IntegerField()),
                ('response_type', models.CharField(max_length=512)),
                ('response_id_source', models.CharField(blank=True, max_length=512)),
            ],
        ),
    ]
