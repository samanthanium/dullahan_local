# Generated by Django 3.0.5 on 2020-06-10 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_system', '0002_auto_20200610_1012'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='connection_type',
            field=models.CharField(choices=[('BT', 'Bluetooth'), ('ZB', 'ZigBee')], default='BT', max_length=2),
        ),
    ]
