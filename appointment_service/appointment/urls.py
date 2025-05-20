from django.urls import path
from .views import AppointmentView, AppointmentStatusUpdateView, AppointmentDetailView, GetListAppointmentByPatientId, GetListAppointmentByDoctorId

urlpatterns = [
    path('patients/appointments', AppointmentView.as_view(), name='appointments-list-create'),  # GET list và POST tạo lịch hẹn
    path('patients/appointments/<int:appointment_id>/status', AppointmentStatusUpdateView.as_view(), name='appointment-update-status'),  
    
     #Get thông tin lịch hẹn theo id  
    path('patients/appointments/<int:appointment_id>', AppointmentView.as_view(), name='appointment-detail'),   

    #Get list lịch hẹn theo id bệnh nhân
    path('patients/appointments/patient/<int:patient_id>', GetListAppointmentByPatientId.as_view(), name='appointments-list-by-patient'),  # GET list lịch hẹn theo id bệnh nhân

    #Get list lịch hẹn theo id bác sĩ
    path('patients/appointments/doctor/<int:doctor_id>', GetListAppointmentByDoctorId.as_view(), name='appointments-list-by-doctor'),  # GET list lịch hẹn theo id bác sĩ

]
