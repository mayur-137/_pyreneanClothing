# Generated by Django 4.2.4 on 2023-10-15 08:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Pyrenean', '0002_alter_wishlist_product_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscribeNow',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=255, unique=True)),
            ],
        ),
    ]