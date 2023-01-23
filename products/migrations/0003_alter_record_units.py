# Generated by Django 4.0.5 on 2022-06-18 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_record'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='units',
            field=models.CharField(choices=[('kg', 'KG'), ('dona', 'Dona'), ('korobka', 'Korobka'), ('qop', 'Qop')], max_length=512),
        ),
    ]