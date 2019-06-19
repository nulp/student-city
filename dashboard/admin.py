from django.contrib import admin
from .models import Hostel, TypeLocality, Country, Person, Book, Pasportyst, Locality, Region, District, \
    PersonHistory

# Register your models here.


admin.site.register(TypeLocality)
admin.site.register(Hostel)
admin.site.register(Country)
admin.site.register(Region)
admin.site.register(District)
admin.site.register(Person)
admin.site.register(PersonHistory)
admin.site.register(Book)
admin.site.register(Pasportyst)
admin.site.register(Locality)
