from django.contrib import admin
from django.urls import path, include
from budgettracker import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('budgettracker/', include('budgettracker.urls')),
]
