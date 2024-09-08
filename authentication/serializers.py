from django.contrib.auth.models import Group
from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    group_id = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'groups', 'identification', 'address', 'state',
                  'phone', 'group_id']
        extra_kwargs = {
            'password': {'write_only': True},
            'groups': {'read_only': True}  # Evita modificar el campo directamente
        }

    def create(self, validated_data):
        group_id = validated_data.pop('group_id', None)
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            identification=validated_data.get('identification', ''),
            address=validated_data.get('address', ''),
            phone=validated_data.get('phone', '')
        )

        # Asigna el grupo si se proporciona
        if group_id:
            group = Group.objects.get(id=group_id)
            user.groups.add(group)

            # Asignar los permisos del grupo al usuario explícitamente
            permissions = group.permissions.all()
            user.user_permissions.set(permissions)

        return user

    def update(self, instance, validated_data):
        # Actualiza la información del usuario
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.identification = validated_data.get('identification', instance.identification)
        instance.address = validated_data.get('address', instance.address)
        instance.phone = validated_data.get('phone', instance.phone)

        # Actualizar el grupo si se proporciona un nuevo `group_id`
        group_id = validated_data.get('group_id', None)
        if group_id:
            # Limpiar los grupos actuales
            instance.groups.clear()

            # Asigna el nuevo grupo
            group = Group.objects.get(id=group_id)
            instance.groups.add(group)

            # Asignar los permisos del grupo al usuario explícitamente
            permissions = group.permissions.all()
            instance.user_permissions.set(permissions)

        instance.save()
        return instance


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']