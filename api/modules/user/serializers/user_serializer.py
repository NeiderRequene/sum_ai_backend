
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.modules.user.serializers.group_serializer import GroupSerializer

# Serializers define the API representation.

User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializador para listar los usuarios
    """
    num_purchased_courses = serializers.IntegerField(read_only=True)
    num_certificates = serializers.IntegerField(read_only=True)
    num_subscriptions = serializers.IntegerField(read_only=True)

    def to_representation(self, instance):
        self.fields['groups'] = GroupSerializer(many=True, required=False)
        return super(UserListSerializer, self).to_representation(instance)

    class Meta:
        model = User
        fields = ['id', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'is_staff',
                  'is_active', 'date_joined', 'name', 'email', 'register_type',
                  'is_verify_email', 'groups', 'user_permissions']


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializador para crear un usuario
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        min_length=8, write_only=True, required=True)
    is_active = serializers.BooleanField(
        required=True)

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],
                                        email=validated_data['email'],
                                        name=validated_data['name'],
                                        first_name=validated_data['first_name'],
                                        last_name=validated_data['last_name'],
                                        is_superuser=False,
                                        is_active=validated_data['is_active'],
                                        is_staff=False,
                                        register_type=validated_data['register_type']
                                        )
        user.set_password(validated_data['password'])
        user.save()
        list_groups = validated_data['groups']
        for group in list_groups:
            user.groups.add(group)
        return user

    def to_representation(self, instance):
        self.fields['groups'] = GroupSerializer(many=True, required=False)
        return super(UserCreateSerializer, self).to_representation(instance)

    class Meta:
        model = User
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializador para mostrar el detalle de un usuario específico.
    Además permitirá actualizar los datos de un usuario
    """
    password = serializers.CharField(
        min_length=8, write_only=True, required=False)

    def update(self, user, validated_data):
        user.username = validated_data.get('username', user.username)
        user.email = validated_data.get('email', user.email)
        user.name = validated_data.get(
            'name', user.name)
        user.first_name = validated_data.get('first_name', user.first_name)
        user.last_name = validated_data.get('last_name', user.last_name)
        user.is_active = validated_data.get('is_active', user.is_active)
        user.register_type = validated_data.get(
            'register_type', user.register_type)
        user.save()
        user.groups.clear()
        list_groups = validated_data['groups']
        for group in list_groups:
            user.groups.add(group)
        return user

    def to_representation(self, instance):
        self.fields['groups'] = GroupSerializer(many=True, required=False)
        return super(UserDetailSerializer, self).to_representation(instance)

    class Meta:
        model = User
