# Generated by Django 4.2.1 on 2023-05-22 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bank_DB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.IntegerField(unique=True)),
                ('date_exp', models.DateField()),
                ('bank_type', models.CharField(max_length=20)),
                ('currency_type', models.CharField(max_length=20)),
                ('balance', models.PositiveIntegerField(default=0)),
                ('pin', models.CharField(max_length=4)),
                ('associated', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Banco_DB',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Person_DB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=50)),
                ('date_birthday', models.DateField()),
                ('address', models.CharField(max_length=50)),
                ('dni', models.IntegerField(unique=True)),
                ('register', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Personas_DB',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Phone_DB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(unique=True)),
                ('propietary_name', models.CharField(max_length=50)),
                ('associated', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Teléfonos_DB',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='User_Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=200, unique=True)),
                ('balance', models.PositiveIntegerField(default=0)),
                ('pin', models.CharField(max_length=4)),
            ],
            options={
                'verbose_name': 'Tarjeta',
                'verbose_name_plural': 'Tarjetas',
                'ordering': ['id'],
            },
        ),
    ]
