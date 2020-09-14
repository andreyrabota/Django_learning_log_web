from django.urls import path
from . import views


app_name = 'learning_logs'

urlpatterns = [
    #homepage
    path('', views.index, name='index'),
    #topics
    path('topics/', views.topics, name='topics'),
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # add new topic
    path('new_topic/', views.new_topic, name='new_topic'),
    # page with entries
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # edit entry
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]