from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Event, EventRegistration
from .serializers import EventSerializer, EventRegistrationSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.views.generic import ListView
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, DateTimeFilter, CharFilter
from django.db.models import Count
from .utils import send_registration_email
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class EventFilter(FilterSet):
    start_date = DateTimeFilter(field_name='date', lookup_expr='gte')
    end_date = DateTimeFilter(field_name='date', lookup_expr='lte')
    location = CharFilter(field_name='location', lookup_expr='icontains')
    
    class Meta:
        model = Event
        fields = ['start_date', 'end_date', 'location', 'organizer']


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управління подіями.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EventFilter
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['date', 'created_at', 'title']
    ordering = ['date']

    def perform_create(self, serializer):
        """
        Зберігає поточного користувача як організатора події.
        """
        serializer.save(organizer=self.request.user)

    @swagger_auto_schema(
        operation_description="Отримати список всіх подій",
        responses={200: EventSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="Search in title, description and location", type=openapi.TYPE_STRING),
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Filter events after this date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="Filter events before this date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('location', openapi.IN_QUERY, description="Filter by location", type=openapi.TYPE_STRING),
            openapi.Parameter('ordering', openapi.IN_QUERY, description="Order by field (prefix with - for descending)", type=openapi.TYPE_STRING),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Створити нову подію",
        request_body=EventSerializer,
        responses={
            201: EventSerializer,
            400: "Неправильні дані",
            401: "Необхідна автентифікація"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Зареєструватися на подію",
        responses={
            201: "Успішна реєстрація",
            400: "Подія заповнена або ви вже зареєстровані",
            404: "Подію не знайдено"
        }
    )
    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def register(self, request, pk=None):
        """
        Реєстрація користувача на подію.
        """
        event = self.get_object()

        if event.registrations.count() >= event.max_participants:
            return Response(
                {'error': 'Event is already full'},
                status=status.HTTP_400_BAD_REQUEST
            )

        registration, created = EventRegistration.objects.get_or_create(
            user=request.user,
            event=event
        )

        if not created:
            return Response(
                {'error': 'You are already registered for this event'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Відправляємо email підтвердження
        try:
            send_registration_email(request.user, event)
        except Exception as e:
            print(f"Failed to send email: {e}")
            # Можна додати логування помилки

        serializer = EventRegistrationSerializer(registration)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Скасувати реєстрацію на подію",
        responses={
            204: "Реєстрацію скасовано",
            400: "Ви не зареєстровані на цю подію",
            404: "Подію не знайдено"
        }
    )
    @action(detail=True, methods=['DELETE'], permission_classes=[permissions.IsAuthenticated])
    def unregister(self, request, pk=None):
        """
        Скасування реєстрації користувача на подію.
        """
        event = self.get_object()

        try:
            registration = EventRegistration.objects.get(
                user=request.user,
                event=event
            )
            registration.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except EventRegistration.DoesNotExist:
            return Response(
                {'error': 'You are not registered for this event'},
                status=status.HTTP_400_BAD_REQUEST
            )

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.all().select_related('organizer').order_by('date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context['events']:
            print("No events found")
        else:
            print(f"Found {len(context['events'])} events")
        messages.get_messages(self.request)  # Clear any existing messages
        return context

def register_view(request):
    if request.method == 'POST':
        form_data = {
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
            'password2': request.POST.get('password2'),
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
        }
        
        if form_data['password'] != form_data['password2']:
            messages.error(request, 'Passwords do not match.')
            return redirect('home')
            
        try:
            user = User.objects.create_user(
                username=form_data['username'],
                email=form_data['email'],
                password=form_data['password'],
                first_name=form_data['first_name'],
                last_name=form_data['last_name']
            )
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
    return redirect('home')

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')