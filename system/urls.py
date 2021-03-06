from django.urls import path
from . import views

urlpatterns = [
    path('registration/',views.landing_page, name="landing-page"),
    path('',views.index, name="index"),
    path('student-class-list/',views.student_class_list, name="student-class-list"),
    path('student-class-detail/<int:class_id>/', views.student_class_detail, name="student-class-detail"),
    path('take-quiz/<int:quiz_id>/', views.take_quiz, name="take-quiz"),
  
    path('quiz/<int:quiz_id>/results', views.show_results, name="show-results"),
    path('announcement-create/', views.announcement_create, name="create-announcement"),
    path('announcement-list/', views.announcement_list, name="announcement-list"),
    path('announcement-detail/<int:announcement_id>', views.announcement_detail, name="announcement-detail"),
    path('announcement-delete/<int:announcement_id>', views.announcement_delete, name="delete-announcement"),
    path('announcement-update/<int:announcement_id>', views.announcement_update, name="update-announcement"),
    

]
