from django.urls import path
from . import views

app_name = "battles"

urlpatterns = [
    path("", views.topic_list, name="topic_list"),
    path("create/", views.topic_create, name="topic_create"),
    path("topic/<int:pk>/", views.topic_detail, name="topic_detail"), 
    path("answer/<int:answer_pk>/vote/", views.vote_answer, name="vote_answer"),
]