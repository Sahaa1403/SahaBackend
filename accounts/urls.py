from django.urls import path
from accounts.views import Logout,Profile,Refresh,RefreshAccess,OverView,Login,Register,ProfilePicture

urlpatterns = [
    path("login", Login.as_view(), name="login"),
    path("register", Register.as_view(), name="register"),
    path("refresh", Refresh.as_view(), name="refresh"),
    path("refresh-access", RefreshAccess.as_view(), name="refresh-access"),
    path("logout", Logout.as_view(), name="logout"),
    path("profile", Profile.as_view(), name="profile"),
    path("profile/picture", ProfilePicture.as_view(), name="profile-picture"),
    path("overview", OverView.as_view(), name="overview"),
]
