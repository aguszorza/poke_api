from django.urls import path
from accounts.views import LoginView, UserView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('user/me/', UserView.as_view(), name='me'),
]
