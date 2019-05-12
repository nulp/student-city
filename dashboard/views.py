from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Person, Locality, BookNumber, Hostel, Pasportyst, Country, Region, District, TypeLocality, \
    PersonHistory
from .forms import PersonForm
from .serializers import PersonTableSerializer

from .utils import populate_db, get_default_person_order, get_ukrainian_person_field_names, \
    str2date, get_url_without_param, date_delta_years
import datetime
import json

import operator
from functools import reduce


def pdb_test_view(request):
    populate_db()
    return HttpResponse("All done!")


@login_required
def person_view(request, pk):
    person = get_object_or_404(Person, pk=pk)
    history = PersonHistory.objects.filter(person_id=person.id)
    table_fields = ['surname', 'name', 'patronymic', 'birthday', 'unique_number', 'passport_number',
                     'passport_authority',
                     'date_of_issue', 'registered_date', 'de_registered_date', 'new_address', 'book_number', 'number_in_book',
                     'pasportyst',
                     'locality', 'hostel', 'room', 'created', 'updated', 'note']

    history = [p for p in history]
    for i, p in enumerate(history):
        row = []
        pd = json.loads(p.data)
        for f in table_fields:

            e = pd.get(f, None)
            if e is None:
                e = '-'
            row.append(e)
        history[i] = [p.edited_by, str(p.timestamp)] + row

    ukr_names = get_ukrainian_person_field_names()
    table_fields = ['edited_by', 'edited_time'] + table_fields
    ctx = {'person': person, 'history': history, 'table_fields': [ukr_names[x] for x in table_fields],}
    return render(request, template_name='person.html', context=ctx)


@login_required
def delete_person_view(request, pk):
    person = get_object_or_404(Person, pk=pk)

    person.deleted = True
    person.deleted_by_id = request.user.id
    person.save()

    return redirect('show_person', pk=pk)


# @login_required
# def person_history_view(request, pk):
#     person = get_object_or_404(Person, pk=pk)
#     return render(request, template_name='person.html', context={'person': person})


@login_required
def save_sidebar_view(request):
    if request.session.get('show_sidebar', False):
        request.session['show_sidebar'] = False
    else:
        request.session['show_sidebar'] = True

    return JsonResponse({'show': request.session['show_sidebar']})


@login_required
def edit_person_view(request, pk):
    person = get_object_or_404(Person, pk=pk)

    if person.deleted:
        raise Http404

    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            person = form.save()

            person.updated_by = request.user
            person.save()

            prev = PersonHistory.objects.filter(person_id=person.id).order_by('-timestamp').first()
            cur_text = json.dumps(PersonTableSerializer(person).data)
            if not prev or not prev.data == cur_text:
                PersonHistory.objects.create(person_id=person.id, data=cur_text, edited_by_id=request.user.id)

            messages.info(request, f"Запис №{person.id} змінено!")
            return redirect('show_person', pk=person.pk)
        else:
            person = form.cleaned_data

    districts = None
    regions = None
    localities = None

    if person.locality:
        regions = Region.objects.filter(country_id=person.locality.region.country_id)
        districts = District.objects.filter(region_id=person.locality.region_id)
        localities = Locality.objects.filter(region_id=person.locality.region_id,
                                             district_id=person.locality.district_id,
                                             l_type_id=person.locality.l_type_id)

    ctx = {
        'person': person,
        'book_numbers': BookNumber.objects.all(),
        'pasportysts': Pasportyst.objects.all(),
        'hostels': Hostel.objects.all(),
        'countries': Country.objects.all(),
        'districts': districts,
        'regions': regions,
        'type_localities': TypeLocality.objects.all(),
        'localities': localities,
    }

    return render(request, template_name='person_edit.html', context=ctx)


@login_required
def create_person_view(request):
    person = {}

    locality = None

    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save()

            person.created_by = request.user
            person.save()

            prev = PersonHistory.objects.filter(person_id=person.id).order_by('-timestamp').first()
            cur_text = json.dumps(PersonTableSerializer(person).data)
            if not prev or not prev.data == cur_text:
                PersonHistory.objects.create(person_id=person.id, data=cur_text, edited_by_id=request.user.id)

            messages.info(request, f"Запис №{person.id} створено!")
            return redirect('show_person', pk=person.pk)
        else:
            person = form.cleaned_data
            locality = person.get('locality', None)

    districts = None
    regions = None
    localities = None

    if locality is not None:
        regions = Region.objects.filter(country_id=locality.region.country_id)
        districts = District.objects.filter(region_id=locality.region_id)
        localities = Locality.objects.filter(region_id=locality.region_id,
                                             district_id=locality.district_id)

    ctx = {
        'person': person,
        'book_numbers': BookNumber.objects.all(),
        'pasportysts': Pasportyst.objects.all(),
        'hostels': Hostel.objects.all(),
        'countries': Country.objects.all(),
        'districts': districts,
        'regions': regions,
        'type_localities': TypeLocality.objects.all(),
        'localities': localities,
    }
    return render(request, template_name='person_create.html', context=ctx)


