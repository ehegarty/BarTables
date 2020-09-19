from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from BarOpenTable.models import Location, Seat, Customer
from django.contrib.auth import authenticate, login, logout


def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('seating'))
            else:
                return HttpResponse("Account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'index.html')


def bar_seating(request):
    if request.user.is_authenticated:
        if 'flip' in request.POST:
            area = request.POST['flip']
            location = Location.objects.get(name=area)
            location.is_open = not location.is_open
            location.save()
            context_dict = build_areas_context(request)
        elif 'loc' in request.POST:
            cap = request.POST['cap']
            loc = request.POST['loc']
            tab = request.POST['tab']
            guests = []
            for x in range(int(cap)):
                temp_first = request.POST['firstname' + str(x + 1)]
                temp_last = request.POST['lastname' + str(x + 1)]
                temp_num = request.POST['usernum' + str(x + 1)]
                if ('under' + str(x + 1)) in request.POST:
                    temp_18 = True
                else:
                    temp_18 = False
                temp = {'first_name': temp_first, 'last_name': temp_last, 'num': temp_num, 'under': temp_18}
                if temp['first_name']:
                    guests.append(temp)
            location = Location.objects.get(name=loc)
            seat = Seat.objects.get(name=tab)
            person = 1
            for guest in guests:
                Customer.objects.get_or_create(first_name=guest['first_name'],
                                               last_name=guest['last_name'],
                                               number=guest['num'],
                                               location=location,
                                               seat=seat,
                                               u18=guest['under'],
                                               person=person)
                person += 1
            seat.is_free = False
            seat.save()
            context_dict = build_areas_context(request)
        elif 'loc_out' in request.POST:
            loc = request.POST['loc_out']
            tab = request.POST['tab_out']
            location = Location.objects.get(name=loc)
            seat = Seat.objects.get(name=tab)
            seat.is_free = True
            seat.save()

            guests = Customer.objects.filter(location=location, seat=seat).order_by('-time_in')
            if len(guests) > 0:
                start = guests[0].person
                for guest in guests:
                    if guest.person == start:
                        guest.person = -1
                        guest.save()
                    else:
                        break
                    start -= 1
            context_dict = build_areas_context(request)
        else:
            context_dict = build_areas_context(request)

        return render(request, 'bar_seating.html', context=context_dict)
    else:
        return redirect(reverse('index'))


def show_location(request, location_slug):
    context_dict = {}
    try:
        location = Location.objects.get(slug=location_slug)
        seats = Seat.objects.filter(location=location)

        context_dict['location'] = location
        tables = []
        for seat in seats:
            temp = {'name': seat.name, 'is_free': seat.is_free, 'capacity': seat.capacity}
            places = []
            for x in range(seat.capacity):
                places.append(1)
            temp['places'] = places
            tables.append(temp)
        context_dict['seats'] = tables
    except Location.DoesNotExist:
        context_dict['location'] = None
        context_dict['seats'] = None

    return render(request, 'location.html', context=context_dict)


def build_areas_context(request):
    user = request.user.userprofile
    user_role = user.role
    locations = Location.objects.all()

    areas = []
    for loc in locations:
        temp = {'name': loc.name, 'slug': loc.slug, 'is_open': loc.is_open}
        seats = Seat.objects.filter(location=loc)
        free_seats = 0
        for seat in seats:
            if seat.is_free:
                free_seats += 1
        temp['free_seats'] = free_seats
        temp['occupied_seats'] = len(seats) - free_seats
        areas.append(temp)

    context_dict = {'manager': True if user.role == 'manager' else False,
                    'boldmessage': user_role,
                    'locations': areas
                    }
    return context_dict


def customers(request):
    if request.user.is_authenticated:
        user = request.user.userprofile
        if user.role == 'manager':
            if 'clear' in request.POST:
                Customer.objects.all().delete()
                guests = []
            else:
                guests = Customer.objects.all()
            context_dict = {'guests': guests}
            return render(request, 'customers.html', context=context_dict)
        else:
            return redirect(reverse('seating'))
    else:
        return redirect(reverse('index'))


def settings(request):
    if request.user.is_authenticated:
        user = request.user.userprofile
        if user.role == 'manager':
            # max_seating = MaxCapacity.objects.all()[0].max
            user_role = user.role
            context_dict = {'boldmessage': user_role}
            return render(request, 'settings.html', context=context_dict)
        else:
            return redirect(reverse('seating'))
    else:
        return redirect(reverse('index'))


def user_logout(request):
    logout(request)
    return redirect(reverse('index'))
