from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Booking
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from .forms import EmailLoginForm
from .forms import CustomSignUpForm
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404, redirect
from .models import Listing, Booking
from .forms import BookingForm
from datetime import datetime

def home(request):
    listings = Listing.objects.all()

    location = request.GET.get('location')
    guests = request.GET.get('guests')
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')

    if location:
        listings = listings.filter(location__icontains=location)

    if guests:
        listings = listings.filter(guest_capacity__gte=guests)

    if checkin and checkout:
        try:
            checkin_date = datetime.strptime(checkin, "%Y-%m-%d").date()
            checkout_date = datetime.strptime(checkout, "%Y-%m-%d").date()

            filtered_listings = []
            for listing in listings:
                overlaps = listing.bookings.filter(
                    check_in__lt=checkout_date,
                    check_out__gt=checkin_date
                ).exists()
                if not overlaps:
                    filtered_listings.append(listing)

            listings = filtered_listings
        except:
            pass

    return render(request, 'homes/home.html', {'listings': listings})


def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    form = BookingForm()
    error = None

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']
            guests = form.cleaned_data['guests']

            if guests > listing.guest_capacity:
                error = "Bu ev bu kadar kişi için uygun değil."
            else:
                existing_bookings = Booking.objects.filter(listing=listing)
                overlap = existing_bookings.filter(
                    check_in__lt=check_out,
                    check_out__gt=check_in
                ).exists()

                if overlap:
                    error = "Seçilen tarihlerde bu ev rezerve edilmiş."
                else:
                    booking = form.save(commit=False)
                    booking.user = request.user
                    booking.listing = listing
                    booking.save()
                    return redirect('home')

    return render(request, 'homes/detail.html', {
        'listing': listing,
        'form': form,
        'error': error
    })
def signup(request):
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            # UserProfile oluştur
            UserProfile.objects.create(
                user=user,
                phone_number=form.cleaned_data['phone_number'],
                id_or_passport_number=form.cleaned_data['id_or_passport_number']
            )

            login(request, user)
            return redirect('home')
    else:
        form = CustomSignUpForm()
    return render(request, 'homes/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            auth_login(request, user)
            return redirect('home')
    else:
        form = EmailLoginForm()
    return render(request, 'homes/login.html', {'form': form})

@login_required
def profile_view(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    reservations = Booking.objects.filter(user=user).order_by('-check_in')
    return render(request, 'homes/profile.html', {
        'user': user,
        'profile': profile,
        'reservations': reservations
    })

@login_required
def cancel_reservation(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    booking.delete()
    messages.success(request, "Reservation cancelled successfully.")
    return redirect('profile')