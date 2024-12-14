from rest_framework import serializers
from .models import Event, EventRegistration
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        extra_kwargs = {'email': {'required': True}}

class EventSerializer(serializers.ModelSerializer):
    """
    Серіалізатор для подій.
    """
    organizer = UserSerializer(read_only=True)
    registered_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'date',
            'location', 'organizer', 'max_participants',
            'registered_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'organizer']
        swagger_schema_fields = {
            'example': {
                'title': 'Конференція Python',
                'description': 'Щорічна конференція Python розробників',
                'date': '2024-03-01T15:00:00Z',
                'location': 'Київ, вул. Хрещатик 1',
                'max_participants': 100
            }
        }

    def get_registered_count(self, obj):
        return obj.registrations.count()

class EventRegistrationSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = EventRegistration
        fields = ['id', 'user', 'event', 'registered_at']
        read_only_fields = ['registered_at']