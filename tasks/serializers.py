from django.contrib.auth.models import User
from rest_framework import serializers
from accounts.serializers import UserSerializer
from tasks.models import Project, Task


# class ProjectSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=255)
#     description = serializers.CharField()
#     owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
#
#     def validate_title(self, value):
#         if len(value) < 8:
#             raise serializers.ValidationError("Title must be between 8 and 128 characters long")
#         return value
#
#     # def validate(self, data):
#     #     pass
#
#     def create(self, validated_data):
#         return Project.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description', instance.description)
#         instance.save()
#         return instance
#
# def save(self, **kwargs):
#     pass

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            "title",
            "description",
            "owner"
        )


class ProjectListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    owner = UserSerializer()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class TaskListSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer()

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            'assigned_to',
            "status",
            'created_at',
            'updated_at',
        )


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            'assigned_to',
            'project',
            "status",
            'created_at',
            'updated_at',
        )
