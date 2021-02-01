from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserForm,DriverForm, DriveRequestForm
from django.http import HttpResponse
from .models import Driver,DriveRequest,ConfirmedDrive, User
from django.contrib import messages
import random

# Create your views here.

def index(request):
    cities = ['--SELECT YOUR CURRENT LOCATION--','Gandhipuram','Ukkadam','Singanallur','Ganapathy','Peelamedu','Kovaipudhur']
    vehicle_type = ['--SELECT TYPE OF VEHICLE--','Car','Auto','Bike','Traveller']
    destination =  ['--SELECT YOUR DESTINATION LOCATION--','Gandhipuram','Ukkadam','Singanallur','Ganapathy','Peelamedu','Kovaipudhur']
    if request.method == 'POST':
        form_request = DriveRequestForm(data=request.POST)
        if form_request.is_valid():
            ride_request = form_request.save(commit=False)
            ride_request.from_location = request.POST.getlist('start')[0]
            ride_request.to_location = request.POST.getlist('end')[0]
            ride_request.vehicle_preference = request.POST.getlist('vehicle_selected')[0]
            ride_request.save()
            print(ride_request.pk)
            return redirect(reverse('drive_request_status',args=[ride_request.pk]))
    else:
        request_form = DriveRequestForm()
        return render(request,'Taxi/user_home.html',{'request_form':request_form,'places':cities,'vehicle_types':vehicle_type,'destination':destination})


def captain_login(request):
    return render(request,'Taxi/captain_login.html')

def login_validation(request):
    username = request.POST['username']
    password = request.POST['userpassword']
    user = authenticate(request,username=username,password=password)
    if user is not None:
        if user.is_superuser:
            login(request, user)
            return redirect('administrator_home')
        else:
            login(request,user)
            return redirect('driver_home')
    else:
        return redirect('captain_login')

@login_required
def user_logout(request):
    logout(request)
    return redirect('captain_login')

@user_passes_test(lambda u: u.is_superuser)
def administrator_home(request):
    cities = ['--SELECT INITIAL LOCATION--','Gandhipuram','Ukkadam','Singanallur','Ganapathy','Peelamedu','Kovaipudhur']
    vehicle_type = ['--SELECT TYPE OF VEHICLE--','Car','Auto','Bike','Traveller']

    if request.method == 'POST':
        form_user = UserForm(data=request.POST)
        form_driver = DriverForm(data=request.POST)
        print(form_user.is_valid(),form_driver.is_valid())
        if form_user.is_valid() and form_driver.is_valid():
            user = form_user.save()
            user.set_password(user.password)
            user.save()
            driver = form_driver.save(commit=False)
            driver.user = user
            driver.current_location = request.POST.getlist('city', None)[0]
            driver.vehicle = request.POST.getlist('vehi', None)[0]
            driver.save()
            return redirect('administrator_home')
        else:
            messages.add_message(request, messages.INFO, 'Username Already Exist, Try Another Username')
            return redirect('administrator_home')
    else:
        form_user = UserForm()
        form_driver = DriverForm()
        return render(request,'Taxi/administrator_home.html',{'user_form':form_user,'driver_form':form_driver,'cities':cities,'vehicles':vehicle_type})


@user_passes_test(lambda u: u.is_superuser)
def delete_driver(request):
    return render(request,'Taxi/delete_driver.html')


@login_required
def driver_home(request):
    cities = ['Gandhipuram','Ukkadam','Singanallur','Ganapathy','Peelamedu','Kovaipudhur']
    if request.method=='POST':
        update_location=Driver.objects.get(user=request.user)
        update_location.current_location = request.POST.getlist('place')[0]
        update_location.save()
        return redirect('driver_home')
    else:
        driver_object = Driver.objects.get(user=request.user)
        location=driver_object.current_location
        cities.remove(location)
        cities.insert(0,location)
        customer_requests = DriveRequest.objects.filter(from_location=location,request_status=0)
        return render(request,'Taxi/driver_home.html',{'places':cities,'customer_requests':customer_requests})


def drive_request_status(request,pk):
    customer_object = DriveRequest.objects.get(pk=pk)
    if customer_object.request_status == 0 :
        return render(request,'Taxi/drive_request.html',{'customer':customer_object})
    else:
        return HttpResponse(pk)

def cancel_ride(request,pk):
    customer_object = DriveRequest.objects.get(pk=pk)
    customer_object.delete()
    return redirect('/')

def accept_ride(request,pk):
    customer_object = DriveRequest.objects.get(pk=pk)
    primarykey=pk
    OTP = random.randint(1000,9999)
    driver_object = Driver.objects.get(user=request.user)
    print(driver_object)
    confirmation_object = ConfirmedDrive.objects.get_or_create(
                            driver_username=driver_object,
                            request_id=pk,
                            customer_name=customer_object.customer_name,
                            customer_phone=customer_object.customer_phone,
                            from_location=customer_object.from_location,
                            to_location=customer_object.to_location,
                            one_time_password=OTP)
    customer_object.request_status = 1
    customer_object.save()
    confirmation=ConfirmedDrive.objects.filter(request_id=primarykey)[0]
    return render(request,'Taxi/accepted_rides.html',{'bill':confirmation})

def status_check(request):
    #print(request.method=='POST')
    if request.method=='POST':
        request_status_check = request.POST['requestid']
        print(DriveRequest.objects.filter(pk=request_status_check))
        try:
            customer_object = DriveRequest.objects.filter(pk=request_status_check)[0]
            if customer_object:
                if customer_object.request_status == 1:
                    confirmation_object = ConfirmedDrive.objects.filter(request_id=customer_object.pk)[0]
                    return render(request,'Taxi/ride_confirmation.html',{'confirmation':confirmation_object,'phone':confirmation_object.driver_username.phone_number})
                else:
                    return redirect(reverse('drive_request_status',args=[request_status_check]))
        except Exception as e:
            print(e)
            messages.add_message(request, messages.INFO, 'Request ID Does not Exist')
            return redirect('status_check')
    else:
        return render(request,'Taxi/status_check.html')

def current_ride(request):
    user_object = User.objects.get(username=request.user)
    print(user_object)
    driver_object = Driver.objects.get(user=user_object)
    print(driver_object)
    confirmed_ride_object = ConfirmedDrive.objects.filter(driver_username=driver_object)[0]
    print(confirmed_ride_object)
    primary=confirmed_ride_object.request_id
    return redirect(reverse('accept_ride',args=[primary]))

def otp_verify(request,pk):
    print(request.method =='POST')
    if request.method == 'POST':
        confirmation = ConfirmedDrive.objects.filter(pk=pk)[0]
        print("hello world")
        print(request.POST['otp'])
        if confirmation.one_time_password == request.POST['otp']:
            return HttpResponse("<h1>Have a Great Ride</h1>")
        else:
            messages.add_message(request, messages.INFO, 'OTP did not match')
            return redirect(reverse('otp_verify',args=[confirmation.pk]))
