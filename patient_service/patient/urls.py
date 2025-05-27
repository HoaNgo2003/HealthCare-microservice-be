from django.urls import path
from .views import AppointmentView, AppointmentStatusUpdateView, AppointmentDetailView, GetListAppointmentByPatientId, GetListAppointmentByDoctorId, AppointmentUpdateView, AppointmentDeleteView
from .views import PatientMedicalRecordsView, PatientPrescriptionsView
urlpatterns = [
    path('patients/appointments', AppointmentView.as_view(), name='appointments-list-create'),  # GET list và POST tạo lịch hẹn
    path('patients/appointments/<int:appointment_id>/status', AppointmentStatusUpdateView.as_view(), name='appointment-update-status'),  
    
     #Get thông tin lịch hẹn theo id  
    path('patients/appointments/<int:appointment_id>', AppointmentDetailView.as_view(), name='appointment-detail'),   

    #Get list lịch hẹn theo id bệnh nhân
    path('patients/appointments/patient/<int:patient_id>', GetListAppointmentByPatientId.as_view(), name='appointments-list-by-patient'),  # GET list lịch hẹn theo id bệnh nhân

    #Get list lịch hẹn theo id bác sĩ
    path('patients/appointments/doctor/<int:doctor_id>', GetListAppointmentByDoctorId.as_view(), name='appointments-list-by-doctor'),  # GET list lịch hẹn theo id bác sĩ
    path('appointments/<int:appointment_id>/update/', AppointmentUpdateView.as_view(), name='appointment-update'),
    
    path('delete/<int:appointment_id>', AppointmentDeleteView.as_view(), name='appointment-delete'),  # DELETE lịch hẹn theo id
    
     path('patient/medical-records/<int:patient_id>/', PatientMedicalRecordsView.as_view(), name='patient-medical-records'),
    path('patient/prescriptions/<int:patient_id>/', PatientPrescriptionsView.as_view(), name='patient-prescriptions'),
]
