# Generated by Django 3.1 on 2020-10-16 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_product_user_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quality',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
