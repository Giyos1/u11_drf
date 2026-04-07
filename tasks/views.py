from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.models import Project, Task, Status
from tasks.serializers import ProjectSerializer, ProjectListSerializer, TaskSerializer, TaskListSerializer


# def post_list(request):
#     posts = Post.objects.all()
#     posts_list = []
#     for post in posts:
#         posts_list.append({"id": post.id, "title": post.title, "content": post.content})
#     return JsonResponse(posts_list, safe=False)


class ProjectView(APIView):
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectListSerializer(projects, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return JsonResponse(serializer.data, safe=False)
        # return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=201)

    def put(self, request, pk=None):
        project = get_object_or_404(Project, id=pk)
        serializer = ProjectSerializer(instance=project, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=200)

    def delete(self, request, pk=None):
        project = get_object_or_404(Project, id=pk)
        project.delete()
        return JsonResponse({"message": "success"}, status=204)


# class HelloViewSet(viewsets.ViewSet):
#     # CRUD -> GET->royxat->list(),GET/1-> detail->retrieve(),POST-> create(),PUT -> update(),
#     # PATCH->partial_update(),DELETE->destroy() ||yana CRUD dan boshqa narsa kerak bolsa -> action
#     def list(self, request):
#         return Response({"message": "hello world"})

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProjectSerializer
        elif self.action == 'tasks':
            return TaskListSerializer
        else:
            return ProjectListSerializer

    @action(detail=True, methods=['get'], url_name='tasks', serializer_class=TaskListSerializer)
    def tasks(self, request, pk=None):
        project = self.get_object()
        tasks = Task.objects.filter(project=project)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)


class TaskViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  ):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_serializer_class(self):
        if self.action in ("list", 'retrieve'):
            return TaskListSerializer
        return TaskSerializer

    def get_queryset(self):
        return self.queryset.exclude(status=Status.REJECTED)
