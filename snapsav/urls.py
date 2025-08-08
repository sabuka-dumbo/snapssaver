from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('download/', views.download_video, name='download_video'),
    path('facebook/', views.facebook_page, name='facebook_page'),
    path('facebook-download/', views.facebook_download, name='facebook_download'),
    path('tiktok/', views.tiktok_page, name='tiktok_page'),
    path('tiktok-download/', views.tiktok_download, name='tiktok_download'),
]
