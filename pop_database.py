import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BarTables.settings')

import django
django.setup()

from BarOpenTable.models import Location, Seat


def populate():

    loft_tables = [
        {'name': '1', 'capacity': '2'},
        {'name': '2', 'capacity': '2'},
        {'name': '3', 'capacity': '2'},
        {'name': '4', 'capacity': '2'},
        {'name': '5', 'capacity': '2'},
        {'name': '6', 'capacity': '2'},
        {'name': '7', 'capacity': '2'},
        {'name': '8', 'capacity': '2'},
        {'name': '9', 'capacity': '2'},
        {'name': '10', 'capacity': '2'},
        {'name': '11', 'capacity': '2'}
    ]

    main_bar_tables = [
        {'name': '12', 'capacity': '2'},
        {'name': '13', 'capacity': '2'},
        {'name': '14', 'capacity': '2'},
        {'name': '15', 'capacity': '2'},
        {'name': '16', 'capacity': '2'},
        {'name': '17', 'capacity': '2'},
        {'name': '18', 'capacity': '2'},
        {'name': '19', 'capacity': '2'},
        {'name': '20', 'capacity': '2'},
        {'name': '21', 'capacity': '2'},
        {'name': '22', 'capacity': '2'},
        {'name': '23', 'capacity': '2'},
        {'name': '24', 'capacity': '2'},
        {'name': '25', 'capacity': '2'},
        {'name': '26', 'capacity': '2'},
        {'name': '27', 'capacity': '2'},
        {'name': '28', 'capacity': '2'},
        {'name': '29', 'capacity': '2'},
        {'name': '30', 'capacity': '2'},
        {'name': '31', 'capacity': '2'},
        {'name': '32', 'capacity': '2'},
        {'name': '33', 'capacity': '2'},
        {'name': '34', 'capacity': '2'},
        {'name': '35', 'capacity': '2'}
    ]

    raised_tables = [
        {'name': '36', 'capacity': '2'},
        {'name': '37', 'capacity': '2'},
        {'name': '38', 'capacity': '2'},
        {'name': '39', 'capacity': '2'},
        {'name': '40', 'capacity': '2'},
        {'name': '41', 'capacity': '2'}
    ]

    foyer_tables = [
        {'name': '42', 'capacity': '2'},
        {'name': '43', 'capacity': '2'},
        {'name': '44', 'capacity': '2'},
        {'name': '45', 'capacity': '2'},
        {'name': '46', 'capacity': '2'},
        {'name': '47', 'capacity': '2'},
        {'name': '48', 'capacity': '2'},
        {'name': '49', 'capacity': '2'}
    ]

    venue_tables = [
        {'name': '50', 'capacity': '1'},
        {'name': '51', 'capacity': '1'},
        {'name': '52', 'capacity': '1'},
        {'name': '53', 'capacity': '1'},
        {'name': '54', 'capacity': '1'},
        {'name': '55', 'capacity': '1'},
        {'name': '56', 'capacity': '1'},
        {'name': '57', 'capacity': '1'},
        {'name': '58', 'capacity': '1'},
        {'name': '59', 'capacity': '1'},
        {'name': '60', 'capacity': '1'},
        {'name': '61', 'capacity': '1'},
        {'name': '62', 'capacity': '1'},
        {'name': '63', 'capacity': '1'},
        {'name': '64', 'capacity': '2'},
        {'name': '65', 'capacity': '2'},
        {'name': '66', 'capacity': '2'},
        {'name': '67', 'capacity': '2'},
        {'name': '68', 'capacity': '2'},
        {'name': '69', 'capacity': '2'},
        {'name': '70', 'capacity': '2'},
        {'name': '71', 'capacity': '2'},
        {'name': '72', 'capacity': '2'},
        {'name': '73', 'capacity': '2'},
        {'name': '74', 'capacity': '2'},
        {'name': '75', 'capacity': '2'},
        {'name': '76', 'capacity': '2'}
    ]

    locs = {'Loft Area': {'seats': loft_tables},
            'Main Bar': {'seats': main_bar_tables},
            'Raised Area': {'seats': raised_tables},
            'Foyer': {'seats': foyer_tables},
            'Venue': {'seats': venue_tables}}

    for loc, loc_data in locs.items():
        l = add_loc(loc)
        for s in loc_data['seats']:
            add_seat(l, s['name'], s['capacity'])

    for l in Location.objects.all():
        for s in Seat.objects.filter(location=l):
            print(f'- {l}: {s}')


def add_seat(loc, name, cap):
    s = Seat.objects.get_or_create(name=name, location=loc, capacity=cap)[0]
    s.save()
    return s


def add_loc(name):
    l = Location.objects.get_or_create(name=name)[0]
    l.save()
    return l


if __name__ == '__main__':
    print("Starting")
    populate()
