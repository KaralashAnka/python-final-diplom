from django.urls import path
from . import views
from .contact_views import ContactViewSet, ContactCreateView

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password-reset'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('addresses/', views.AddressViewSet.as_view({'get': 'list', 'post': 'create'}), name='addresses'),
    path('contacts/', ContactViewSet.as_view({'get': 'list', 'post': 'create'}), name='contacts'),
    path('contacts/add/', ContactCreateView.as_view(), name='contact-add'),
]
