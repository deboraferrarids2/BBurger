# Generated by Django 3.2.13 on 2024-01-27 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=400),
        ),
    ]
