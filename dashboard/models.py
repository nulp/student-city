from django.contrib.auth.models import User
from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Region(models.Model):
    # область
    name = models.CharField(db_index=True, max_length=256)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


    class Meta:
        ordering = ['name']


class District(models.Model):
    # район
    name = models.CharField(db_index=True, max_length=256)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class TypeLocality(models.Model):
    name = models.CharField(max_length=32)
    short = models.CharField(max_length=8)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Locality(models.Model):
    name = models.CharField(db_index=True, max_length=256)
    type_locality = models.ForeignKey(TypeLocality, on_delete=models.SET_NULL, null=True)

    district = models.ForeignKey(District, on_delete=models.SET_NULL, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.type_locality.short + ' ' + self.name

    class Meta:
        ordering = ['name']

    @property
    def full_locality(self):
        country_name = self.region.country.name
        region_name = self.region.name
        short_type_l = self.type_locality.short
        if self.district:
            district_name = ' ' + self.district.name + ','
        else:
            district_name = ''
        return f"{country_name}, {region_name},{district_name} {short_type_l} {self.name}"


class Hostel(models.Model):
    number = models.CharField(max_length=16)
    address = models.CharField(max_length=256)

    def __str__(self):
        return "№" + self.number


class Pasportyst(models.Model):
    name = models.CharField(max_length=256)
    active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    number = models.CharField(max_length=64)
    hostel = models.ForeignKey(Hostel, on_delete=models.SET_NULL, null=True)
    
    note = models.TextField()

    def __str__(self):
        return '(г. №' + self.hostel.number + ') ' + str(self.number)

    class Meta:
        ordering = ['hostel_id', 'number']


class PersonQuerySet(models.QuerySet):
    def active(self):
        return self.filter(deleted=False)

    def deleted(self):
        return self.filter(deleted=True)

    def any(self):
        return self


class PersonManager(models.Manager):
    def get_queryset(self):
        return PersonQuerySet(self.model, using=self._db)

    def editors(self):
        return

    def active(self):
        return self.get_queryset().active()

    def deleted(self):
        return self.get_queryset().deleted()

    def any(self):
        return self.get_queryset().any()


class Person(models.Model):

    name = models.CharField(db_index=True, max_length=128)
    surname = models.CharField(db_index=True, max_length=128,)
    patronymic = models.CharField(db_index=True, max_length=128, blank=True, default="")

    birthday = models.DateField(db_index=True)

    unique_number = models.CharField(max_length=256, blank=True, null=True)
    passport_number = models.CharField(max_length=32, blank=False, null=True)
    passport_authority = models.CharField(max_length=128, blank=False, null=True)
    date_of_issue = models.DateField(blank=False, null=True)

    registered = models.DateField(db_index=True, null=True)
    registered_period = models.DateField(db_index=True, null=True, blank=True)
    continued = models.DateField(db_index=True, null=True, blank=True)
    continued_period = models.DateField(db_index=True, null=True, blank=True)
    de_registered = models.DateField(db_index=True, null=True, blank=True)

    old_address = models.CharField(max_length=256, default='', null=True, blank=True)
    new_address = models.CharField(max_length=256, default='', null=True, blank=True)

    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
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

    deleted = models.BooleanField(default=False)
    deleted_time = models.DateTimeField(auto_now=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # sex = models.CharField(max_length=1, default="Ч")

    note = models.TextField(blank=True)

    people = PersonManager()
    objects = models.Manager()

    @property
    def book_number(self):
        if self.book:
            return self.book.number
        else:
            return None


    @property
    def short_name(self):
        p = ''
        if self.patronymic:
            p = ' ' + self.patronymic[0] + '. '
        return f"{self.surname} {self.name[0]}.{p}"

    @property
    def full_name(self):
        p = ''
        if self.patronymic:
            p = ' ' + self.patronymic + ' '
        return f"{self.surname} {self.name}{p}"

    def __str__(self):
        return self.name + ' ' + self.surname


class PersonHistory(models.Model):
    person_id = models.PositiveIntegerField(db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data = models.TextField()


class DeletedPerson(models.Model):
    person_id = models.PositiveIntegerField(db_index=True)
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
