from .models import Hostel, Locality, Region, TypeLocality, Country, District, Book, Pasportyst, Person
from django.contrib.auth.models import User
from django.utils.text import slugify
from unidecode import unidecode
import csv

from django.utils.timezone import get_current_timezone
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from urllib.parse import urlparse, parse_qs, urlencode


def get_url_without_param(url, param='page'):
    u = urlparse(url)
    query = parse_qs(u.query)
    query.pop(param, None)
    u = u._replace(query=urlencode(query, True))
    u = u.geturl()
    if len(query) > 0:
        u += '&'
    else:
        u += '?'
    return u


def str2date(str_date, pattern='%Y-%m-%d'):
    tz = get_current_timezone()
    return tz.localize(datetime.strptime(str_date, pattern))


def date_delta_years(date, years):
    return date - relativedelta(years=years)


def get_default_person_order():
    order = ['surname', 'name', 'patronymic', 'birthday', 'unique_number', 'old_address', 'passport_number',
             'passport_authority',
             'date_of_issue', 'registered', 'registered_period', 'continued', 'continued_period', 'de_registered', 'new_address', 'book_number',
             'pasportyst',
             'country', 'region', 'district', 'locality',
             'hostel', 'hostel_address', 'room', 'created', 'created_by', 'updated', 'updated_by', 'note']

    return order


def get_ukrainian_person_field_names():
    names = {'id': '№',
             'name': 'Ім\'я',
             'surname': 'Прізвище',
             'patronymic': 'Побатькові',
             'birthday': 'Дата народження',
             'unique_number': 'Унікальний номер',
             'passport_number': 'Номер паспорта',
             'passport_authority': 'Орган видачі',
             'date_of_issue': 'Дата видачі',
             'registered': 'Дата реєстації',
             'registered_period': 'Термін реєстації',
             'continued': 'Дата продовження',
             'continued_period': 'Термін продовження',
             'de_registered': 'Дата зняття',
             'old_address': 'Звідки прибув',
             'new_address': 'Куди зараєст.',
             'book_number': 'Книга',
             'pasportyst': 'Паспортист',
             'country': 'Країна',
             'region': 'Область',
             'district': 'Район',
             'locality': 'Нас. Пункт',
             'hostel': 'Гурт.',
             'hostel_address': 'Адреса реєс.',
             'room': 'Кімната',
             'created': 'Створено',
             'created_by': 'Створив',
             'updated': 'Змінено',
             'updated_by': 'Змінив',
             'note': 'Примітка',
             'edited_by': 'Змінив',
             'edited_time': 'Час'}
    return names


def date_before_2000(s):
    c = s
    s = s.split(' ')
    l = s[0].split('/')
    if int(l[-1]) > 20:
        l[-1] = '19' + l[-1]
        l = '/'.join(l)
        s[0] = l
        s = ' '.join(s)
        res = datetime.strptime(s, "%m/%d/%Y %H:%M:%S").date()
    else:
        res = datetime.strptime(c, "%m/%d/%y %H:%M:%S").date()
    return res


def populate_hostels():
    with open('dashboard/old_data/Hostels-1.csv', mode='r') as infile:
        reader = csv.reader(infile)
        field_names = next(reader)
        for line in reader:
            d = {}
            for i, f in enumerate(field_names):
                d[f] = line[i]
            address = d["Address"] + ", б." + d["Number"]
            number = str(int(d["NameObject"].split("№")[-1]))
            Hostel.objects.get_or_create(address=address, number=number)


def populate_locs():
    country, _ = Country.objects.get_or_create(name="Україна")

    tls = (("місто", "м."),
           ("село", "с."),
           ("селище", "с-ще."),
           ("селище міського типу", "смт."))
    for name, short in tls:
        TypeLocality.objects.get_or_create(name=name, short=short)

    from .old_data.locations import locs

    for loc in locs:
        locality_name = loc[5]
        type_locality_name = loc[7]
        region_name = loc[13].split(' ')[0]
        district_name = loc[10].split(' ')[0]

        region, _ = Region.objects.get_or_create(country_id=country.id, name=region_name)

        type_locality, _ = TypeLocality.objects.get_or_create(name=type_locality_name)

        if district_name:
            district, _ = District.objects.get_or_create(name=district_name, region_id=region.id)
            Locality.objects.update_or_create(name=locality_name,
                                              region_id=region.id,
                                              type_locality=type_locality,
                                              district_id=district.id)
        else:
            Locality.objects.update_or_create(name=locality_name, region_id=region.id, type_locality=type_locality)


