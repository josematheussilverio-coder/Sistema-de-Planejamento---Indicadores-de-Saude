from django.contrib import admin
from django.urls import path, include
from app import views 

urlpatterns = [
    path('apagar-banco/', views.apagar_banco, name='apagar_banco'),
    path('admin/', admin.site.urls),
    
    path('accounts/', include('django.contrib.auth.urls')), 
    
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.importar_planilhas, name='importar_planilhas'),
]