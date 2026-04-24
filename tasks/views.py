# from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, mixins, filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.models import Project, Task, Status
from tasks.serializers import ProjectSerializer, ProjectListSerializer, TaskSerializer, TaskListSerializer
from django.contrib.postgres.search import TrigramSimilarity


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

    @swagger_auto_schema(
        operation_summary='project_create',
        operation_description='create a new project',
        request_body=ProjectSerializer,
        responses={
            200: openapi.Response(
                'Muvaffaqiyatli',
                ProjectSerializer,
            ),
        }

    )
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
    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter
    ]
    search_fields = [
        'title',
        'description',
    ]
    filterset_fields = [
        'status',
        'assigned_to',
        'project',
    ]
    ordering_fields = [
        'created_at',
    ]

    def get_serializer_class(self):
        if self.action in ("list", 'retrieve'):
            return TaskListSerializer
        return TaskSerializer

    # def get_queryset(self):
    #     # search = self.request.GET.get('search')
    #     # if search:
    #     #     self.queryset = self.queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))
    #     return self.queryset.exclude(status=Status.REJECTED)

    # def get_queryset(self):
    #     q = self.request.query_params.get('search')
    #     qs = Task.objects.all()
    #     if q:
    #         qs = qs.annotate(
    #             similarity=TrigramSimilarity(
    #                 'title', q
    #             )
    #         ).filter(
    #             similarity__gt=0.1  # 30% o'xshashlik
    #         ).order_by('-similarity')
    #     return qs