def populate_db():
    if Locality.objects.all().count() == 0:
        populate_locs()
        populate_hostels()

    b = {}

    year_now = datetime.today().year

    for i in range(1, 5):
        with open(f'dashboard/old_data/Books-{i}.csv', mode='r') as fb:
            books_reader = csv.reader(fb)
            books_fields = next(books_reader)

            lines = []
            for line in books_reader:
                b[line[0]] = {}
                lines.append(line)

            for j in range(1, len(books_fields)):
                f = books_fields[j]
                for line in lines:
                    b[line[0]][f] = line[j]

    for i in range(1, 5):
        with open(f'dashboard/old_data/Books-{i}.csv', mode='r') as fb, open('bad_locality_people.csv',
                                                                             'w') as bad_file:
            books_reader = csv.reader(fb)
            books_fields = next(books_reader)
            lines = []
            for line in books_reader:
                b[line[0]] = {}
                lines.append(line)

            for j in range(1, len(books_fields)):
                f = books_fields[j]
                for line in lines:
                    b[line[0]][f] = line[j]

            with open(f'dashboard/old_data/People-{i}.csv', mode='r') as fp:
                people_reader = csv.reader(fp)
                people_fields = next(people_reader)

                bad_file_w = csv.writer(bad_file)
                bad_file_w.writerow(people_fields)

                for line in people_reader:
                    d = {}
                    for j, f in enumerate(people_fields):
                        d[f] = line[j]

                    name = d['Name'].strip().capitalize()
                    surname = d["Surname"].strip().capitalize()
                    patronymic = d['Patron'].strip().capitalize()
                    birthday = date_before_2000(d['DateBirthday'])

                    unique_number = None
                    passport_number = None
                    passport_authority = None
                    date_of_issue = None

                    if len(d['Room']) > 4:
                        data = [e.strip() for e in d['Room'].split(',')]
                        if len(data) == 4:
                            unique_number, passport_number, passport_authority, date_of_issue = data
                            try:
                                date_of_issue = datetime.strptime(date_of_issue, "%d.%m.%y").date()
                            except:
                                try:
                                    date_of_issue = datetime.strptime(date_of_issue, "%d.%m.%Y").date()
                                except:
                                    unique_number += ', ' + date_of_issue
                                    date_of_issue = None
                        # elif len(data) == 3:
                        #     passport_number, passport_authority, date_of_issue = data
                        #     try:
                        #         date_of_issue = datetime.strptime(date_of_issue, "%d.%m.%y").date()
                        #     except:
                        #         try:
                        #             date_of_issue = datetime.strptime(date_of_issue, "%d.%m.%Y").date()
                        #         except:
                        #             unique_number = date_of_issue
                        #             date_of_issue = None
                        else:
                            unique_number = ', '.join(data)

                        room = None
                    else:
                        room = d['Room']

                    new_address = d['WhereOut']
                    # new_address = new_address.strip()

                    registered = date_before_2000(d['DatePropysky'])
                    try:
                        de_registered = date_before_2000(d['DateOut'])
                        if de_registered < registered and not new_address:
                            de_registered = None
                    except ValueError:
                        de_registered = None



                    number_in_book = int(d['NumberInBook'])

                    hostel_id = int(d['IdHostel'])

                    try:
                        created = date_before_2000(d['DateCreate'])
                    except:
                        created = registered
                    try:
                        updated = date_before_2000(d['DateEdit'])
                    except:
                        updated = None

                    note = d['TextNote']

                    bk = b[d['IdBook']]

                    officer_name = bk['Vidpovidalnyj'].strip()
                    book_note = bk['TextNote']
                    book_name = bk['NameBook']

                    user, _ = User.objects.get_or_create(username=slugify(unidecode(officer_name)),
                                                         password=slugify(unidecode(officer_name)) + '1')

                    pasportyst, _ = Pasportyst.objects.get_or_create(name=officer_name, active=True)
                    book, _ = Book.objects.get_or_create(number=book_name,
                                                         hostel_id=hostel_id)
                    book.note = book_note
                    book.save()

                    locality_country = d['Country']
                    locality_region_cat = d['RegionCat']
                    locality_region = d['Region']
                    locality_district_cat = d['DistrictCat']
                    locality_district = d['District']
                    locality_cat = d['Category']
                    locality_name = d['Locality']

                    try:
                        region = Region.objects.get(name=locality_region)
                        try:
                            district = District.objects.get(name=locality_district, region_id=region.id)
                            locality = Locality.objects.get(name=locality_name, district_id=district.id)
                        except:
                            locality = Locality.objects.get(name=locality_name, region_id=region.id)

                    except:
                        note += '\n' + ', '.join((locality_country, locality_region_cat, locality_region,
                                                  locality_district_cat, locality_district, locality_cat,
                                                  locality_name))
                        locality = None
                        # bad_file_w.writerow(line)
                        # continue

                    person, _ = Person.objects.update_or_create(
                        name=name,
                        surname=surname,
                        patronymic=patronymic,
                        birthday=birthday,
                        book=book,
                        # number_in_book=number_in_book,
                        pasportyst_id=pasportyst.id,
                        locality=locality,
                        hostel_id=hostel_id,
                        room=room,
                        created_by_id=user.id,
                        updated_by_id=user.id,
                    )

                    person.unique_number = unique_number
                    person.passport_number = passport_number
                    person.passport_authority = passport_authority
                    person.date_of_issue = date_of_issue
                    person.registered = registered
                    person.de_registered = de_registered
                    person.new_address = new_address
                    person.created = created
                    person.updated = updated
                    person.note = note
                    person.save()
