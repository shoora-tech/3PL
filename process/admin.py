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
from user.models import User
from django.db.models import Sum
from django import forms
from dal import autocomplete

# Register your models here.

class AdvanceCashInline(admin.TabularInline):
    fields = ["currency", "amount","exchange_rate","local_exchange_rate"]
    extra = 0
    model = AdvanceCash


class AdvanceOthersInline(admin.TabularInline):
    fields = ["sellable","unit","unit_price","currency","exchange_rate",  "quantity","local_exchange_rate"]
    extra = 0
    model = AdvanceOthers


class AdvanceFuelInline(admin.TabularInline):
    fields = ["station","requested_fuel_quantity","requested_date", "approved_fuel_quantity","approved_date","fuel_price","currency","exchange_rate","local_exchange_rate"]
    extra = 0
    model = AdvanceFuel


    



class NominationForm(forms.ModelForm):
    vehicle = forms.ModelChoiceField(
        queryset=Vehicle.objects.all(),
        widget=autocomplete.ModelSelect2(
                        url='transporter_vehicle_autocomplete',
                        forward=['transporter'],
                ),
    )

    
    
    tanker = forms.ModelChoiceField(
        queryset=Tanker.objects.all(),
        widget=autocomplete.ModelSelect2(
                        url='transporter_tanker_autocomplete',
                        forward=['transporter'],
                ),
    )

    driver = forms.ModelChoiceField(
        queryset=Driver.objects.all(),
        widget=autocomplete.ModelSelect2(
                        url='transporter_driver_autocomplete',
                        forward=['transporter'],
                ),
    )

