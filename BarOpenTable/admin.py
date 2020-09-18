from django.contrib import admin
from BarOpenTable.models import UserProfile, Location, Seat, Customer


class LocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Location, LocationAdmin)
admin.site.register(UserProfile)
admin.site.register(Seat)
admin.site.register(Customer)
