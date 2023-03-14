from django.db import models
from TPL.models import UUIDModel
from components.models import *
from uuid import uuid4
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class SummaryInLocalCurrency(UUIDModel):
    nomination = models.ForeignKey("Nomination", on_delete=models.CASCADE, blank=True, null=True, related_name="nomination_summary_local")
    transit = models.ForeignKey("Transit", on_delete=models.CASCADE, blank=True, null=True, related_name="transit_summary_local")
    fullfillment = models.ForeignKey("Fullfillment", on_delete=models.CASCADE, blank=True, null=True, related_name="fullfillment_summary_local")
    summary = models.ForeignKey("Summary", on_delete=models.CASCADE, blank=True, null=True, related_name="summary_local")

    class Meta:
        verbose_name_plural = "Summary In Local Currency"

class Summary(UUIDModel):
    nomination = models.ForeignKey("Nomination", on_delete=models.CASCADE, blank=True, null=True, related_name="nomination_summary")
    transit = models.ForeignKey("Transit", on_delete=models.CASCADE, blank=True, null=True, related_name="transit_summary")
    fullfillment = models.ForeignKey("Fullfillment", on_delete=models.CASCADE, blank=True, null=True, related_name="fullfillment_summary")
    summary_in_local_currency = models.ForeignKey("SummaryInLocalCurrency", on_delete=models.SET_NULL, blank=True, null=True, related_name="local_summary")
    is_deleted = models.BooleanField(default=False)


    class Meta:
        verbose_name_plural = "Summary"
    
    

class Fullfillment(UUIDModel):
    off_loading_date = models.DateField()
    off_loading_l20_quantity = models.FloatField()
    product_cost = models.FloatField(default=0, verbose_name="Product Cost (USD)")
    local_exchange_rate = models.FloatField(default=1)
    shortage = models.FloatField(blank=True, null=True)
    tolerance = models.FloatField(blank=True, null=True) # tol_product * loading_qty
    net_shortage = models.FloatField(blank=True, null=True) # shortahge - tolerance, neg == 0, +ve
    shortage_value = models.FloatField(blank=True, null=True) # net_shoratge * product_cost
    shortage_value_local = models.FloatField(blank=True, null=True)
    net_to_be_paid = models.FloatField(blank=True, null=True) # invoice_value - all_advance - shortage
    net_to_be_paid_local = models.FloatField(blank=True, null=True)
    profiltability = models.FloatField(blank=True, null=True) # (customer_price * l20_loaded) - invoice_value
    profiltability_local = models.FloatField(blank=True, null=True)
    dues_paid = models.BooleanField(default=False)
    summary = models.ForeignKey("Summary", on_delete=models.SET_NULL, blank=True, null=True, related_name="summary_offload")
    summary_in_local_currency = models.ForeignKey("SummaryInLocalCurrency", on_delete=models.SET_NULL, blank=True, null=True, related_name="local_summary_offload")
    is_deleted = models.BooleanField(default=False)

class Transit(UUIDModel):
    loading_date = models.DateField()
    loading_base_quantity = models.FloatField()
    locading_l20_quantity = models.FloatField()
    release_date = models.DateField()
    invoice_value = models.FloatField(default=0)
    invoice_value_local = models.FloatField(default=0)
    invoice_number = models.CharField(null=True, blank=True, max_length=50)
    invoice_date = models.DateField(blank=True, null=True)
    fullfillment = models.ForeignKey(Fullfillment, on_delete=models.SET_NULL, related_name="transit", blank=True, null=True)
    # loading_depot = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="transit")
    summary = models.ForeignKey("Summary", on_delete=models.SET_NULL, blank=True, null=True, related_name="summary_transit")
    summary_in_local_currency = models.ForeignKey("SummaryInLocalCurrency", on_delete=models.SET_NULL, blank=True, null=True, related_name="local_summary_transit")   
    is_deleted = models.BooleanField(default=False)



class Nomination(UUIDModel):
    VALIDATION_PENDING = "validation_pending"
    APPROVAL_PENDING = "approval_pending"
    APPROVED = "approved"

    NOMINATION_STATUS_CHOICES = (
        (VALIDATION_PENDING, "Validation Pending"),
        (APPROVAL_PENDING, "Approval Pending"),
        (APPROVED, "Approved"),
    )
    
    NOMINATION = "nomination"
    TRANSIT = "transit"
    OFFLOAD = "offload"

    STAGE_STATUS_CHOICES = (
        (NOMINATION, "Nomination"),
        (TRANSIT, "Transit"),
        (OFFLOAD, "Offloaded"),
    )
    transporter = models.ForeignKey(Transporter, on_delete=models.CASCADE, related_name="nomination")
    tanker = models.ForeignKey(Tanker, on_delete=models.CASCADE, related_name="nomination")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="nomination")
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="nomination")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="nomination")
    source = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="source_nomination")
    destination = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="destination_nomination")
    # advance = models.ManyToManyField(Advance, related_name="nomination")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="nomination")
    # product_quantity = models.FloatField()
    # tanker_capacity = models.FloatField(default=0)
    # product_cost = models.FloatField()
    expected_loading_date = models.DateField()
    summary = models.ForeignKey("Summary", on_delete=models.SET_NULL, blank=True, null=True, related_name="summary_nomination")
    summary_in_local_currency = models.ForeignKey("SummaryInLocalCurrency", on_delete=models.SET_NULL, blank=True, null=True, related_name="local_summary_nomination")
    is_deleted = models.BooleanField(default=False)
    nomination_status = models.CharField(
        choices=NOMINATION_STATUS_CHOICES,
        default=VALIDATION_PENDING,
        max_length=20
    )
    stage = models.CharField(
        choices=STAGE_STATUS_CHOICES,
        default=NOMINATION,
        max_length=20
    )
    sales_approved = models.BooleanField(default=False)
    rate = models.FloatField(default=0, null=True, blank=True, verbose_name="Rate (usd/ton)")
    local_exchange_rate = models.FloatField(default=1)
    transit = models.ForeignKey(Transit, on_delete=models.SET_NULL, related_name="nomination", blank=True, null=True)
    offload = models.ForeignKey(Fullfillment, on_delete=models.SET_NULL, related_name="nomination", blank=True, null=True)


