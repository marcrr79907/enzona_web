from django.contrib import admin
from .models import *

admin.site.register(User_Card)
admin.site.register(Bank_DB)
admin.site.register(Person_DB)
admin.site.register(Phone_DB)
admin.site.register(Transfer)
admin.site.register(Service_Pay)
admin.site.register(Destinatary)
admin.site.register(Gas_Service)
admin.site.register(Electricity_Service)

