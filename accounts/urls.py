from django.urls import path
from .views import SignUpView,UpdateProfileView

urlpatterns = [
    path('signup/',SignUpView.as_view(),name='signup'),
    path('profile/<int:pk>/',UpdateProfileView.as_view(),name='profile')

]