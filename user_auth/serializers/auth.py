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
            if cpf_value:
                try:
                    # Ensure CPF is cleaned and validated before creating or fetching
                    cpf_cleaned = Cpf.clean_cpf(cpf_value)
                    if not cpf_cleaned:
                        raise serializers.ValidationError({'cpf': _('CPF cannot be null or empty')})
                    if len(cpf_cleaned) != 11:
                        raise serializers.ValidationError({'cpf': _('CPF must be exactly 11 digits')})
                    
                    # Use get_or_create_cpf method without unpacking its return value
                    cpf_instance, _ = Cpf.get_or_create_cpf(cpf_cleaned)
                    data['cpf'] = cpf_instance
                except Exception as e:
                    raise serializers.ValidationError({'cpf': 'Não foi possível criar o usuário com esse CPF'})
                
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

