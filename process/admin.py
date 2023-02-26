from django.contrib import admin
from django.http import HttpResponseRedirect
# from django.http import HttpResponseRedirect

# from process.forms import VerifyNominationForm
from .models import *
from django.utils.html import format_html
from django.urls import path
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import redirect

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
    list_display = (
        "transporter",
        "nomination_date",
        "vehicle",
        "tanker",
        "customer",
        "product",
        "advance_cash",
        "advance_fuel",
        "advance_others",
        "base_quantity",
        "l20_quantity",
        "loading_date",
        "release_date",
        "rate",
        "invoice_value",
        "transporter_invoice_number",
        "transporter_invoice_date",
        "ofloading_quantity",
        "offloading_date",
        "shortage",
        "tolerance",
        "net_shortage",
        "shortage_value",
        "net_to_be_paid",
        "profitability",
        "paid",
        "sales_approval",
        "stage",
        "custom_button",
        "action_button"
    )
    readonly_fields = ("transit", "offload", "stage", "nomination_status", "sales_approved")
    inlines = (AdvanceCashInline, AdvanceFuelInline, AdvanceOthersInline)

    def nomination_date(self, obj):
        return obj.created_at.date()
    
    def advance_cash(self, obj):
        cash = obj.advance_cash.all()
        total = 0
        for c in cash:
            if c.currency.name != "USD":
                exchange_rate = CurrencyExchange.objects.get(from_currency__name="USD", to_currency=c.currency).exchange_rate
                amount = c.amount * (1/exchange_rate)
            else:
                amount = c.amount
            total += amount
        total = round(total, 2)
        return format_html(
                    '<a href="{}">{}</a>&nbsp;',
                    reverse('admin:process_nomination_change', args=[obj.pk]),
                    total
                )


    def advance_fuel(self, obj):
        fuel = obj.advance_fuel.all()
        total = 0
        for f in fuel:
            fuel_price = Fuel.objects.filter(station=f.station).last()
            if fuel_price:
                qty = f.fuel_quantity
                amount = qty * fuel_price.fuel_price
                total += amount
        total = round(total, 2)
        return format_html(
                    '<a href="{}">{}</a>&nbsp;',
                    reverse('admin:process_nomination_change', args=[obj.pk]),
                    total
                )


    def advance_others(self, obj):
        others = obj.advance_others.all()
        total = 0
        for o in others:
            qty = o.quantity
            exchange_rate = CurrencyExchange.objects.get(from_currency__name="USD", to_currency=o.sellable.currency).exchange_rate
            amount = qty * o.sellable.unit_price * (1/exchange_rate)
            total += amount
        total = round(total, 2)
        return format_html(
                    '<a href="{}">{}</a>&nbsp;',
                    reverse('admin:process_nomination_change', args=[obj.pk]),
                    total
                )

    def base_quantity(self, obj):
        if obj.transit:
            return obj.transit.loading_base_quantity
        return None

    def l20_quantity(self, obj):
        if obj.transit:
            return obj.transit.locading_l20_quantity
        return None

    def loading_date(self, obj):
        if obj.transit:
            return obj.transit.created_at.date()
        return None

    def release_date(self, obj):
        if obj.transit:
            return obj.transit.release_date
        return None

    
    def invoice_value(self, obj):
        if obj.transit:
            return obj.transit.invoice_value
        return None

    def transporter_invoice_number(self, obj):
        if obj.transit:
            return obj.transit.invoice_number
        return None

    def transporter_invoice_date(self, obj):
        if obj.transit:
            return obj.transit.invoice_date
        return None
        
    def ofloading_quantity(self, obj):
        if obj.offload:
            return obj.offload.off_loading_l20_quantity
        return None

    def offloading_date(self, obj):
        if obj.offload:
            return obj.offload.off_loading_date
        return None

    def shortage(self, obj):
        if obj.offload:
            return obj.offload.shortage
        return None

    def tolerance(self, obj):
        if obj.offload:
            return obj.offload.tolerance
        return None

    def net_shortage(self, obj):
        if obj.offload:
            return obj.offload.net_shortage
        return None

    def shortage_value(self, obj):
        if obj.offload:
            return obj.offload.shortage_value
        return None

    def net_to_be_paid(self, obj):
        if obj.offload:
            return obj.offload.net_to_be_paid
        return None

    def profitability(self, obj):
        if obj.offload:
            return obj.offload.profiltability
        return None

    def sales_approval(self, obj):
        if not obj.sales_approved:
            return format_html(
                    '<a class="button" href="{}">Approve</a>&nbsp;',
                    reverse('admin:nomination-approve-sale', args=[obj.pk])
                )
        return "Sales Approved"
    
    def paid(self, obj):
        if obj.offload and not obj.offload.dues_paid:
            transporter = obj.transporter
            try:
                if transporter.bulk_money >= obj.offload.net_to_be_paid:
                    return format_html(
                            '<a class="button" href="{}">Pay</a>&nbsp;',
                            reverse('admin:nomination-paid', args=[obj.pk])
                        )
            except Exception as e:
                pass
        elif obj.offload and obj.offload.dues_paid:
            return format_html(
                "<p>PAID<p>"
            )

        return "---"
    
    
    

    

    def custom_button(self, obj):
        if obj.nomination_status == Nomination.VALIDATION_PENDING:
            return format_html(
                '<a class="button" href="{}">Verify</a>&nbsp;',
                reverse('admin:nomination-verify', args=(obj.pk, )),
            )
        elif obj.nomination_status == Nomination.APPROVAL_PENDING:
            return format_html(
                '<a class="button" href="{}">Approve</a>&nbsp;',
                reverse('admin:nomination-approve', args=[obj.pk])
            )
        
        return format_html(
            '<p> Approved </p>',
        )
    
    def action_button(self, obj):
        if obj.nomination_status != Nomination.APPROVED:
            return format_html(
            '<p> ---- </p>',
        )
        else:
            if obj.stage == Nomination.NOMINATION and obj.nomination_status == Nomination.APPROVED and obj.sales_approved:
                return format_html(
                    '<a class="button" href="{}">Move to transit</a>&nbsp;',
                    reverse('admin:nomination-transit', args=(obj.pk, )),
                )
            elif obj.stage == Nomination.TRANSIT and obj.nomination_status == Nomination.APPROVED and obj.sales_approved:
                return format_html(
                    '<a class="button" href="{}">Move to offload</a>&nbsp;',
                    reverse('admin:nomination-offload', args=[obj.pk])
                )
            
            elif obj.stage == Nomination.OFFLOAD and obj.nomination_status == Nomination.APPROVED and obj.sales_approved:
                return format_html(
                    '<p> Completed </p>'
                )
            
        
        return format_html(
            '<p> --- </p>',
        )

    custom_button.short_description = "Status Action"
    action_button.short_description = "Stage Action"
        
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("<nomination_id>/verify/",
            self.admin_site.admin_view(self.verify),
            name='nomination-verify'
            ),
            path("<nomination_id>/approve/",
            self.admin_site.admin_view(self.approve),
            name='nomination-approve'
            ),
            path("<nomination_id>/transit/",
            self.admin_site.admin_view(self.transit),
            name='nomination-transit'
            ),
            path("<nomination_id>/offload/",
            self.admin_site.admin_view(self.offload),
            name='nomination-offload'
            ),
            path("<nomination_id>/approve-sale/",
            self.admin_site.admin_view(self.approve_sales),
            name='nomination-approve-sale'
            ),
            path("<nomination_id>/paid/",
            self.admin_site.admin_view(self.dues),
            name='nomination-paid'
            ),
            
        ]
        return custom_urls + urls
    
    def verify(self, request, nomination_id, *args, **kwargs):
        nomination = self.get_object(request, nomination_id)
        nomination.nomination_status = Nomination.APPROVAL_PENDING
        nomination.save()
        return HttpResponseRedirect(reverse('admin:process_nomination_changelist'))
    
    def approve(self, request, nomination_id, *args, **kwargs):
        nomination = self.get_object(request, nomination_id)
        nomination.nomination_status = Nomination.APPROVED
        nomination.save()
        return HttpResponseRedirect(reverse('admin:process_nomination_changelist'))
    
    def transit(self, request, nomination_id, *args, **kwargs):
        # create transit for this nomination using default values
        nomination = self.get_object(request, nomination_id)
        transit = Transit.objects.create(
            loading_date = timezone.now().date(),
            release_date = timezone.now().date(),
            loading_base_quantity = 0,
            locading_l20_quantity = 0,
        )
        nomination.transit = transit
        nomination.stage = Nomination.TRANSIT
        nomination.save()
        return HttpResponseRedirect(reverse('admin:process_transit_change', args=(transit.id,)))
    
    
    def offload(self, request, nomination_id, *args, **kwargs):
        # create transit for this nomination using default values
        nomination = self.get_object(request, nomination_id)
        transit = nomination.transit
        offload = Fullfillment.objects.create(
            off_loading_date = timezone.now().date(),
            off_loading_l20_quantity = 0,
        )
        transit.fullfillment = offload
        transit.save()
        nomination.offload = offload
        nomination.stage = Nomination.OFFLOAD
        nomination.save()
        return HttpResponseRedirect(reverse('admin:process_fullfillment_change', args=(offload.id,)))
    
    def approve_sales(self, request, nomination_id, *args, **kwargs):
        nomination = self.get_object(request, nomination_id)
        nomination.sales_approved = True
        nomination.save()
        return HttpResponseRedirect(reverse('admin:process_nomination_changelist'))
    
    def dues(self, request, nomination_id, *args, **kwargs):
        nomination = self.get_object(request, nomination_id)
        transporter = nomination.transporter
        offload = nomination.offload
        bm = transporter.bulk_money
        bm = bm - offload.net_to_be_paid
        transporter.bulk_money = bm
        transporter.save()
        offload.dues_paid = True
        offload.save()
        return HttpResponseRedirect(reverse('admin:process_nomination_changelist'))



