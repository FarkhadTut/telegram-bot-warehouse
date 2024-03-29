# Generated by Django 4.0.4 on 2022-08-11 06:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_alter_identifier_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identifier',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='identifier',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
