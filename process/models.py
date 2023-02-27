from django.db import models
from TPL.models import UUIDModel
from components.models import *
from uuid import uuid4

# Create your models here.

class Summary(UUIDModel):
    nomination = models.ForeignKey("Nomination", on_delete=models.CASCADE, blank=True, null=True, related_name="nomination_summary")
    transit = models.ForeignKey("Transit", on_delete=models.CASCADE, blank=True, null=True, related_name="transit_summary")
    fullfillment = models.ForeignKey("Fullfillment", on_delete=models.CASCADE, blank=True, null=True, related_name="fullfillment_summary")
    
    

class Fullfillment(UUIDModel):
    off_loading_date = models.DateField()
    off_loading_l20_quantity = models.FloatField()
    shortage = models.FloatField(blank=True, null=True)
    tolerance = models.FloatField(blank=True, null=True) # tol_product * loading_qty
    net_shortage = models.FloatField(blank=True, null=True) # shortahge - tolerance, neg == 0, +ve
    shortage_value = models.FloatField(blank=True, null=True) # net_shoratge * product_cost
    net_to_be_paid = models.FloatField(blank=True, null=True) # invoice_value - all_advance - shortage
    profiltability = models.FloatField(blank=True, null=True) # (customer_price * l20_loaded) - invoice_value
    dues_paid = models.BooleanField(default=False)
    summary = models.ForeignKey("Summary", on_delete=models.SET_NULL, blank=True, null=True, related_name="summary_offload")
    is_deleted = models.BooleanField(default=False)

class Transit(UUIDModel):
    loading_date = models.DateField()
    loading_base_quantity = models.FloatField()
    locading_l20_quantity = models.FloatField()
    release_date = models.DateField()
    invoice_value = models.FloatField(default=0)
    invoice_number = models.CharField(null=True, blank=True, max_length=50)
    invoice_date = models.DateField(blank=True, null=True)
    fullfillment = models.ForeignKey(Fullfillment, on_delete=models.SET_NULL, related_name="transit", blank=True, null=True)
    # loading_depot = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="transit")
    summary = models.ForeignKey("Summary", on_delete=models.SET_NULL, blank=True, null=True, related_name="summary_transit")
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
    transit = models.ForeignKey(Transit, on_delete=models.SET_NULL, related_name="nomination", blank=True, null=True)
    offload = models.ForeignKey(Fullfillment, on_delete=models.SET_NULL, related_name="nomination", blank=True, null=True)


class AdvanceOthers(UUIDModel):
    nomination = models.ForeignKey(Nomination, on_delete=models.CASCADE, related_name="advance_others")
    sellable = models.ForeignKey(Sellables, on_delete=models.CASCADE, related_name="advance_others")
    quantity = models.FloatField()

    def save(self, *args, **kwargs):
        # set nomination status to validation pending
        nomination = self.nomination
        nomination.nomination_status = Nomination.VALIDATION_PENDING
        nomination.save()
        super().save(*args, **kwargs)


class AdvanceCash(UUIDModel):
    nomination = models.ForeignKey(Nomination, on_delete=models.CASCADE, related_name="advance_cash")
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="advance_cash")
    amount = models.FloatField()

    def save(self, *args, **kwargs):
        # set nomination status to validation pending
        nomination = self.nomination
        nomination.nomination_status = Nomination.VALIDATION_PENDING
        nomination.save()
        super().save(*args, **kwargs)
    

class AdvanceFuel(UUIDModel):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="advance_fuel")
    nomination = models.ForeignKey(Nomination, on_delete=models.CASCADE, related_name="advance_fuel")
    fuel_quantity = models.FloatField()

    def save(self, *args, **kwargs):
        # set nomination status to validation pending
        nomination = self.nomination
        nomination.nomination_status = Nomination.VALIDATION_PENDING
        nomination.save()
        super().save(*args, **kwargs)



    # off_loading_depot = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="fullfillment")


# class Demurrage(UUIDModel):
#     VALIDATION_PENDING = "validation_pending"
#     APPROVAL_PENDING = "approval_pending"
#     APPROVED = "approved"

#     DEMURRAGE_STATUS_CHOICES = (
#         (VALIDATION_PENDING, "Validation Pening"),
#         (APPROVAL_PENDING, "Approval Pending"),
#         (APPROVED, "Approved"),
#     )

