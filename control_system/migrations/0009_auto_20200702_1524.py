# Generated by Django 3.0.4 on 2020-07-02 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_system', '0008_auto_20200613_0852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='connection_type',
            field=models.CharField(choices=[('BT', 'Bluetooth')], default='BT', max_length=2),
        ),
    ]
