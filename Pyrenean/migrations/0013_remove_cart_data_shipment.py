# Generated by Django 4.2.5 on 2023-11-02 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Pyrenean', '0012_merge_20231102_1610'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart_data',
            name='shipment',
        ),
    ]
