from django.shortcuts import render
from dal import autocomplete
from components.models import Vehicle, Tanker , Driver
# Create your views here.


class TransporterVehicleView(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Vehicle.objects.none()
        transporter = self.forwarded.get("transporter", None)
        if transporter:
            qs = Vehicle.objects.filter(transporter=transporter)
        else:
            qs =  Vehicle.objects.none()
        if self.q:
            qs = Vehicle.objects.filter(vehicle_number__icontains=self.q)
        return qs
    
class TransporterTankerView(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Tanker.objects.none()
        transporter = self.forwarded.get("transporter", None)
        if transporter:
            qs = Tanker.objects.filter(transporter=transporter)
        else:
            qs =  Tanker.objects.none()
        if self.q:
            qs = Tanker.objects.filter(tanker_number__icontains=self.q)
        return qs



class TransporterDriverView(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Driver.objects.none()
        transporter = self.forwarded.get("transporter", None)
        if transporter:
            qs = Driver.objects.filter(transporter=transporter)
        else:
            qs =  Driver.objects.none()
        if self.q:
            qs = Driver.objects.filter(driver_name__icontains=self.q)
        return qs

