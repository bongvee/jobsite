from django.urls import path
from . import views

urlpatterns = [
    # CRUD routes
    path('jobs/', views.readAllJobs, name='list_jobs'),
    path('jobs/<str:pk>/', views.readAJob, name='read_job'),

    path('jobs/create/', views.createAJob, name='create_job'),
    path('jobs/<str:pk>/update/', views.updateAJob, name='update_job'),
    path('jobs/<str:pk>/delete/', views.deleteAJob, name='delete_job'),

    # FILTER
    path('topic-stats/<str:topic>/', views.readTopicStatistics, name='topic_stats'),
]
