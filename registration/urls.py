from django.urls import path
from .views import SignUpView, ProfileUpdate, EmailUpdate, update_profile_admin2
from . import views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name = 'signup'),
    path('profile/', ProfileUpdate.as_view(), name = 'profile'),
    path('profile/admin/', views.update_profile_admin2, name = 'profile_admin'),
    path('profile/email/', EmailUpdate.as_view(), name = 'profile_email')
]