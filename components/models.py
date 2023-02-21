from django.db import models
from TPL.models import UUIDModel
from user.models import Organization
# Create your models here.

class Currency(UUIDModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Currencies"


class CurrencyExchange(UUIDModel):
    exchange_rate = models.IntegerField()
    from_currency = models.ForeignKey(Currency, related_name="from_currency", on_delete=models.CASCADE, blank=True, null=True)
    to_currency = models.ForeignKey(Currency, related_name="to_currency", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.exchange_rate} for {self.currency}"
    
    class Meta:
        verbose_name_plural = "Currency Exchange"


class Product(UUIDModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Company(UUIDModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Companies"


class Station(UUIDModel):
    name = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    contact_person = models.CharField(max_length=50)
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Fuel(UUIDModel):
    fuel_price = models.FloatField(default=0)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)


class Transporter(UUIDModel):
    name = models.CharField(max_length=50)
    poc_email = models.EmailField()
    poc_name = models.CharField(max_length=50)
    poc_phone = models.CharField(max_length=50)


class TransporterOrganizationFuel(UUIDModel):
    transporter = models.ForeignKey(Transporter, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    fuel_discount = models.FloatField(default=0)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)


class Vehicle(UUIDModel):
    vehicle_number = models.CharField(max_length=10)
    transporter = models.ForeignKey(Transporter, on_delete=models.CASCADE)


class Tanker(UUIDModel):
    tanker_number = models.CharField(max_length=10)
    transporter = models.ForeignKey(Transporter, on_delete=models.CASCADE)


class Driver(UUIDModel):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    transporter = models.ForeignKey(Transporter, on_delete=models.CASCADE)


class Location(UUIDModel):
    LOADING = "loading"
    UNLOADING = "unloading"

    LOCATION_TYPE_CHOICES = (
        (LOADING, "Loading"),
        (UNLOADING, "Unloading"),
    )
    name = models.CharField(max_length=150)
    location_type = models.CharField(
        choices=LOCATION_TYPE_CHOICES,
        default=UNLOADING,
        max_length=10
    )


class Customer(UUIDModel):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    location = models.ManyToManyField(Location, related_name="locations")

    def __str__(self):
        return self.name
