from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

class Qualification(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Specialization(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    office_number = models.CharField(max_length=20)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    qualifications = models.ManyToManyField(Qualification)
    years_of_experience = models.PositiveIntegerField()
    image = models.ImageField(upload_to='doctors/', null=True, blank=True)

    def __str__(self):
        return self.name

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=20, validators=[RegexValidator(regex=r'^\d{10}$', message="Phone number must be 10 digits long.")])
    email = models.EmailField(null=True)
    age = models.PositiveIntegerField()
    blood_group = models.CharField(max_length=3)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed')])

    def clean(self):
        same_doctor_patients = Appointment.objects.filter(doctor=self.doctor, patient__in=[self.patient, self.patient.user])
        same_patient_doctors = Appointment.objects.filter(patient=self.patient, doctor__in=[self.doctor, self.doctor.user])
        conflicting_appointments = same_doctor_patients | same_patient_doctors
        conflicting_appointments = conflicting_appointments.exclude(pk=self.pk).filter(date=self.date, time=self.time)
        if conflicting_appointments.exists():
            raise ValidationError("The appointment date and time conflicts with another appointment for the same doctor and patient.")

        if not self.doctor.user.is_active or not self.patient.user.is_active:
            raise ValidationError("The doctor or patient has been deleted or changed.")

        if self.date < timezone.now().date():
            raise ValidationError("The appointment date is in the past.")

    def __str__(self):
        return f"{self.doctor.user.username} - {self.patient.user.username} - {self.date} - {self.time}"

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.user.username} - {self.doctor.user.username} - {self.date}"

class Conversation(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_conversations')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_conversations')

    def __str__(self):
        return f"{self.doctor.username} - {self.patient.username}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} - {self.conversation} - {self.timestamp}"


