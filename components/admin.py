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

class TransporterBulkPaymentInline(admin.TabularInline):
    fields = ["currency", "amount","exchange_rate", "payment_date"]
    readonly_fields = ("created_at",)
    extra = 1
    model = TransporterBulkPayment


@admin.register(Transporter)
class TransporterAdmin(admin.ModelAdmin):
    list_display = ("name","poc_name","poc_email")
    readonly_fields = ("bulk_money",)
    inlines = (TransporterBulkPaymentInline,)


admin.site.register(DiscountMaster)

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("vehicle_number","transporter")

@admin.register(Tanker)
class TankerAdmin(admin.ModelAdmin):
    list_display = ("tanker_number","transporter")

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("name","transporter")


admin.site.register(Customer)
admin.site.register(Sellables)
admin.site.register(Unit)
admin.site.register(Manufacturer)
admin.site.register(Location)