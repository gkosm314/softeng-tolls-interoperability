from django.urls import path
from . import views


#TODO: handle csv format admin/healthcheck?format=<response_format>'

urlpatterns = [
    path('admin/healthcheck', views.admin_healthcheck, name='healthcheck_url'),
    path('admin/resetpasses', views.admin_resetpasses, name='resetpasses_url'),
    path('admin/resetstations', views.admin_resetstations, name='resetstations_url'),
    path('admin/resetvehicles', views.admin_resetvehicles, name='resetvehicles_url'),
    path('admin/hardreset', views.admin_hardreset, name='hardreset_url'),

    path('login', views.obtain_auth_token, name = "login_url"), #this refers to the views imported from rest_framework.authtoken
    path('logout', views.logout_view, name = "logout_url"),
    path('PassesPerStation/<stationID>/<datefrom>/<dateto>', views.PassesPerStation.as_view(), name='passes_per_station'),
    path('PassesAnalysis/<op1_ID>/<op2_ID>/<datefrom>/<dateto>', views.PassesAnalysis.as_view(), name='passes_analysis'),
    path('PassesCost/<op1_ID>/<op2_ID>/<datefrom>/<dateto>', views.PassesCost.as_view(), name='passes_analysis'),
    path('ChargesBy/<op_ID>/<datefrom>/<dateto>', views.ChargesBy.as_view(), name='passes_analysis'),
]
