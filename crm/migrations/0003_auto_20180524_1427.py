# Generated by Django 2.0.5 on 2018-05-24 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_auto_20180524_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='menu',
            field=models.ManyToManyField(blank=True, to='crm.Menu'),
        ),
    ]