@admin.register(AdvanceCash)
class AdvanceCashAdmin(admin.ModelAdmin):
    list_display = ("nomination", "currency", "amount")


@admin.register(AdvanceFuel)
class AdvanceFuelAdmin(admin.ModelAdmin):
    list_display = ("station", "fuel_quantity")

@admin.register(AdvanceOthers)
class AdvanceOthersAdmin(admin.ModelAdmin):
    list_display = ("sellable", "quantity")

# Transit
class NominationInline(admin.StackedInline):
    readonly_fields = [
        "transporter",
        "tanker",
        "vehicle",
        "driver",
        "customer",
        "source",
        "destination",
        "product",
        # "tanker_capacity",
        "expected_loading_date",
        "nomination_status",
        "stage",
        "sales_approved",
        "rate",
        "offload"
        ]
    extra = 0
    model = Nomination


class TransitInline(admin.TabularInline):
    readonly_fields = [
        "loading_date",
        "loading_base_quantity",
        "locading_l20_quantity",
        "release_date",
    ]
    extra = 0
    model = Transit

@admin.register(Transit)
class TransmitAdmin(admin.ModelAdmin):
    inlines = (NominationInline,)
    readonly_fields = ("fullfillment", "invoice_value")

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/process/nomination')

    def response_change(self, request, obj):
        return redirect('/admin/process/nomination')
    
    def save_model(self, request, obj, form, change):
        # print("rate ", obj.__dict__)
        nomination = Nomination.objects.get(transit__id=obj.id)
        obj.invoice_value = (nomination.rate * obj.locading_l20_quantity)/1000
        super().save_model(request, obj, form, change)