@admin.register(Nomination)
class NominationAdmin(admin.ModelAdmin):
    exclude = ('is_deleted',)
    list_display = (
        "transporter",
        "stage",
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
        # "paid",
        "sales_approval",
        "custom_button",
        "action_button"
    )
    form = NominationForm
    readonly_fields = ("transit", "offload", "stage", "nomination_status", "sales_approved", "summary","summary_in_local_currency")
    inlines = (AdvanceCashInline, AdvanceFuelInline, AdvanceOthersInline)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.user_type == User.VALIDATOR:
            return qs.filter(nomination_status=Nomination.VALIDATION_PENDING)
        
        if request.user.user_type == User.OPERATOR:
            return qs.exclude(stage=Nomination.OFFLOAD)
        
        elif request.user.user_type == User.SALES_APPROVER:
            return qs.filter(sales_approved=False)
        return qs.filter(is_deleted=False)

    def get_list_display(self, request):
        # only sales approver user can see sales approve section
        # only validator can see validate option
        # only approver can see approve option
        list_display = list(self.list_display)
        if not request.user.is_superuser:
            if request.user.user_type not in  [User.SALES_APPROVER, User.ADMIN]:
                list_display.remove("sales_approval")

            if request.user.user_type not in [User.VALIDATOR, User.ADMIN]:
                list_display.remove("custom_button")
        
        return list_display
        

    def nomination_date(self, obj):
        return obj.created_at.date()
    
    def advance_cash(self, obj):
        others = obj.advance_cash.all()
        total = 0
        for o in others:
            amt = o.amount
            exchange_rate = o.exchange_rate
            if exchange_rate :
                amount = amt*(1/exchange_rate)
                total += amount
            else:
                exchange_rate = 1
                amount = amt*(1/exchange_rate)
                total += amount

        total = round(total, 2)
        return format_html(
                    '<a href="{}">{}</a>&nbsp;',
                    reverse('admin:process_nomination_change', args=[obj.pk]),
                    total
                )


    def advance_fuel(self, obj):
        total = 0
        fuel = obj.advance_fuel.aggregate(total=Sum("net_amount"))
        if fuel['total']:
            total = round(fuel['total'], 2)
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
            exchange_rate = o.exchange_rate
            amount = qty * o.unit_price * (1/exchange_rate)
            total += amount
        total = round(total, 2)
        return format_html(
                    '<a href="{}">{}</a>&nbsp;',
                    reverse('admin:process_nomination_change', args=[obj.pk]),
                    str(total)
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
        nomination.offload = offload
        nomination.stage = Nomination.OFFLOAD
        # create summary
        summary = Summary.objects.create(
            nomination = nomination,
            transit = transit,
            fullfillment = offload,
        )
        summary.save()
        nomination.summary = summary
        transit.summary = summary
        offload.summary = summary
        nomination.save()
        transit.save()
        offload.save()

        #creating summary in local currency
        summary_in_local_currency = SummaryInLocalCurrency.objects.create(
            nomination = nomination,
            transit = transit,
            fullfillment = offload,
            summary = summary,
        )
        summary_in_local_currency.save()
        nomination.summary_in_local_currency = summary_in_local_currency
        transit.summary_in_local_currency = summary_in_local_currency
        offload.summary_in_local_currency = summary_in_local_currency
        summary.summary_in_local_currency = summary_in_local_currency
        nomination.save()
        transit.save()
        offload.save()
        summary.save()
        return HttpResponseRedirect(reverse('admin:process_fullfillment_change', args=(offload.id,)))
    
    def approve_sales(self, request, nomination_id, *args, **kwargs):
        nomination = self.get_object(request, nomination_id)
        nomination.sales_approved = True
        nomination.save()
        return HttpResponseRedirect(reverse('admin:process_nomination_changelist'))
    
    


@admin.register(AdvanceCash)
class AdvanceCashAdmin(admin.ModelAdmin):
    list_display = ("nomination", "currency", "amount","exchange_rate","local_exchange_rate")
    def has_module_permission(self, request):
        # print("\n\n............................................................................\n\n")
        # print(request.user)
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
        return False


@admin.register(AdvanceFuel)
class AdvanceFuelAdmin(admin.ModelAdmin):
    list_display = ("station","requested_fuel_quantity","requested_date", "approved_fuel_quantity","approved_date","fuel_price","currency","exchange_rate","local_exchange_rate")
    def has_module_permission(self, request):
        # print("\n\n............................................................................\n\n")
        # print(request.user)
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
        return False

@admin.register(AdvanceOthers)
class AdvanceOthersAdmin(admin.ModelAdmin):
    list_display = ("sellable","unit","unit_price","currency","exchange_rate", "quantity","local_exchange_rate")
    def has_module_permission(self, request):
        # print("\n\n............................................................................\n\n")
        # print(request.user)
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
        return False

# Transit
class NominationInline(admin.StackedInline):
    exclude = ('is_deleted',)
    readonly_fields = [
        "local_exchange_rate",
        "transit",
        "summary",
        "summary_in_local_currency",
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
    exclude = ('is_deleted',)
    readonly_fields = [
        "invoice_value",
        "invoice_value_local",
        "invoice_number",
        "invoice_date",
        "summary",
        "summary_in_local_currency",
        "loading_date",
        "loading_base_quantity",
        "locading_l20_quantity",
        "release_date",
    ]
    extra = 0
    model = Transit

@admin.register(Transit)
class TransmitAdmin(admin.ModelAdmin):
    exclude = ('is_deleted',)
    inlines = (NominationInline,)
    readonly_fields = ("fullfillment", "invoice_value", "summary","summary_in_local_currency","invoice_value_local",)

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/process/nomination')

    def response_change(self, request, obj):
        return redirect('/admin/process/nomination')
    
    def save_model(self, request, obj, form, change):
        # print("rate ", obj.__dict__)
        nomination = Nomination.objects.get(transit__id=obj.id)
        obj.invoice_value = (nomination.rate * obj.locading_l20_quantity)/1000
        obj.invoice_value_local = (nomination.rate*nomination.local_exchange_rate * obj.locading_l20_quantity) /1000

        super().save_model(request, obj, form, change)
    
    def has_module_permission(self, request):
        # print("\n\n............................................................................\n\n")
        # print(request.user)
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
        return False

@admin.register(Fullfillment)
class FullfillmentAdmin(admin.ModelAdmin):
    exclude = ('is_deleted',)
    inlines = (NominationInline, TransitInline)
    readonly_fields = (
        "shortage",
        "tolerance",
        "net_shortage",
        "shortage_value",
        "net_to_be_paid",
        "profiltability",
        "shortage_value_local",
        "net_to_be_paid_local",
        "profiltability_local",
        "summary",
        "summary_in_local_currency",
        "dues_paid",
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
        # obj.shortage_value = obj.net_shortage * nomination.product.cost
        obj.shortage_value = obj.net_shortage * obj.product_cost
        #shortage value in local
        obj.shortage_value_local = obj.net_shortage * obj.product_cost * obj.local_exchange_rate
        # All Advances
        cash = nomination.advance_cash.all()
        advance_fuel = nomination.advance_fuel.all()
        others = nomination.advance_others.all()
        total = 0
        for c in cash:
            if c.currency.name != "USD":
                exchange_rate = c.exchange_rate
                amount = c.amount * (1/exchange_rate)
            else:
                amount = c.amount
            total += amount
        
        
        
        for f in advance_fuel:
            dm = DiscountMaster.objects.filter(station=f.station, transporter__nomination=nomination).last()
            fd = 0
            if dm:
                fd = dm.fuel_discount
            if not dm:
                dm = 0
            fuel = Fuel.objects.filter(station=f.station).last()
            fuel_pr = f.fuel_price
            if fuel_pr : 
                fp = f.fuel_price
                exchange = f.exchange_rate
                amount = round(fp *(1/exchange),2)
                # fd = dm.fuel_discount
                exchange = dm.exchange_rate
                discount_per_liter = round(fd *(1/exchange),2)
                net_amount = (amount - discount_per_liter) * f.approved_fuel_quantity
                self.discount = discount_per_liter
                self.net_amount = net_amount
                total += net_amount

            else:     
                fp = fuel.fuel_price
                exchange = fuel.exchange_rate
                amount = round(fp *(1/exchange),2)
                # fd = dm.fuel_discount
                exchange = dm.exchange_rate
                discount_per_liter = round(fd *(1/exchange),2)
                net_amount = (amount - discount_per_liter) * f.approved_fuel_quantity
                self.discount = discount_per_liter
                self.net_amount = net_amount
                total += net_amount
        
        for o in others:
            qty = o.quantity
            exchange_rate = o.exchange_rate
            amount = qty * o.unit_price * (1/exchange_rate)
            total += amount

        #total for currency in local
        total_local = 0
        for o in cash:
            amt = o.amount
            exchange_rate = o.local_exchange_rate
            if exchange_rate :
                amount = amt*exchange_rate
                total_local += amount
            else:
                exchange_rate = 1
                amount = amt*exchange_rate
                total_local += amount
        
        
        
        for f in advance_fuel:
            dm = DiscountMaster.objects.filter(station=f.station, transporter__nomination=nomination).last()
            fd = 0
            if dm:
                fd = dm.fuel_discount
            if not dm:
                dm = 0
            fuel = Fuel.objects.filter(station=f.station).last()
            fuel_pr = f.fuel_price
            if fuel_pr : 
                fp = f.fuel_price
                exchange = f.local_exchange_rate 
                amount = round(fp * exchange,2)
                # fd = dm.fuel_discount
                exchange = dm.local_exchange_rate 
                discount_per_liter = round(fd * exchange,2)
                net_amount = (amount - discount_per_liter) * f.approved_fuel_quantity
                self.discount = discount_per_liter
                self.net_amount = net_amount
                total_local += net_amount

            else:     
                fp = fuel.fuel_price
                exchange = fuel.local_exchange_rate 
                amount = round(fp *exchange,2)
                exchange = dm.local_exchange_rate 
                discount_per_liter = round(fd *exchange,2)
                net_amount = (amount - discount_per_liter) * f.approved_fuel_quantity
                self.discount = discount_per_liter
                self.net_amount = net_amount
                total_local += net_amount
        
        for o in others:
            qty = o.quantity
            exchange_rate = o.local_exchange_rate 
            amount = qty * o.unit_price * exchange_rate
            total_local += amount    
        
        
        
        obj.net_to_be_paid = round((transit.invoice_value - obj.shortage_value - total),2)
        obj.invoice_value = nomination.rate * transit.locading_l20_quantity
        obj.profiltability = ((nomination.customer.price * transit.locading_l20_quantity)/1000) - transit.invoice_value
        #invoice value, net to be paid, profitability for local currency
        obj.invoice_value_local = nomination.rate*nomination.local_exchange_rate * transit.locading_l20_quantity 
        obj.net_to_be_paid_local = round((transit.invoice_value_local - obj.shortage_value_local - total_local),2)
        obj.profiltability_local = ((nomination.customer.price*nomination.customer.local_exchange_rate * transit.locading_l20_quantity)/1000) - transit.invoice_value_local


        obj.is_deleted = True
        nomination.is_deleted = True
        nomination.save()
        transit.is_deleted = True
        transit.save()
        return super().save_model(request, obj, form, change)

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/process/nomination')

    def response_change(self, request, obj):
        return redirect('/admin/process/nomination')
    
    def has_module_permission(self, request):
        # print("\n\n............................................................................\n\n")
        # print(request.user)
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
        return False

class FullfilmentInline(admin.TabularInline):
    exclude = ('is_deleted',)
    readonly_fields = [
        "shortage",
        "tolerance",
        "net_shortage",
        "shortage_value",
        "net_to_be_paid",
        "profiltability",
        "shortage_value_local",
        "net_to_be_paid_local",
        "profiltability_local",
    ]
    extra = 0
    model = Fullfillment

@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    inlines = (NominationInline, TransitInline, FullfilmentInline)
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
    )
    readonly_fields = (
        "nomination",
        "transit",
        "fullfillment",
        "summary_in_local_currency"
    )
    exclude = ("is_deleted",)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("<summary_id>/paid/",
            self.admin_site.admin_view(self.dues),
            name='summary-paid'
            ),
            
        ]
        return custom_urls + urls

    def transporter(self, obj):
        return obj.nomination.transporter

    def nomination_date(self, obj):
        return obj.nomination.created_at.date()

    def advance_cash(self, obj):
        cash = obj.nomination.advance_cash.all()
        total = 0
        for c in cash:
            if c.currency.name != "USD":
                exchange_rate = c.exchange_rate
                amount = c.amount * (1/exchange_rate)
            else:
                amount = c.amount
            total += amount
        total = round(total, 2)
        return total


    def advance_fuel(self, obj):
        total = 0
        fuel = obj.nomination.advance_fuel.aggregate(total=Sum("net_amount"))
        if fuel['total']:
            total = round(fuel['total'], 2)
        return total

    def rate(self, obj):
        return obj.nomination.rate

    def vehicle(self, obj):
        return obj.nomination.vehicle

    def tanker(self, obj):
        return obj.nomination.tanker

    def customer(self, obj):
        return obj.nomination.customer

    def product(self, obj):
        return obj.nomination.product


    def advance_others(self, obj):
        others = obj.nomination.advance_others.all()
        total = 0
        for o in others:
            qty = o.quantity
            exchange_rate = o.exchange_rate
            amount = qty * o.unit_price * (1/exchange_rate)
            total += amount
        total = round(total, 2)
        return total

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
        if obj.fullfillment:
            return obj.fullfillment.off_loading_l20_quantity
        return None

    def offloading_date(self, obj):
        if obj.fullfillment:
            return obj.fullfillment.off_loading_date
        return None

    def shortage(self, obj):
        if obj.fullfillment:
            return obj.fullfillment.shortage
        return None

    def tolerance(self, obj):
        if obj.fullfillment:
            return obj.fullfillment.tolerance
        return None

    def net_shortage(self, obj):
        if obj.fullfillment:
            return obj.fullfillment.net_shortage
        return None

    def shortage_value(self, obj):
        if obj.fullfillment:
            return obj.fullfillment.shortage_value
        return None

    def net_to_be_paid(self, obj):
        if obj.fullfillment:
            return obj.fullfillment.net_to_be_paid
        return None

    def profitability(self, obj):
        if obj.fullfillment:
            return obj.fullfillment.profiltability
        return None

    def sales_approval(self, obj):
        return "Approved"
    
    # def paid(self, obj):
    #     return "Paid"  

    def paid(self, obj):
        if obj.fullfillment and not obj.fullfillment.dues_paid:
            transporter = obj.nomination.transporter
            try:
                if transporter.bulk_money >= obj.fullfillment.net_to_be_paid:
                    return format_html(
                            '<a class="button" href="{}">Pay</a>&nbsp;',
                            reverse('admin:summary-paid', args=[obj.pk])
                        )
            except Exception as e:
                pass
        elif obj.fullfillment and obj.fullfillment.dues_paid:
            return format_html(
                "<p>PAID<p>"
            )

        return "---"

    def dues(self, request, summary_id, *args, **kwargs):
        summary = self.get_object(request, summary_id)
        nomination = summary.nomination
        transporter = nomination.transporter
        offload = nomination.offload
        bm = transporter.bulk_money
        if offload.net_to_be_paid >= 0:
            bm = bm - offload.net_to_be_paid
            transporter.bulk_money = round(bm, 2)
            transporter.save()
        offload.dues_paid = True
        offload.save()
        return HttpResponseRedirect(reverse('admin:process_summary_change', args=(summary.id,)))  

    def stage(self, obj):
        return "Completed"
        
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.user_type == User.ADMIN:
                return True
        return False
    


#Summary Model for local currency
class SummaryInline(admin.TabularInline):
    exclude = ('is_deleted',)
    readonly_fields = [
        "nomination",
        "transit",
        "fullfillment"
    ]
    extra = 0
    model = Summary

@admin.register(SummaryInLocalCurrency)
class SummaryInLocalCurrencyAdmin(admin.ModelAdmin):    
    inlines = (NominationInline, TransitInline, FullfilmentInline,SummaryInline)
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
    )
    readonly_fields = (
        "nomination",
        "transit",
        "fullfillment",
    )
    exclude = ("is_deleted",)

   

    def transporter(self, obj):
        return obj.nomination.transporter

    def nomination_date(self, obj):
        return obj.nomination.created_at.date()

    def advance_cash(self, obj):
        cash = obj.nomination.advance_cash.all()
        total = 0
        for o in cash:
            amt = o.amount
            exchange_rate = o.local_exchange_rate
            if exchange_rate :
                amount = amt*exchange_rate
                total += amount
            else:
                exchange_rate = 1
                amount = amt*exchange_rate
                total += amount

        total = round(total, 2)
        return total


    def advance_fuel(self, obj):
        total = 0
        fuel = obj.nomination.advance_fuel.aggregate(total=Sum("local_net_amount"))
        if fuel['total']:
            total = round(fuel['total'], 2)
        return total

    def rate(self, obj):
        return obj.nomination.rate

    def vehicle(self, obj):
        return obj.nomination.vehicle

    def tanker(self, obj):
        return obj.nomination.tanker

    def customer(self, obj):
        return obj.nomination.customer

    def product(self, obj):
        return obj.nomination.product


    def advance_others(self, obj):
        others = obj.nomination.advance_others.all()
        total = 0
        for o in others:
            qty = o.quantity
            exchange_rate = o.local_exchange_rate
            amount = qty * o.unit_price * exchange_rate
            total += amount
        total = round(total, 2)
        return total

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
            return obj.transit.invoice_value_local
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
        if obj.fullfillment:
            return obj.fullfillment.off_loading_l20_quantity
        return None

    def offloading_date(self, obj):
        if obj.fullfillment:
            return obj.fullfillment.off_loading_date
        return None

    def shortage(self, obj):
        if obj.fullfillment:
            return obj.fullfillment.shortage
        return None

    def tolerance(self, obj):
        if obj.fullfillment:
            return obj.fullfillment.tolerance
        return None

    def net_shortage(self, obj):
        if obj.fullfillment:
            return obj.fullfillment.net_shortage
        return None

    def shortage_value(self, obj):
        if obj.fullfillment:
            return obj.fullfillment.shortage_value_local
        return None

    def net_to_be_paid(self, obj):
        if obj.fullfillment:
            return obj.fullfillment.net_to_be_paid_local
        return None

    def profitability(self, obj):
        if obj.fullfillment:
            return obj.fullfillment.profiltability_local
        return None

    def sales_approval(self, obj):
        return "Approved"
    
     

    def paid(self, obj):
        if obj.fullfillment and not obj.fullfillment.dues_paid:
            transporter = obj.nomination.transporter
            try:
                if transporter.bulk_money >= obj.fullfillment.net_to_be_paid:
                    return format_html(
                            "<p>Unpaid<p>"
                        )
            except Exception as e:
                pass
        elif obj.fullfillment and obj.fullfillment.dues_paid:
            return format_html(
                "<p>Paid<p>"
            )

        return "---"
 

    def stage(self, obj):
        return "Completed"
        
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.user_type == User.ADMIN:
                return True
        return False   


    
