from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView

from tasks.models import Post, Project
from tasks.serializers import ProjectSerializer, ProjectListSerializer


def post_list(request):
    posts = Post.objects.all()
    posts_list = []
    for post in posts:
        posts_list.append({"id": post.id, "title": post.title, "content": post.content})
    return JsonResponse(posts_list, safe=False)


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
