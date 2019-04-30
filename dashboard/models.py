from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Region(models.Model):
    # область
    name = models.CharField(db_index=True, max_length=256)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class District(models.Model):
    # район
    name = models.CharField(db_index=True, max_length=256)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TypeLocality(models.Model):
    name = models.CharField(max_length=32)
    short = models.CharField(max_length=8)

    def __str__(self):
        return self.name


class Locality(models.Model):
    name = models.CharField(db_index=True, max_length=256)
    l_type = models.ForeignKey(TypeLocality, on_delete=models.CASCADE)

    district = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def full_locality(self):
        country_name = self.region.country.name
        region_name = self.region.name
        district_name = self.region.name
        short_type_l = self.l_type.short
        if self.district:
            district_name = ' ' + self.district.name + ','
        return f"{country_name}, {region_name},{district_name} {short_type_l} {self.name}"


class Hostel(models.Model):
    number = models.CharField(max_length=16)
    address = models.CharField(max_length=256)

    def __str__(self):
        return "Гуртожиток №" + self.number


class Pasportyst(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    active = models.BooleanField(default=True)
    # editor = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class BookNumber(models.Model):
    number = models.CharField(max_length=16)

    def __str__(self):
        return self.number


class Book(models.Model):
    book_number = models.ForeignKey(BookNumber, on_delete=models.CASCADE)
    pasportyst = models.ForeignKey(Pasportyst, on_delete=models.CASCADE)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    note = models.TextField()

    @property
    def number(self):
        return self.book_number.number

    def __str__(self):
        return str(self.book_number) + ' ' + str(self.pasportyst) + ' ' + str(self.hostel)


class Person(models.Model):

    def n_in_b(self):

        no = \
        Person.objects.filter(book__book_number_id=self.book.book_number_id).aggregate(models.Max('number_in_book'))[
            'number_in_book__max']

        if no is None:
            return 1
        else:
            return no + 1

    name = models.CharField(db_index=True, max_length=128)
    surname = models.CharField(db_index=True, max_length=128)
    patronymic = models.CharField(db_index=True, max_length=128)

    birthday = models.DateField(db_index=True)

    unique_number = models.CharField(max_length=100, blank=False, null=True)
    passport_number = models.CharField(max_length=32, blank=False, null=True)
    passport_authority = models.CharField(max_length=128, blank=False, null=True)
    date_of_issue = models.DateField(blank=False, null=True)

    registered_date = models.DateField(db_index=True, null=True)
    de_registered_date = models.DateField(db_index=True, null=True)
    new_address = models.CharField(max_length=256, default='')

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    number_in_book = models.IntegerField(default=n_in_b)
    pasportyst = models.ForeignKey(Pasportyst, on_delete=models.CASCADE)

    locality = models.ForeignKey(Locality, on_delete=models.CASCADE)

    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    room = models.CharField(max_length=32, null=True)

    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    note = models.TextField()

    def __str__(self):
        return self.name + ' ' + self.surname
