from django.urls import path

from topics import views

app_name = "topics"

urlpatterns = [
    path("create-topic/",
         views.TopicCreateView.as_view(), name="topic_create"),
    path("delete-topic/<int:pk>/",
         views.TopicDeleteView.as_view(), name="topic_delete"),
    path("<int:pk_topic>/",
         views.TopicView.as_view(), name="topic_detail"),

    path("create-message/",
         views.MessageCreateView.as_view(), name="message_create"),

    path("vote/",
         views.VoteMessageView.as_view(), name="vote_message"),
]
