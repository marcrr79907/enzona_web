# Generated by Django 4.2.1 on 2023-06-05 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0006_service_pay_checked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service_pay',
            name='service_id',
            field=models.IntegerField(),
        ),
        migrations.DeleteModel(
            name='Gas_Service_Pay',
        ),
    ]
