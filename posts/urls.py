from django.urls import path
from .import views

urlpatterns = [
    path('post-create/',views.post_create, name='create-post'),
    path('post-update/<int:post_id>/',views.post_update, name='update-post'),
    path('post-delete/<int:post_id>/',views.post_delete, name='delete-post'),
]
