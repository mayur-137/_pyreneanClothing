# Generated by Django 4.2.5 on 2023-10-30 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pyrenean', '0007_merge_20231030_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='final_order',
            name='link_id',
            field=models.CharField(default=0, max_length=1000),
        ),
    ]
