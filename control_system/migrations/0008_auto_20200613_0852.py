# Generated by Django 3.0.4 on 2020-06-13 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_system', '0007_auto_20200613_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='hostname',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='name',
            field=models.CharField(default='My New Device', max_length=50),
        ),
    ]
