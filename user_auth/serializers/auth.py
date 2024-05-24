from rest_framework import serializers
from django.contrib.auth import authenticate
from user_auth.models import BaseUser, Cpf


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ['email', 'name', 'password', 'cpf']

    def to_internal_value(self, data):
        if 'cpf' in data:
            cpf_value = data['cpf']
            cpf_instance, created = Cpf.get_or_create_cpf(cpf_value)
            data['cpf'] = cpf_instance

        return super().to_internal_value(data)

    def create(self, validated_data):
        user = BaseUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])

        user.save()
        return user


class UserGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = [
            'id',
            'email',
        ]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField()
    cpf = serializers.CharField(required=False)

    def validate(self, attrs):
        email = attrs.get('email')
        cpf = attrs.get('cpf')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
        elif cpf and password:
            try:
                baseuser=BaseUser.objects.get(cpf=cpf)
                email=baseuser.email
                user = authenticate(email=email, password=password)
                if not user:
                    raise serializers.ValidationError('Invalid credentials')
                if not user.is_active:
                    raise serializers.ValidationError('User account is disabled')
            except: 
                raise serializers.ValidationError('User not found')
        else:
            raise serializers.ValidationError('Email and password are required')

        attrs['user'] = user
        return attrs

