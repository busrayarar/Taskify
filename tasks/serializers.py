from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, Comment

class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'password_confirm']
        extra_kwargs = {
            'password': {'write_only':True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            }
    
    def validate_email(self, value):
        value = value.lower().strip()
        qs = User.objects.filter(email__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Bu e-posta adresi zaten kullanılıyor.")
        return value

    def validate(self, data):
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError({
                "password_confirm": "Şifreler Eşleşmiyor."
            })
        data.pop('password_confirm', None)
        return data

    def create (self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content', 'task', 'author', 'created_at')
        read_only_fields = ['author', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'task_name', 'task_description', 'state', 'user', 'created_at', 'updated_at')
        read_only_fields = ['created_at']

    def validate_state(self,value):
        valid_states = ['TODO', 'IN_PROGRESS', 'DONE']
        if value not in valid_states:
            raise serializers.ValidationError(
                f"Geçersiz durum: '{value}' Yalnızca TODO, IN_PROGRESS VEYA DONE durumları geçerlidir."
            )
        return value
    
    def validate(self,data):
        request = self.context.get('request')
        if 'user' in data:
            if self.instance is None:
                data.pop('user', None)
            elif not (request and request.user.is_staff):
                raise serializers.ValidationError({
                    "user": "Sadece admin görevleri atayabilir."
                })
        state = data.get('state')
        user = data.get('user', getattr(self.instance, 'user', None))
        if state == 'DONE' and user is None:
            raise serializers.ValidationError({
                "user": " Atama yapılmamış bir görev 'Done' olarak işaretlenemez."           
            })
        return data

