from django.contrib import admin
from .models import Hostel, TypeLocality, Country, Person, Book, BookNumber, Pasportyst, Locality
# Register your models here.


admin.site.register(TypeLocality)
admin.site.register(Hostel)
admin.site.register(Country)
admin.site.register(Person)
admin.site.register(Book)
admin.site.register(BookNumber)
admin.site.register(Pasportyst)
admin.site.register(Locality)
