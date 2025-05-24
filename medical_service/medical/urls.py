# medical/urls.py

from django.urls import path
from .views import MedicalRecordCreateView, PrescriptionCreateView, GetListMedicalRecordView, GetListPrescriptionView, GetMedicalRecordByIdView, GetPrescriptionByIdView, GetListMedicalRecordByPatientIdView, GetListPrescriptionByPatientIdView, GetListMedicalRecordByDoctorIdView, GetListPrescriptionByDoctorIdView, DeleteMedicalRecordView, DeletePrescriptionView

urlpatterns = [
    path('medical-records/', MedicalRecordCreateView.as_view(), name='create-medical-record'),
    path('medical-records/<int:pk>/', MedicalRecordCreateView.as_view(), name='update-medical-record'),
    path('prescriptions/', PrescriptionCreateView.as_view(), name='create-prescription'),
    path('prescriptions/<int:pk>/', PrescriptionCreateView.as_view(), name='update-prescription'),
    path('medical-records/list/', GetListMedicalRecordView.as_view(), name='list-medical-records'),
    path('prescriptions/list/', GetListPrescriptionView.as_view(), name='list-prescriptions'),
    path('medical-records/<int:pk>/', GetMedicalRecordByIdView.as_view(), name='get-medical-record-by-id'),
    path('prescriptions/<int:pk>/', GetPrescriptionByIdView.as_view(), name='get-prescription-by-id'),
    path('medical-records/patient/<int:patient_id>/', GetListMedicalRecordByPatientIdView.as_view(), name='list-medical-records-by-patient'),
    path('prescriptions/patient/<int:patient_id>/', GetListPrescriptionByPatientIdView.as_view(), name='list-prescriptions-by-patient'),
    path('list-medical-records-by-doctor/<int:doctor_id>/', GetListMedicalRecordByDoctorIdView.as_view(), name='list-medical-records-by-doctor'),
    path('list-prescriptions-by-doctor/<int:doctor_id>/', GetListPrescriptionByDoctorIdView.as_view(), name='list-prescriptions-by-doctor'),
    path('delete-medical-record/<int:pk>/', DeleteMedicalRecordView.as_view(), name='delete-medical-record'),
    path('delete-prescription/<int:pk>/', DeletePrescriptionView.as_view(), name='delete-prescription')
   
]
