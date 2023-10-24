# Generated by Django 4.2.4 on 2023-10-07 09:44

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Pyrenean', '0005_cart_data_final_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='size',
            name='kid',
        ),
        migrations.RemoveField(
            model_name='size',
            name='men',
        ),
        migrations.RemoveField(
            model_name='size',
            name='women',
        ),
        migrations.CreateModel(
            name='Product_Details',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('category', models.CharField(choices=[('Mens', 'Mens'), ('UniSex', 'UniSex'), ('Women', 'Women')], max_length=10)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=1080)),
                ('price', models.IntegerField()),
                ('discount', models.PositiveIntegerField()),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('picture', models.ImageField(upload_to='static/images/Product_images/')),
                ('picture_1', models.ImageField(upload_to='static/images/Product_images/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Pyrenean.size')),
            ],
        ),
    ]