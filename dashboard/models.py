from django.contrib.auth.models import User
from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Region(models.Model):
    # область
    name = models.CharField(db_index=True, max_length=256)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class District(models.Model):
    # район
    name = models.CharField(db_index=True, max_length=256)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class TypeLocality(models.Model):
    name = models.CharField(max_length=32)
    short = models.CharField(max_length=8)

    def __str__(self):
        return self.name


class Locality(models.Model):
    name = models.CharField(db_index=True, max_length=256)
    l_type = models.ForeignKey(TypeLocality, on_delete=models.SET_NULL, null=True)

    district = models.ForeignKey(District, on_delete=models.SET_NULL, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.l_type.short + ' ' + self.name

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
    # user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
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
    book_number = models.ForeignKey(BookNumber, on_delete=models.SET_NULL, null=True)
    pasportyst = models.ForeignKey(Pasportyst, on_delete=models.SET_NULL, null=True)
    hostel = models.ForeignKey(Hostel, on_delete=models.SET_NULL, null=True)
    note = models.TextField()

    @property
    def number(self):
        return self.book_number.number

    def __str__(self):
        return str(self.book_number) + ' ' + str(self.pasportyst) + ' ' + str(self.hostel)


class Person(models.Model):

    def n_in_b(self):

        no = \
            Person.objects.filter(book__book_number_id=self.book.book_number_id).aggregate(
                models.Max('number_in_book'))[
                'number_in_book__max']

        if no is None:
            return 1
        else:
            return no + 1

    name = models.CharField(db_index=True, max_length=128)
    surname = models.CharField(db_index=True, max_length=128,)
    patronymic = models.CharField(db_index=True, max_length=128, blank=True, default="")

    birthday = models.DateField(db_index=True)

    unique_number = models.CharField(max_length=256, blank=True, null=True)
    passport_number = models.CharField(max_length=32, blank=False, null=True)
    passport_authority = models.CharField(max_length=128, blank=False, null=True)
    date_of_issue = models.DateField(blank=False, null=True)

    registered_date = models.DateField(db_index=True, null=True)
    de_registered_date = models.DateField(db_index=True, null=True, blank=True)
    new_address = models.CharField(max_length=256, default='', blank=True)

    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    number_in_book = models.IntegerField(default=0, blank=True)
    pasportyst = models.ForeignKey(Pasportyst, on_delete=models.SET_NULL, null=True)

    locality = models.ForeignKey(Locality, on_delete=models.SET_NULL, null=True)

    hostel = models.ForeignKey(Hostel, on_delete=models.SET_NULL, null=True)
    room = models.CharField(max_length=32, null=True, blank=True)

    created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="persons_created", default=None,
                                   null=True)
    updated = models.DateField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="persons_updated", default=None,
                                   null=True)

    note = models.TextField(blank=True)

    def __str__(self):
        return self.name + ' ' + self.surname


class PersonHistory(models.Model):
    person_id = models.PositiveIntegerField(db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    data = models.TextField()


class DeletedPerson(models.Model):
    person_id = models.PositiveIntegerField(db_index=True)
