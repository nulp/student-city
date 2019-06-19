from django import forms
from .models import Person, Book, PersonHistory, Country, Region, Locality, District
from  .serializers import PersonTableSerializer


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name']


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['name', 'country']


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = ['name', 'region']


class LocalityForm(forms.ModelForm):
    class Meta:
        model = Locality
        fields = ['name', 'type_locality', 'district', 'region']


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ['surname', 'name', 'patronymic', 'birthday', 'unique_number', 'passport_number',
                  'passport_authority',
                  'date_of_issue', 'registered', 'registered_period', 'continued_period', 'continued', 'de_registered', 'new_address',
                  'pasportyst',
                  'locality', 'hostel', 'room', 'note', 'book']

    # def clean_name(self):
    #     data = self.cleaned_data['name']
    #     # if "fred@example.com" not in data:
    #     #     raise forms.ValidationError("You have forgotten about Fred!")
    #
    #     return data

    def save(self, commit=True):
        person = super(PersonForm, self).save(commit=False)
        # do custom stuff

        if commit:
            person.save()
        return person
