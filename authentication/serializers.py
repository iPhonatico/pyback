from django.contrib.auth.models import Group
from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'groups', 'identification', 'address', 'state', 'phone']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            identification=validated_data.get('identification', ''),
            address=validated_data.get('address', ''),
            phone=validated_data.get('phone', '')
        )

        # Asigna el grupo con ID 1 al usuario recién creado
        default_group = Group.objects.get(id=1)
        user.groups.add(default_group)

        return user


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']