# Generated by Django 5.1.3 on 2024-12-07 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_wishlist_wishlistitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]
