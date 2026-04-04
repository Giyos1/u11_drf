from django.urls import path, include
from rest_framework import routers

from tasks import views

router = routers.DefaultRouter()

router.register('task', views.TaskViewSet, basename='tasks')
router.register('project', views.ProjectViewSet, basename='projects')

urlpatterns = [
    path('', include(router.urls)),
    # path('project/', views.ProjectView.as_view(), name='project'),
    # path('project/create/', views.ProjectView.as_view(), name='project-create'),
    # path('project/update/<int:pk>/', views.ProjectView.as_view(), name='project-update'),
    # path('project/delete/<int:pk>/', views.ProjectView.as_view(), name='project-delete'),
]
