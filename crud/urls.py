from django.urls import path
from . import views



urlpatterns = [
    # path('courses/',views.course, name="course-list"),
    path('class-detail/<int:class_id>/',views.class_detail, name="class-detail"),
    path('class-delete/<int:class_id>/',views.class_delete, name="class-delete"),
    path('class-update/<int:class_id>/',views.class_update, name="class-update"),
    path('class-create/',views.class_create, name="class-create"),
    path('administration/',views.administration, name="administration"),
    #announcement
    path('announcement-create/<int:class_id>/',views.announcement_create, name="announcement-create"),
   
   
    #create quiz
    path('create-quiz/<int:class_id>/',views.create_quiz, name='create-quiz'),
    path('create-question/<int:quiz_id>/',views.create_question, name='create-question'),
    
    path('question-update/<int:question_id>/',views.question_update, name='question-update'),
    path('question-delete/<int:question_id>/',views.question_delete, name='question-delete'),
    #create choices
    path('create-choice/<int:question_id>/',views.create_choice, name='create-choice'),
    #choice detail
    path('choice-detail/<int:choice_id>/',views.choice_detail, name='choice-detail'),
    #choice update
    path('choice-update/<int:choice_id>/',views.choice_update, name='update-choice'),
    #choice delete
    path('choice-delete/<int:choice_id>/',views.choice_delete, name='delete-choice'),
    #quiz
    #list
    path('quiz-list/<int:class_id>/',views.quiz_list, name='quiz-list'),
    #result
    path('quiz-results/<int:quiz_id>/',views.quiz_results, name='quiz-results'),
    #detail
    path('quiz-detail/<int:quiz_id>/',views.quiz_detail, name='quiz-detail'),
    #update
    path('quiz-update/<int:quiz_id>/',views.quiz_update, name='quiz-update'),
    #delete
    path('quiz-delete/<int:quiz_id>/',views.quiz_delete, name='quiz-delete'),
   
]