@admin.register(Fullfillment)
class FullfillmentAdmin(admin.ModelAdmin):
    inlines = (NominationInline, TransitInline)
    readonly_fields = (
        "shortage",
        "tolerance",
        "net_shortage",
        "shortage_value",
        "net_to_be_paid",
        "profiltability",
    )

    def save_model(self, request, obj, form, change):
        # print("rate ", obj.__dict__)
        nomination = Nomination.objects.get(offload__id=obj.id)
        transit = Transit.objects.get(fullfillment__id=obj.id)
        # shortage 
        obj.shortage = transit.locading_l20_quantity - obj.off_loading_l20_quantity
        # tolerance
        obj.tolerance = (nomination.product.tolerance / 100) * transit.locading_l20_quantity
        # net shortage
        net_shortage = obj.shortage - obj.tolerance
        obj.net_shortage = 0 if net_shortage < 0 else net_shortage
        obj.shortage_value = obj.net_shortage * nomination.product.cost
        # All Advances
        cash = nomination.advance_cash.all()
        fuel = nomination.advance_fuel.all()
        others = nomination.advance_others.all()
        total = 0
        for c in cash:
            if c.currency.name != "USD":
                exchange_rate = CurrencyExchange.objects.get(from_currency__name="USD", to_currency=c.currency).exchange_rate
                amount = c.amount * (1/exchange_rate)
            else:
                amount = c.amount
            total += amount
        
        for f in fuel:
            fuel_price = Fuel.objects.filter(station=f.station).last()
            qty = f.fuel_quantity
            amount = qty * fuel_price.fuel_price
            total += amount
        
        for o in others:
            qty = o.quantity
            exchange_rate = CurrencyExchange.objects.get(from_currency__name="USD", to_currency=o.sellable.currency).exchange_rate
            amount = qty * o.sellable.unit_price * (1/exchange_rate)
            total += amount
        
        obj.net_to_be_paid = transit.invoice_value - obj.shortage_value - total
        obj.invoice_value = nomination.rate * transit.locading_l20_quantity
        obj.profiltability = ((nomination.customer.price * transit.locading_l20_quantity)/1000) - transit.invoice_value
        super().save_model(request, obj, form, change)

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/process/nomination')

    def response_change(self, request, obj):
        return redirect('/admin/process/nomination')