class AdvanceOthers(UUIDModel):
    nomination = models.ForeignKey(Nomination, on_delete=models.CASCADE, related_name="advance_others")
    sellable = models.ForeignKey(Sellables, on_delete=models.CASCADE, related_name="advance_others")
    quantity = models.FloatField()
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="sellables", blank=True, null=True)
    exchange_rate = models.FloatField(default=1)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="sellables", blank=True, null=True)
    unit_price = models.FloatField(default=0)
    local_exchange_rate = models.FloatField(default=1)


    def save(self, *args, **kwargs):
        # set nomination status to validation pending
        nomination = self.nomination
        nomination.nomination_status = Nomination.VALIDATION_PENDING
        nomination.save()
        super().save(*args, **kwargs)


class AdvanceCash(UUIDModel):
    nomination = models.ForeignKey(Nomination, on_delete=models.CASCADE, related_name="advance_cash")
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="advance_cash")
    amount = models.FloatField(default=0)
    exchange_rate = models.FloatField(default=1)
    local_exchange_rate = models.FloatField(default=1)

    def save(self, *args, **kwargs):
        # set nomination status to validation pending
        nomination = self.nomination
        nomination.nomination_status = Nomination.VALIDATION_PENDING
        nomination.save()
        super().save(*args, **kwargs)
    

class AdvanceFuel(UUIDModel):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="advance_fuel")
    nomination = models.ForeignKey(Nomination, on_delete=models.CASCADE, related_name="advance_fuel")
    requested_fuel_quantity = models.FloatField(default=0)
    requested_date = models.DateField(blank=True, null=True)
    approved_fuel_quantity = models.FloatField(default=0)
    approved_date = models.DateField(blank=True, null=True)
    discount = models.FloatField(default=0)
    local_currency_discount = models.FloatField(default=0)
    net_amount = models.FloatField(default=0)
    local_net_amount = models.FloatField(default=0)
    fuel_price = models.FloatField(default=0)
    currency = models.ForeignKey(Currency,on_delete=models.CASCADE, blank=True, null=True)
    exchange_rate = models.FloatField(default=1)
    local_exchange_rate = models.FloatField(default=1)

    def save(self, *args, **kwargs):
        # set nomination status to validation pending
        nomination = self.nomination
        nomination.nomination_status = Nomination.VALIDATION_PENDING
        nomination.save()
        # calculate net amount after discount
        fd = 0
        discount_exchange=1
        local_discount_exchange = 1
        dm = DiscountMaster.objects.filter(station=self.station, transporter__nomination=nomination).last()
        if dm:
            fd = dm.fuel_discount
            discount_exchange = dm.exchange_rate
            local_discount_exchange = dm.local_exchange_rate

        fuel = Fuel.objects.filter(station=self.station).last()
        fuel_pr = self.fuel_price
        if fuel_pr : 
            fp = self.fuel_price
            exchange = self.exchange_rate
            amount = round(fp *(1/exchange),2)
            discount_per_liter = round(fd *(1/discount_exchange),2)
            net_amount = (amount - discount_per_liter) * self.approved_fuel_quantity
            self.discount = discount_per_liter
            self.net_amount = net_amount
            #calculation for local currency
            local_exchange = self.local_exchange_rate
            amt = round(fp*local_exchange,2)
            local_discount = round(fd*local_discount_exchange,2)
            local_amount = (amt - local_discount)*self.approved_fuel_quantity
            self.local_currency_discount = local_discount
            self.local_net_amount = local_amount

        else:     
            fp = fuel.fuel_price
            exchange = fuel.exchange_rate
            amount = round(fp *(1/exchange),2)
            # fd = dm.fuel_discount
            exchange = dm.exchange_rate
            discount_per_liter = round(fd *(1/exchange),2)
            net_amount = (amount - discount_per_liter) * self.approved_fuel_quantity
            self.discount = discount_per_liter
            self.net_amount = net_amount

            #calculation for local currency
            local_exchange = fuel.local_exchange_rate
            amt =round(fp*local_exchange,2)
            local_discount = round(fd*local_discount_exchange,2)
            local_amount = (amt - local_discount)*self.approved_fuel_quantity
            self.local_currency_discount = local_discount
            self.local_net_amount = local_amount

            
        super().save(*args, **kwargs)


