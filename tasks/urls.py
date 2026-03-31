from django.urls import path

from tasks import views

urlpatterns = [
    # path('', views.post_list, name='post'),
    path('project/', views.ProjectView.as_view(), name='project'),
    path('project/create/', views.ProjectView.as_view(), name='project-create'),
    path('project/update/<int:pk>/', views.ProjectView.as_view(), name='project-update'),
]
