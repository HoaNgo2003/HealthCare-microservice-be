from django.urls import path
from .views import PatientInfoView, MedicalRecordsView, AppointmentListView

urlpatterns = [
    path('patients/me/', PatientInfoView.as_view(), name='patient-info'),
    path('patients/medical-records/', MedicalRecordsView.as_view(), name='patient-medical-records'),
    path('patients/appointments/', AppointmentListView.as_view(), name='patient-appointments'),
]
