from django.db import models
from datetime import datetime

# Create your models here.

# -----------------Data Bases------------------#


class Bank_DB(models.Model):
    card_number = models.IntegerField(unique=True, null=False)
    date_exp = models.DateField(null=False)
    bank_type = models.CharField(max_length=20, null=False)
    currency_type = models.CharField(max_length=20, null=False)
    balance = models.PositiveIntegerField(default=0, null=False)
    associated = models.BooleanField(default=False, null=False)

    def __str__(self):
        return f'Número: {self.card_number} Banco: {self.bank_type} Saldo: {self.balance} Asociada: {self.associated}'


class Person_DB(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    gener = models.CharField(max_length=50, null=False)
    born_date = models.DateField(null=False)
    address = models.CharField(max_length=50, null=False)
    dni = models.IntegerField(unique=True, null=False)
    register = models.BooleanField(default=False)

    def __str__(self):
        return f'Nombre: {self.first_name} Apellido: {self.last_name} Registrada: {self.register}'


class Phone_DB(models.Model):
    number = models.IntegerField(unique=True, null=False)
    propietary_name = models.CharField(max_length=50, null=False)
    associated = models.BooleanField(default=False)

    def __str__(self):
        return f'Número: {self.number} Nombre Propietario: {self.propietary_name} Asociado: {self.associated}'


class Electricity_Service(models.Model):
    electricity_id = models.IntegerField(unique=True, null=False)
    electricity_cost = models.IntegerField()
    propietary_name = models.CharField(max_length=50)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return f'ID_Electricidad: {self.electricity_id} Importe: {self.cost} Chequeado: {self.checked}'


class Gas_Service(models.Model):
    gas_id = models.IntegerField(unique=True, null=False)
    gas_cost = models.IntegerField()
    propietary_name = models.CharField(max_length=50)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return f'ID_Gas: {self.gas_id} Importe: {self.gas_cost} Chequeado: {self.checked}'


# -----------------Fin Data Bases------------------#


# ____________________ENZONA DATA BASES____________________

class User(models.Model):
    full_name = models.CharField(max_length=200)
    gener = models.CharField(max_length=50)
    born_date = models.DateField()
    address = models.CharField(max_length=200)

    user_name = models.CharField(max_length=200, unique=True, null=False)
    password = models.CharField(max_length=200, null=False)

    phone = models.ForeignKey(Phone_DB, unique=True, on_delete=models.CASCADE)
    id_person = models.ForeignKey(
        Person_DB, unique=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_name


class User_Card(models.Model):
    card_card = models.ManyToManyField(Bank_DB)
    card_electricity = models.ManyToManyField(Electricity_Service)
    card_gas = models.ManyToManyField(Gas_Service)

    card_number = models.IntegerField(unique=True, null=False)
    date_ex = models.DateField(null=False)
    currency_type = models.CharField(max_length=20, null=False)
    balance = models.PositiveIntegerField(default=0)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Número tarjeta: {self.card_number} Usuario: {self.user.user_name}'


"""class Transfer(models.Model):
    origin_card = models.IntegerField(null=False)
    dest_card = models.IntegerField(null=False)
    import_transfer = models.PositiveIntegerField(null=False)
    confirm_mobile = models.IntegerField(null=False)
    date = models.DateField(default=datetime.now)

    def __str__(self):
        return f'Origen: {self.origin_card} Destino: {self.dest_card} Cantidad: {self.import_transfer}'


class Electricity_Service_Pay(models.Model):
    service_id = models.ForeignKey(
        Electricity_Service, unique=True, on_delete=models.CASCADE, null=False)

    propietary = models.CharField(max_length=50)
    service_type = models.CharField(max_length=50)
    import_service = models.IntegerField()
    date = models.DateField(default=datetime.now)

    def __str__(self) -> str:
        return f'ID_servicio: {self.service_id.electricity_id} Tipo: {self.service_type} Importe: {self.import_service}'

"""


class Destinatary(models.Model):
    name = models.CharField(max_length=50)
    associated_card = models.ForeignKey(
        Bank_DB, unique=True, on_delete=models.CASCADE, null=False)

    def __str__(self) -> str:
        return f'Nombre: {self.name} Tarjeta: {self.associated_card}'

# ____________________ENZONA DATA BASES____________________
