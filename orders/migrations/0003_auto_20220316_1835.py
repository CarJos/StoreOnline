# Generated by Django 2.2 on 2022-03-16 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_total',
            field=models.DecimalField(decimal_places=2, default=5, max_digits=8),
        ),
    ]
