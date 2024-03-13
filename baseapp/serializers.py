from rest_framework import serializers
from .models import Doctor, Patient, Appointment, MedicalRecord, Qualification, Specialization, Conversation, Message
from django.utils import timezone


class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = '__all__'

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    specialization = serializers.CharField(source='specialization.name')
    qualifications = serializers.CharField(source='get_qualifications_display', read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id',
            'name',
            'qualifications',
            'specialization',
            'image',
            'email',
            'office_number',
            'available',
        ]

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    patient = PatientSerializer()

    class Meta:
        model = Appointment
        fields = '__all__'

    def clean(self):
        same_doctor_patients = Appointment.objects.filter(doctor=self.validated_data['doctor'], patient__in=[self.validated_data['patient'], self.validated_data['patient'].user])
        same_patient_doctors = Appointment.objects.filter(patient=self.validated_data['patient'], doctor__in=[self.validated_data['doctor'], self.validated_data['doctor'].user])
        conflicting_appointments = same_doctor_patients | same_patient_doctors
        conflicting_appointments = conflicting_appointments.exclude(pk=self.instance.pk).filter(date=self.validated_data['date'])
        if conflicting_appointments.exists():
            raise serializers.ValidationError("The appointment date conflicts with another appointment for the same doctor and patient.")

        if not self.validated_data['doctor'].user.is_active or not self.validated_data['patient'].user.is_active:
            raise serializers.ValidationError("The doctor or patient has been deleted or changed.")

        if self.validated_data['date'] < timezone.now():
            raise serializers.ValidationError("The appointment date is in the past.")

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    doctor = DoctorSerializer()

    class Meta:
        model = MedicalRecord
        fields = '__all__'

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    conversation = ConversationSerializer()
    sender = DoctorSerializer()

    class Meta:
        model = Message
        fields = '__all__'