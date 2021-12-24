from django.urls import path
from . import views


#TODO: handle csv format admin/healthcheck?format=<response_format>'

urlpatterns = [
    # path('admin/healthcheck', views.admin_healthcheck, name='healthcheck_url'),
    # path('admin/resetpasses', views.admin_resetpasses, name='resetpasses_url'),
    # path('admin/resetstations', views.admin_resetstations, name='resetstations_url'),
    path('admin/resetvehicles', views.admin_resetvehicles, name='resetvehicles_url'),
    # path('admin/hardreset', views.admin_hardreset, name='hardreset_url'),

    # path('login', views.obtain_auth_token, name = "login_url"), #this refers to the views imported from rest_framework.authtoken
    # path('logout', views.logout_view, name = "logout_url"),
]
