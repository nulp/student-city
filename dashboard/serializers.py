from rest_framework import serializers
from .models import Person


class PersonTableSerializer(serializers.ModelSerializer):
    locality = serializers.SerializerMethodField()
    hostel = serializers.SerializerMethodField()
    book = serializers.SerializerMethodField()
    room = serializers.SerializerMethodField()
    pasportyst = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ('pasportyst', 'book',
                  'locality', 'hostel', 'room',
                  'id', 'name', 'surname', 'patronymic', 'birthday', 'unique_number', 'passport_number',
                  'passport_authority',
                  'date_of_issue', 'registered_date', 'de_registered_date', 'new_address', 'number_in_book',
                  'created', 'updated', 'note')

    def get_locality(self, obj):
        return obj.locality.full_locality

    def get_hostel(self, obj):
        return obj.hostel.number

    def get_book(self, obj):
        return obj.book.number

    def get_room(self, obj):
        return obj.room

    def get_pasportyst(self, obj):
        return obj.pasportyst.name
