# Generated by Django 3.1 on 2020-08-10 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileuser',
            name='birthday',
            field=models.CharField(max_length=40),
        ),
    ]