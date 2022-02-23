from django.urls import path
from . import views


urlpatterns = [
    path('statistics/<provider_Abbr>/<datefrom>/<dateto>', views.statistics_dashboard, name='statistics_dashboard_url'),
    path('statistics/', views.statistics_home, name='statistics_home_url'),
    path('upload_passes/', views.upload_passes_view, name='upload_passes_url'),
    path('upload_passes/successful_upload/', views.successful_upload_view, name='upload_passes_url'),
    path('upload_passes/failed_upload/', views.failed_upload_view, name='upload_passes_url')
]