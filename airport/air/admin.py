from django.contrib import admin

# Register your models here.
from .models import *


class AirportAdmin(admin.ModelAdmin):
    list_display = ('id','airportname')
    list_display_links = ('id','airportname')


class FlightRaceAdmin(admin.ModelAdmin):
    list_display = ('id','RaceNumber','From','To','Price')
    list_display_links = ('id','RaceNumber')


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id','companyname')
    

class AirPlaneAdmin(admin.ModelAdmin):
    list_display = ('id','planenumber','company')
    

class FlightAdmin(admin.ModelAdmin):
    list_display = ('id','Race','startTime','plane')


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id','flight','seat','available','buyer')
    list_display_links = ('id','flight','buyer')

    
admin.site.register(Airport, AirportAdmin)
admin.site.register(FlightRace, FlightRaceAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(AirPlane, AirPlaneAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Ticket, TicketAdmin)
