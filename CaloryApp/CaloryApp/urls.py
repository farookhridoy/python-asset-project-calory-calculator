from django.contrib import admin
from django.urls import path
from CaloryApp.views import home, about
from Backend import views as backend_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('register/', backend_views.register, name='register'),
    path('login/', backend_views.user_login, name='login'),
    path('logout/', backend_views.user_logout, name='logout'),
    path('profile/', backend_views.profile, name='profile'),
    path('dashboard/', backend_views.dashboard, name='dashboard'),
    path('api/dashboard/', backend_views.api_dashboard, name='api_dashboard'),
    path('api/add/', backend_views.add_food, name='add_food'),
    path('api/edit/<int:entry_id>/', backend_views.edit_food, name='edit_food'),
    path('api/delete/<int:entry_id>/', backend_views.delete_food, name='delete_food'),
]
