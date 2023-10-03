# Generated by Django 4.2.5 on 2023-10-03 12:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Pyrenean', '0003_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_data',
            name='state',
            field=models.CharField(default='GUJRAT', max_length=100),
        ),
        migrations.AlterField(
            model_name='user_data',
            name='email',
            field=models.EmailField(max_length=100),
        ),
        migrations.AlterField(
            model_name='user_data',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
