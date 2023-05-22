from datetime import datetime
from django.db import models

from app_users.models import User

# Create your models here.

# -----------------Data Bases------------------#


class Bank_DB(models.Model):

    card_number = models.IntegerField(unique=True)
    date_exp = models.DateField(null=False)
    bank_type = models.CharField(max_length=20)
    currency_type = models.CharField(max_length=20)
    balance = models.PositiveIntegerField(default=0)
    pin = models.CharField(max_length=4)
    associated = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Banco_DB'
        ordering = ['id']

    def __str__(self):
        return f'Número: {self.card_number} Banco: {self.bank_type} Saldo: {self.balance} Asociada: {self.associated}'


class Person_DB(models.Model):

    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    gender = models.CharField(max_length=50, null=False)
    date_birthday = models.DateField(null=False)
    address = models.CharField(max_length=50, null=False)
    dni = models.IntegerField(unique=True, null=False)
    register = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Personas_DB'
        ordering = ['id']

    def __str__(self):
        return f'Nombre: {self.first_name} Apellido: {self.last_name} Registrada: {self.register}'


class Phone_DB(models.Model):

    number = models.IntegerField(unique=True, null=False)
    propietary_name = models.CharField(max_length=50, null=False)
    associated = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Teléfonos_DB'
        ordering = ['id']

    def __str__(self):
        return f'Número: {self.number} Nombre Propietario: {self.propietary_name} Asociado: {self.associated}'


class Electricity_Service(models.Model):

    electricity_id = models.IntegerField(unique=True, null=False)
    electricity_cost = models.IntegerField()
    propietary_name = models.CharField(max_length=50)
    checked = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Servicio_Electricidad'
        ordering = ['id']

    def __str__(self):
        return f'ID_Electricidad: {self.electricity_id} Importe: {self.cost} Chequeado: {self.checked}'


class Gas_Service(models.Model):

    gas_id = models.IntegerField(unique=True, null=False)
    gas_cost = models.IntegerField()
    propietary_name = models.CharField(max_length=50)
    checked = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Servicio_Gas '
        ordering = ['id']

    def __str__(self):
        return f'ID_Gas: {self.gas_id} Importe: {self.gas_cost} Chequeado: {self.checked}'


# -----------------Fin Data Bases------------------#


# ____________________ENZONA DATA BASES____________________


class User_Card(models.Model):
    card_number = models.CharField(max_length=200, unique=True)
    balance = models.PositiveIntegerField(default=0)
    pin = models.CharField(max_length=4)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Tarjeta'
        verbose_name_plural = 'Tarjetas'
        ordering = ['id']


class Transfer(models.Model):

    origin_card = models.IntegerField(null=False)
    dest_card = models.IntegerField(null=False)
    import_transfer = models.PositiveIntegerField(null=False)
    confirm_mobile = models.IntegerField(null=False)
    date = models.DateField(default=datetime.now)

    class Meta:
        verbose_name = 'Transferencia'
        verbose_name_plural = 'Transferencias'
        ordering = ['id']

    def __str__(self):
        return f'Origen: {self.origin_card} Destino: {self.dest_card} Cantidad: {self.import_transfer}'


class Electricity_Service_Pay(models.Model):

    service_id = models.IntegerField(unique=True, null=False)
    propietary = models.CharField(max_length=50)
    service_type = models.CharField(max_length=50)
    import_service = models.IntegerField()
    date = models.DateField(default=datetime.now)

    id_electricity = models.ForeignKey(
        Electricity_Service, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Pago_Electricidad'
        ordering = ['id']

    def __str__(self) -> str:
        return f'ID_servicio: {self.service_id} Tipo: {self.service_type} Importe: {self.import_service}'


class Gas_Service_Pay(models.Model):
    service_id = models.IntegerField(unique=True, null=False)
    propietary = models.CharField(max_length=50)
    service_type = models.CharField(max_length=50)
    import_service = models.IntegerField()
    date = models.DateField(default=datetime.now)

    id_gas = models.ForeignKey(
        Gas_Service, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Pago_Gas'
        ordering = ['id']

    def __str__(self) -> str:
        return f'ID_servicio: {self.service_id} Tipo: {self.service_type} Importe: {self.import_service}'


class Destinatary(models.Model):
    name = models.CharField(max_length=50)
    associated_card = models.ForeignKey(
        Bank_DB, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Destinatario'
        verbose_name_plural = 'Destinatarios'
        ordering = ['id']

    def __str__(self) -> str:
        return f'Nombre: {self.name} Tarjeta: {self.associated_card}'

# ____________________ENZONA DATA BASES____________________
