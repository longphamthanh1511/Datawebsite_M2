from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('tank/',views.tank_water_chart, name='tank_water_chart'),
    path('refill_tank/', views.refill_tank, name='refill_tank'),
    path('drain_tank_chart/', views.drain_tank_chart, name='drain_tank_chart'),
    path('drain_tank/', views.drain_tank, name='drain_tank'),
    path('mail/', views.send_mail_page, name='send_mail_page'),
    path('upload/<str:time>/<str:temperature>/<str:humidity>/<str:soil_temperature>/<str:soil_humidity>/<str:soil_pH>/<str:soil_EC>/<str:input_ph>/<str:input_ec>/<str:drain_ph>/<str:drain_ec>/<str:plant_weight>/<str:input_weight>/<str:drain_weight>/'
, views.upload_data, name='upload_data'),
    
]