from django.urls import reverse_lazy
from django.urls import path
from django.contrib.auth import views as auth_views  
from . import views


urlpatterns = [
    
    path('profile/', views.profile_view, name='profile'),
    path('', views.home, name='home'),
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('cancel-reservation/<int:pk>/', views.cancel_reservation, name='cancel_reservation'),
]
