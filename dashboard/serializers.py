from rest_framework import serializers

from .models import Person, Country, Region, District, Locality, TypeLocality, Hostel, Pasportyst


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ['id', 'name']


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = ['id', 'name', 'country_id']


class DistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = ['id', 'name', 'region_id']


class LocalitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Locality
        fields = ['id', 'name', 'type_locality', 'district_id', 'region_id']


class TypeLocalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeLocality
        fields = ['id', 'short', 'name']


class HostelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostel
        fields = ['id', 'number', 'address']


class BookNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostel
        fields = ['id', 'number']


class PasportystSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pasportyst
        fields = ['id', 'name', 'active']


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class PersonTableSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    locality = serializers.SerializerMethodField()
    hostel = serializers.SerializerMethodField()
    book_number = serializers.SerializerMethodField()
    room = serializers.SerializerMethodField()
    pasportyst = serializers.SerializerMethodField()

    birthday = serializers.SerializerMethodField()
    date_of_issue = serializers.SerializerMethodField()
    registered = serializers.SerializerMethodField()
    registered_period = serializers.SerializerMethodField()
    continued = serializers.SerializerMethodField()
    continued_period = serializers.SerializerMethodField()
    de_registered = serializers.SerializerMethodField()
    hostel_address = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ('pasportyst', 'book_number',
                  'country', 'region', 'district', 'locality', 'hostel', 'room',
                  'id', 'name', 'surname', 'patronymic', 'birthday', 'unique_number', 'passport_number',
                  'passport_authority',
                  'date_of_issue', 'registered', 'registered_period', 'continued', 'continued_period', 'de_registered',
                  'new_address', 'old_address', 'hostel_address',
                  'created', 'updated', 'created_by', 'updated_by', 'note')

    def get_country(self, obj):
        if obj.locality and obj.locality.region and obj.locality.region.country:
            return obj.locality.region.country.name
        return '-'

    def get_region(self, obj):
        if obj.locality and obj.locality.region:
            return obj.locality.region.name
        return '-'

    def get_district(self, obj):
        if obj.locality and obj.locality.district:
            return obj.locality.district.name
        return '-'

    def get_locality(self, obj):
        if obj.locality:
            return obj.locality.type_locality.short + ' ' + obj.locality.name
        return '-'

    def get_birthday(self, obj):
        if obj.birthday:
            return obj.birthday.strftime('%d.%m.%Y')
        return '-'

    def get_date_of_issue(self, obj):
        if obj.date_of_issue:
            return obj.date_of_issue.strftime('%d.%m.%Y')
        return '-'

    def get_registered(self, obj):
        if obj.registered:
            return obj.registered.strftime('%d.%m.%Y')
        return '-'

    def get_registered_period(self, obj):
        if obj.registered_period:
            return obj.registered_period.strftime('%d.%m.%Y')
        return '-'

    def get_continued(self, obj):
        if obj.continued:
            return obj.continued.strftime('%d.%m.%Y')
        return '-'

    def get_continued_period(self, obj):
        if obj.continued_period:
            return obj.continued_period.strftime('%d.%m.%Y')
        return '-'

    def get_de_registered(self, obj):
        if obj.de_registered:
            return obj.de_registered.strftime('%d.%m.%Y')
        return '-'

    def get_created(self, obj):
        if obj.created:
            return obj.created.strftime('%d.%m.%Y')
        return '-'

    def get_created_by(self, obj):
        if obj.created_by:
            return str(obj.created_by)
        return '-'

    def get_hostel_address(self, obj):
        if obj.hostel:
            return obj.hostel.address
        return '-'

    def get_updated(self, obj):
        if obj.updated:
            return obj.updated.strftime('%d.%m.%Y')
        return '-'

    def get_updated_by(self, obj):
        if obj.updated_by:
            return str(obj.updated_by)
        return '-'

    def get_hostel(self, obj):
        return obj.hostel.number

    def get_book_number(self, obj):
        if obj.book_number:
            return obj.book_number
        return None

    def get_room(self, obj):
        return obj.room

    def get_pasportyst(self, obj):
        return obj.pasportyst.name

