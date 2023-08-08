from django.urls import path
from . import views

app_name = "predict"

urlpatterns = [
    path('predictor/', views.predict, name='prediction_page'),
    path('predict/', views.predict_chances, name='submit_prediction'),
    path('results/', views.view_results, name='results'),
    path('about/',views.view_about,name='about'),
    path('doctor/',views.view_doctor,name='doctor'),
    path('register/', views.register_request, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name= 'logout'),
    path('', views.home_request, name= 'home'),

]
