from django.contrib import admin
from .models import *
# Register your models here.

class AdvanceCashInline(admin.TabularInline):
    fields = ["currency", "amount"]
    extra = 0
    model = AdvanceCash


class AdvanceOthersInline(admin.TabularInline):
    fields = ["sellable", "quantity"]
    extra = 0
    model = AdvanceOthers


class AdvanceFuelInline(admin.TabularInline):
    fields = ["station", "fuel_quantity"]
    extra = 0
    model = AdvanceFuel



@admin.register(Nomination)
class NominationAdmin(admin.ModelAdmin):
    list_display = ("transporter", "customer", "nomination_status")
    inlines = (AdvanceCashInline, AdvanceFuelInline, AdvanceOthersInline)


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.operator:
            return qs.filter(nomination_status= "approval_pending") 
        elif request.user.validator:
            return qs.filter(nomination_status = "validation_pending")    
        else :
            return qs


@admin.register(AdvanceCash)
class AdvanceCashAdmin(admin.ModelAdmin):
    list_display = ("nomination", "currency", "amount")

@admin.register(AdvanceFuel)
class AdvanceFuelAdmin(admin.ModelAdmin):
    list_display = ("station", "fuel_quantity")

@admin.register(AdvanceOthers)
class AdvanceOthersAdmin(admin.ModelAdmin):
    list_display = ("sellable", "quantity")


admin.site.register(Transit)
admin.site.register(Fullfillment)
