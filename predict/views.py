from django.shortcuts import render, redirect
from django.http import JsonResponse
import pandas as pd
from .models import PredResults
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout

def home_request(request):
    return render(request, 'home.html')
    
def predict(request):
    return render(request, 'predict.html')


def predict_chances(request):

    if request.POST.get('action') == 'post':

        # Receive data from client
        Patient_ID = int(request.POST.get('Patient_ID'))
        Patient_Age = int(request.POST.get('Patient_Age'))
        Patient_Gender = int(request.POST.get('Patient_Gender'))
        Patient_Blood_Pressure = int(request.POST.get('Patient_Blood_Pressure'))
        Patient_Heartrate = int(request.POST.get('Patient_Heartrate'))

        # Unpickle model
        model = pd.read_pickle(r"new_model.pickle")
        # Make prediction
        result = model.predict([[Patient_ID, Patient_Age, Patient_Gender, Patient_Blood_Pressure, Patient_Heartrate]])

        Heart_Disease = result[0]

        PredResults.objects.create(Patient_ID=Patient_ID, Patient_Age=Patient_Age, Patient_Gender=Patient_Gender,
                                   Patient_Blood_Pressure=Patient_Blood_Pressure, Patient_Heartrate=Patient_Heartrate, Heart_Disease=Heart_Disease)

        return JsonResponse({'result': Heart_Disease, 'Patient_ID': Patient_ID,
                             'Patient_Age': Patient_Age, 'Patient_Gender': Patient_Gender, 'Patient_Blood_Pressure': Patient_Blood_Pressure, 'Patient_Heartrate': Patient_Heartrate},
                            safe=False)


def view_results(request):
    # Submit prediction and show all
    data = {"dataset": PredResults.objects.all()}
    return render(request, "results.html", data)

def view_about(request):
    return render(request, 'about.html')


def view_doctor(request):
    return render(request, 'doctor.html')

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("predict:prediction_page")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm
	return render (request=request, template_name="register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("predict:prediction_page")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.")
	return render(request,"home.html")
