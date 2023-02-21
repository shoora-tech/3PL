from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Currency)

@admin.register(CurrencyExchange)
class AdvanceCashAdmin(admin.ModelAdmin):
    list_display = ("from_currency", "to_currency", "exchange_rate")

admin.site.register(Product)
admin.site.register(Company)
admin.site.register(Station)
admin.site.register(Fuel)
admin.site.register(Transporter)
admin.site.register(TransporterOrganizationFuel)
admin.site.register(Vehicle)
admin.site.register(Tanker)
admin.site.register(Driver)
admin.site.register(Customer)
admin.site.register(Sellables)
admin.site.register(Unit)
admin.site.register(Manufacturer)