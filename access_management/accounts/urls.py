from django.urls import path
from accounts.views import AddGroupView, LoginView, UserView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('user/me/', UserView.as_view(), name='me'),
    path('group/<str:type_name>/add/', AddGroupView.as_view(), name='add_group'),
]
