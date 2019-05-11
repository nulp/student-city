from rest_framework import serializers

from .models import Person, Country, Region, District, Locality, TypeLocality, Hostel, BookNumber, Pasportyst


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
        fields = ['id', 'name', 'l_type', 'district_id', 'region_id']


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
    locality = serializers.SerializerMethodField()
    hostel = serializers.SerializerMethodField()
    book_number = serializers.SerializerMethodField()
    room = serializers.SerializerMethodField()
    pasportyst = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ('pasportyst', 'book_number',
                  'locality', 'hostel', 'room',
                  'id', 'name', 'surname', 'patronymic', 'birthday', 'unique_number', 'passport_number',
                  'passport_authority',
                  'date_of_issue', 'registered_date', 'de_registered_date', 'new_address', 'number_in_book',
                  'created', 'updated', 'note')

    def get_locality(self, obj):
        if obj.locality:
            return obj.locality.full_locality
        return '-'

    def get_hostel(self, obj):
        return obj.hostel.number

    def get_book_number(self, obj):
        return obj.book_number

    def get_room(self, obj):
        return obj.room

    def get_pasportyst(self, obj):
        return obj.pasportyst.name

