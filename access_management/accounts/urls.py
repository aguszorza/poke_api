from django.urls import path
from accounts.views import AddToGroupView, LoginView, RemoveFromGroupView, UserView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("user/me/", UserView.as_view(), name="me"),
    path("group/<str:type_name>/add/", AddToGroupView.as_view(), name="add_to_group"),
    path(
        "group/<str:type_name>/remove/",
        RemoveFromGroupView.as_view(),
        name="remove_from_group",
    ),
]
