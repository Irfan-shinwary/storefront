# Generated by Django 5.1.4 on 2025-01-30 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_product_price_alter_product_promotions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adress',
            name='zip',
        ),
    ]
