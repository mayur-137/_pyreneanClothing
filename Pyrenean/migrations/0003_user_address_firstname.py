# Generated by Django 4.2.4 on 2023-11-04 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pyrenean', '0002_alter_cart_data_address_1'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_address',
            name='firstname',
            field=models.CharField(default='', max_length=50),
        ),
    ]
