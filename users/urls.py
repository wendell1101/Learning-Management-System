from django.urls import path
from django.contrib.auth import views as auth_view
from . import views

urlpatterns = [
    path('register/teacher',views.teacher_register, name="teacher-register"),
    path('register/student',views.student_register, name="student-register"),
    path('login/',auth_view.LoginView.as_view(template_name='users/login.html'), name="login"),
    path('logout/',auth_view.LogoutView.as_view(template_name='users/logout.html'), name="logout"),
    #student profile
    path('profile',views.profile, name="profile"),
    path('profile-update/<str:username>',views.profile_update, name="profile-update"),
]