@login_required
def dashboard_view(request):
    request.GET = request.GET.copy()

    table_fields = request.session.get('table_fields', get_default_person_order())

    # list of filter queries from request
    person_filters = []

    # book_id from request
    book_id = request.GET.get('book')
    if book_id:
        try:
            book_id = int(book_id)
            if book_id != -1:
                person_filters.append(Q(book_id=book_id))
        except ValueError:
            pass

    # hostel_id from request
    hostel_id = request.GET.get('hostel')
    if hostel_id:
        try:
            hostel_id = int(hostel_id)
            if hostel_id != -1:
                person_filters.append(Q(hostel_id=hostel_id))
        except ValueError:
            pass

    # surname from request
    surname = request.GET.get('surname')
    if surname:
        if surname.strip():
            surname = surname.strip()
            surname = surname.capitalize()
            person_filters.append(Q(surname=surname))
        else:
            request.GET.pop('surname')

            # localized_str2date()

    # filter by birthday from request
    if request.GET.get('birth_check'):
        try:
            start_date = request.GET.get('birthday_start')
            str2date(start_date)
            end_date = request.GET.get('birthday_end')
            str2date(end_date)
            person_filters.append(Q(birthday__range=[start_date, end_date]))
        except:
            pass

    # filter by registration date from request
    if request.GET.get('reg_check'):
        try:
            start_date = request.GET.get('reg_start')
            str2date(start_date)
            end_date = request.GET.get('reg_end')
            str2date(end_date)
            person_filters.append(Q(registered_date__range=[start_date, end_date]))
        except:
            pass

    # filter by de_registration date from request
    if request.GET.get('de_reg_check'):
        try:
            start_date = request.GET.get('de_reg_start')
            str2date(start_date)
            end_date = request.GET.get('de_reg_end')
            str2date(end_date)
            person_filters.append(Q(de_registered_date__range=[start_date, end_date]))
        except:
            pass

    # filter by age on date from request
    if request.GET.get('age_one_check'):
        try:
            age_on = request.GET.get('age_on')
            age_on = str2date(age_on)
            age = int(request.GET.get('age'))

            start_date = date_delta_years(age_on, age + 1)
            end_date = date_delta_years(age_on, age)

            person_filters.append(Q(birthday__gt=start_date,
                                    birthday__lte=end_date))
        except:
            pass

    # filter by de_registration (if address is present) from request
    registered = request.GET.get('registered', '0')
    if registered == '0':
        person_filters.append(Q(new_address__exact=''))
        person_filters.append(Q(new_address__isnull=False))

    # get ordering from request and convert into list of params
    ordering = request.GET.get('ordering', '0')
    if ordering == '1':
        ordering = ['hostel_id', 'pasportyst_id', 'surname', 'name', 'patronymic']
    elif ordering == '2':
        ordering = ['hostel_id', 'registered_date', 'surname', 'name', 'patronymic']
    elif ordering == '3':
        ordering = ['hostel_id', 'de_registered_date', 'surname', 'name', 'patronymic']
    else:
        ordering = ['hostel_id', 'surname', 'name', 'patronymic']

    if request.GET.get('deleted', None) is not None:
        persons = Person.people.deleted()
    else:
        persons = Person.people.active()

    # getting person queryset based on order and filters
    if person_filters:
        if len(person_filters) > 1:
            filter_query = reduce(operator.and_, person_filters)
        else:
            filter_query = person_filters[0]
        persons = persons.filter(filter_query).order_by(*ordering)
    else:
        persons = persons.order_by(*ordering)

    if registered == '1':
        persons = persons.exclude(Q(new_address__isnull=True) | Q(new_address__exact=''))

    # results count
    person_count = persons.count()

    # pagination
    paginator = Paginator(persons, 100)
    page = request.GET.get('page')
    persons_paginator = paginator.get_page(page)

    # serialization of person
    persons = [p for p in persons_paginator]
    for i, p in enumerate(persons):
        row = []
        pd = PersonTableSerializer(p).data
        for f in table_fields:

            e = pd.get(f, None)
            if e is None:
                e = '-'
            row.append(e)

        row.append(f'data-id={pd.get("id")}')

        persons[i] = row

    # additional context data
    ukr_names = get_ukrainian_person_field_names()
    book_numbers = BookNumber.objects.all()
    hostels = Hostel.objects.all()
    path_without_page = get_url_without_param(request.get_full_path())

    ctx = {
        'persons': persons,
        'persons_paginator': persons_paginator,
        'persons_count': person_count,
        'table_fields': [ukr_names[x] for x in table_fields],
        'book_numbers': book_numbers,
        'hostels': hostels,
        'path_without_page': path_without_page,

    }
    return render(request=request, template_name="dashboard.html", context=ctx)


def logout_view(request):
    logout(request)
    return redirect('login')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if request.GET.get('next'):
                    return HttpResponseRedirect(request.GET.get('next'))
                else:
                    return redirect('main')

        # if form is not valid or user is None
        messages.error(request, "Будь ласка, введіть правильні ім'я користувача та пароль.")
        messages.error(request, "Зауважте, що обидва поля чутливі до регістру.")

    if request.user.is_authenticated:
        if request.GET.get('next'):
            return HttpResponseRedirect(request.GET.get('next'))
        else:
            return redirect('main')

    return render(request=request, template_name="login.html", context={})
