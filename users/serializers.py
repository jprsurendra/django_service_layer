from rest_framework import serializers


class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class TestModelSerializer(serializers.Serializer):
    name = serializers.CharField()
    password = serializers.CharField()