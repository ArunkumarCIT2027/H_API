from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Doctor, Patient, Appointment, MedicalRecord, Qualification, Specialization, Conversation, Message
from .serializers import QualificationSerializer, SpecializationSerializer, DoctorSerializer, PatientSerializer, AppointmentSerializer, MedicalRecordSerializer, ConversationSerializer, MessageSerializer
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login,logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import TemplateResponseMixin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_doctor(request):
    if request.method == 'POST':
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data['user']['username'],
                password=serializer.validated_data['user']['password'],
                email=serializer.validated_data['user']['email'],
                first_name=serializer.validated_data['user']['first_name'],
                last_name=serializer.validated_data['user']['last_name'],
            )
            doctor = serializer.save(user=user)
            return Response(DoctorSerializer(doctor).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_user(request):
    if request.method == 'POST':
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data['user']['username'],
                password=serializer.validated_data['user']['password'],
                email=serializer.validated_data['user']['email'],
                first_name=serializer.validated_data['user']['first_name'],
                last_name=serializer.validated_data['user']['last_name'],
            )
            patient = serializer.save(user=user)
            return Response(PatientSerializer(patient).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_doctor(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                return Response({'detail': 'Disabled account'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                return Response({'detail': 'Disabled account'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

# class PasswordResetEmailView(TemplateResponseMixin, CreateView):
#     template_name = 'registration/password_reset_form.html'
#     form_class = PasswordResetForm
#     success_url = reverse_lazy('password_reset_done')

#     def form_valid(self, form):
#         email = form.cleaned_data['email']
#         user = get_user_model().objects.get(email=email)
#         token = Token.objects.get_or_create(user=user)[0]
#         subject = 'Password Reset Request'
#         message = f'Hello {user.get_full_name()},\n\nYou have requested a password reset. If this was not you, please ignore this email.\n\nTo reset your password, visit this link:\n\n{reverse_lazy("password_reset_confirm", kwargs={"uidb64": urlsafe_base64_encode(force_bytes(user.pk)).decode(), "token": token.key})'
#         email_message = EmailMessage(subject, message, to=[email])
#         email_message.send()
#         return super().form_valid(form)

# class PasswordResetConfirmView(PasswordResetConfirmView):
#     template_name = 'registration/password_reset_confirm_form.html'
#     success_url = reverse_lazy('password_reset_complete')

# class PasswordResetCompleteView(TemplateResponseMixin, CreateView):
#     template_name = 'registration/password_reset_complete.html'

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def forgot_password(request):
#     if request.method == 'POST':
#         return PasswordResetEmailView.as_view()(request)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_all_doctors(request):
    if request.method == 'GET':
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_doctor_details(request, doctor_id):
    if request.method == 'GET':
        try:
            doctor = Doctor.objects.get(pk=doctor_id)
        except Doctor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_appointments_ordered(request):
    if request.method == 'GET':
        appointments = Appointment.objects.filter(status__in=['pending', 'confirmed']).order_by('date', 'time')
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def mark_appointment_completed(request, appointment_id):
    if request.method == 'PUT':
        appointment = get_object_or_404(Appointment, pk=appointment_id)
        appointment.status = 'completed'
        appointment.save()
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def mark_appointment_cancelled(request, appointment_id):
    if request.method == 'PUT':
        appointment = get_object_or_404(Appointment, pk=appointment_id)
        appointment.status = 'cancelled'
        appointment.save()
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_appointment_details(request, appointment_id):
    if request.method == 'GET':
        try:
            appointment = Appointment.objects.get(pk=appointment_id)
        except Appointment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_all_messages(request):
    if request.method == 'GET':
        messages = Message.objects.order_by('-time')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_message(request):
    if request.method == 'POST':
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            raise ValidationError(serializer.errors)

