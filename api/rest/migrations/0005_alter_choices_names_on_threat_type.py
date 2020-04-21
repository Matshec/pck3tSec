# Generated by Django 3.0.5 on 2020-04-21 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0004_auto_20200419_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='threat',
            name='threat_type',
            field=models.CharField(choices=[('HOST', 'host'), ('FILE', 'file'), ('USER_DEFINED', 'user_defined')], max_length=20),
        ),
    ]
