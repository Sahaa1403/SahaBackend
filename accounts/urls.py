from django.urls import path
from accounts.views import Logout,Profile,Refresh,RefreshAccess,OverView,Login,Register,ProfilePicture,FullRegister
from accounts.management_views import UsersList,UserItem

urlpatterns = [
    path("login", Login.as_view(), name="login"),
    path("register", Register.as_view(), name="register"),
    path("full-register", FullRegister.as_view(), name="full-register"),
    path("refresh", Refresh.as_view(), name="refresh"),
    path("refresh-access", RefreshAccess.as_view(), name="refresh-access"),
    #path("overview", OverView.as_view(), name="overview"),
    path("profile", Profile.as_view(), name="profile"),
    path("profile-picture", ProfilePicture.as_view(), name="profile-picture"),
    path("logout", Logout.as_view(), name="logout"),
    # --- Manage users ---
    path("users", UsersList.as_view(), name="users"),
    path("user/<int:id>", UserItem.as_view(), name="user"),
]
