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
    
    class Meta:
        verbose_name_plural = "Currency Exchange"


class Product(UUIDModel):
    name = models.CharField(max_length=50)
    tolerance = models.FloatField(null=True, blank=True, verbose_name="Tolerance (%)")
    cost = models.FloatField(null=True, blank=True, verbose_name="Cost (USD)")

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
    name_in_bank_TZS_account = models.CharField(max_length=50,blank=True, null=True)
    bank_name_TZS_account = models.CharField(max_length=50,blank=True, null=True)
    swift_code_TZS_account = models.CharField(max_length=20,blank=True, null=True)
    account_number_TZS_account = models.IntegerField( blank=True, null=True)
    name_in_bank_USD_account = models.CharField(max_length=50,blank=True, null=True)
    bank_name_USD_account = models.CharField(max_length=50,blank=True, null=True)
    swift_code_USD_account = models.CharField(max_length=20,blank=True, null=True)
    account_number_USD_account = models.IntegerField( blank=True, null=True)

    def __str__(self):
        return self.name


class DiscountMaster(UUIDModel):
    transporter = models.ForeignKey(Transporter, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    fuel_discount = models.FloatField(default=0)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    

class Vehicle(UUIDModel):
    vehicle_number = models.CharField(max_length=10)
    transporter = models.ForeignKey(Transporter, on_delete=models.CASCADE)

    def __str__(self):
        return self.vehicle_number


class Tanker(UUIDModel):
    tanker_number = models.CharField(max_length=10)
    transporter = models.ForeignKey(Transporter, on_delete=models.CASCADE)

    def __str__(self):
        return self.tanker_number


class Driver(UUIDModel):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    passport_number = models.CharField(max_length=20, blank=True, null=True)
    passport_validity = models.DateField(blank=True, null=True)
    driving_license_number = models.CharField(max_length=50, blank=True, null=True)
    driving_license_validity = models.DateField(blank=True, null=True)
    transporter = models.ForeignKey(Transporter, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


class Customer(UUIDModel):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    location = models.ManyToManyField(Location, related_name="locations", blank=True)
    price = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Unit(UUIDModel):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Manufacturer(UUIDModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Sellables(UUIDModel):
    name = models.CharField(max_length=20)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name="sellable")
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="sellables")
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="sellables")
    unit_price = models.FloatField()

    def __str__(self):
        return self.name
