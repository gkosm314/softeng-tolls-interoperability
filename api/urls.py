from django.urls import path
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


#TODO: handle csv format admin/healthcheck?format=<response_format>'

urlpatterns = [
    path('admin/healthcheck', views.api_admin_healthcheck, name='healthcheck_url'),
    path('admin/resetpasses', views.api_admin_resetpasses, name='resetpasses_url'),
    path('admin/resetstations', views.api_admin_resetstations, name='resetstations_url'),
    path('admin/resetvehicles', views.api_admin_resetvehicles, name='resetvehicles_url'),
    path('admin/hardreset', views.api_admin_hardreset, name='hardreset_url'),

    path('login', views.ApiLoginView.as_view(), name="login_url"),
    path('logout', views.api_logout_view, name="logout_url"),
    path('PassesPerStation/<stationID>/<datefrom>/<dateto>', views.ApiPassesPerStation.as_view(), name='passes_per_station'),
    path('PassesAnalysis/<op1_ID>/<op2_ID>/<datefrom>/<dateto>', views.ApiPassesAnalysis.as_view(), name='passes_analysis'),
    path('PassesCost/<op1_ID>/<op2_ID>/<datefrom>/<dateto>', views.ApiPassesCost.as_view(), name='passes_analysis'),
    path('ChargesBy/<op_ID>/<datefrom>/<dateto>', views.ApiChargesBy.as_view(), name='passes_analysis'),

    # Schema urls
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
