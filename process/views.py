from django.shortcuts import render
from dal import autocomplete
from components.models import Vehicle
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

