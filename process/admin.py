from django.contrib import admin
from .models import *
# Register your models here.

class AdvanceInline(admin.TabularInline):
    fields = ["advance_type", "quantity", "unit", "cost"]
    extra = 0
    model = Advance


class NominationStationInline(admin.TabularInline):
    fields = ["station", "fuel_quantity"]
    extra = 0
    model = NominationStation


@admin.register(Nomination)
class NominationAdmin(admin.ModelAdmin):
    list_display = ("transporter", "customer", "nomination_status")
    inlines = (AdvanceInline, NominationStationInline)

admin.site.register(NominationStation)
admin.site.register(Transit)
admin.site.register(Fullfillment)
