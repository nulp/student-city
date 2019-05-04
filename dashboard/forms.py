from django import forms
from .models import Person


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['surname', 'name', 'patronymic', 'birthday', 'unique_number', 'passport_number',
             'passport_authority',
             'date_of_issue', 'registered_date', 'de_registered_date', 'new_address', 'book',
             'pasportyst',
             'locality', 'hostel', 'room', 'note']
