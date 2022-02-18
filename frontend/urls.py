from django.urls import path
from . import views


urlpatterns = [
    path('<provider_Abbr>/<datefrom>/<dateto>', views.statistics_dashboard, name='statistics_dashboard_url'),
    path('', views.statistics_home, name='statistics_home_url')
]
