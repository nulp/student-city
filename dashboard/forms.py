from django import forms
from .models import Person, BookNumber, Book, PersonHistory
from  .serializers import PersonTableSerializer


class PersonForm(forms.ModelForm):
    book_number = forms.ModelChoiceField(queryset=BookNumber.objects.all())

    class Meta:
        model = Person
        fields = ['surname', 'name', 'patronymic', 'birthday', 'unique_number', 'passport_number',
                  'passport_authority',
                  'date_of_issue', 'registered_date', 'de_registered_date', 'new_address',
                  'pasportyst',
                  'locality', 'hostel', 'room', 'note']

    # def clean_name(self):
    #     data = self.cleaned_data['name']
    #     # if "fred@example.com" not in data:
    #     #     raise forms.ValidationError("You have forgotten about Fred!")
    #
    #     return data

    def save(self, commit=True):
        person = super(PersonForm, self).save(commit=False)
        # do custom stuff

        book, _ = Book.objects.get_or_create(book_number_id=self.cleaned_data.get('book_number').id,
                                             pasportyst_id=self.cleaned_data.get('pasportyst').id,
                                             hostel_id=self.cleaned_data.get('hostel').id)
        person.book = book

        if person.number_in_book is None or person.number_in_book == 0:
            person.number_in_book = person.n_in_b()

        if commit:
            person.save()
        return person
