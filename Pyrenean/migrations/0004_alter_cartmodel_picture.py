# Generated by Django 4.2.4 on 2023-08-24 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pyrenean', '0003_alter_cartmodel_description_alter_kides_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartmodel',
            name='picture',
            field=models.FileField(upload_to='static/images/CartModules/'),
        ),
    ]
