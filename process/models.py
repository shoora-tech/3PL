from django.db import models
from TPL.models import UUIDModel
from components.models import *

# Create your models here.

class Fullfillment(UUIDModel):
    off_loading_date = models.DateField()
    off_loading_l20_quantity = models.FloatField()

class Transit(UUIDModel):
    loading_date = models.DateField()
    loading_base_quantity = models.FloatField()
    locading_l20_quantity = models.FloatField()
    release_date = models.DateField()
    fullfillment = models.ForeignKey(Fullfillment, on_delete=models.SET_NULL, related_name="transit", blank=True, null=True)
    # loading_depot = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="transit")




class Nomination(UUIDModel):
    VALIDATION_PENDING = "validation_pending"
    APPROVAL_PENDING = "approval_pending"
    APPROVED = "approved"

    NOMINATION_STATUS_CHOICES = (
        (VALIDATION_PENDING, "Validation Pening"),
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
    product_quantity = models.FloatField()
    product_cost = models.FloatField()
    expected_loading_date = models.DateField()
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
    transit = models.ForeignKey(Transit, on_delete=models.SET_NULL, related_name="nomination", blank=True, null=True)
    offload = models.ForeignKey(Fullfillment, on_delete=models.SET_NULL, related_name="nomination", blank=True, null=True)


class AdvanceOthers(UUIDModel):
    nomination = models.ForeignKey(Nomination, on_delete=models.CASCADE, related_name="advance_others")
    sellable = models.ForeignKey(Sellables, on_delete=models.CASCADE, related_name="advance_others")
    quantity = models.FloatField()


class AdvanceCash(UUIDModel):
    nomination = models.ForeignKey(Nomination, on_delete=models.CASCADE, related_name="advance_cash")
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="advance_cash")
    amount = models.FloatField()
    

class AdvanceFuel(UUIDModel):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="advance_fuel")
    nomination = models.ForeignKey(Nomination, on_delete=models.CASCADE, related_name="advance_fuel")
    fuel_quantity = models.FloatField()



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
