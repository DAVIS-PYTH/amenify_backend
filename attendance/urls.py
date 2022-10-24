from django.urls import path, include
from . import social_auth
from . import views
urlpatterns = [
    path("authenticate/token/", views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),

    path("authenticate/register/", views.registerUser, name="register_user_pair"),
    
    # attendance views
    path("attendance/list/", views.getAttendanceList, name="list_user_attendance"),
    path("attendance/update/", views.updateAttendanceList, name="update_user_attendance"),
    path("attendance/create/", views.addAttendance, name="create_user_attendance"),
    
    path('accounts/', include('allauth.urls')),
    path('social-auth/google/', social_auth.GoogleLogin.as_view()),
    path('social-auth/facebook/',social_auth.FacebookLogin.as_view()),
]
