from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LoginView
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('user_accounts/<int:user_id>/', views.user_accounts, name='user_accounts'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('register/', views.register, name='register'),
    path('logged_out/', views.logged_out, name='logged_out'),
    path('logged_in/', views.logged_in, name='logged_in'),
    path('please_authenticate/', views.please_authenticate, name='please_authenticate'),
    path('specific_uma/<int:uma_id>/', views.specific_uma, name='specific_uma'),
    path('specific_uma_transaction_buffer/<int:uma_id>/<int:buffer_iteration>/', views.specific_uma_transaction_buffer, name='specific_uma_transaction_buffer'),
    path('delete_all_accounts/<int:user_id>/', views.delete_all_accounts, name='delete_all_accounts'),



    path('run_tests/', views.run_tests, name='run_tests'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)