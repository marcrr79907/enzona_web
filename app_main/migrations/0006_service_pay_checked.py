# Generated by Django 4.2.1 on 2023-06-02 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0005_remove_transfer_confirm_mobile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='service_pay',
            name='checked',
            field=models.BooleanField(default=False),
        ),
    ]
