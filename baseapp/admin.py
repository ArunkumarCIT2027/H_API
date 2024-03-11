from django.contrib import admin
from .models import Doctor, Patient, Appointment, MedicalRecord, Conversation, Message,Qualification,Specialization

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'office_number', 'email')
    search_fields = ('user__username', 'user__email')

class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'gender', 'phone_number', 'email', 'age', 'blood_group')
    search_fields = ('user__username', 'user__email')

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'date', 'time', 'status')
    search_fields = ('doctor__user__username', 'patient__user__username')

class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'description')
    search_fields = ('patient__user__username', 'doctor__user__username')

class ConversationAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient')
    search_fields = ('doctor__username', 'patient__username')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'conversation', 'content', 'timestamp')
    search_fields = ('sender__username', 'conversation__doctor__username', 'conversation__patient__username')

admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(MedicalRecord, MedicalRecordAdmin)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Qualification)
admin.site.register(Specialization)

