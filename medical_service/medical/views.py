# medical/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MedicalRecord, Prescription
from .serializers import MedicalRecordSerializer, PrescriptionSerializer

class MedicalRecordCreateView(APIView):
    def post(self, request):
        serializer = MedicalRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk):
        try:
            record = MedicalRecord.objects.get(pk=pk)
            serializer = MedicalRecordSerializer(record, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MedicalRecord.DoesNotExist:
            return Response({'detail': 'Medical Record not found'}, status=status.HTTP_404_NOT_FOUND)
    

class PrescriptionCreateView(APIView):
    def post(self, request):
        serializer = PrescriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk):
        try:
            prescription = Prescription.objects.get(pk=pk)
            serializer = PrescriptionSerializer(prescription, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Prescription.DoesNotExist:
            return Response({'detail': 'Prescription not found'}, status=status.HTTP_404_NOT_FOUND)


class GetListMedicalRecordView(APIView):
    def get(self, request):
        records = MedicalRecord.objects.all()
        serializer = MedicalRecordSerializer(records, many=True)
        return Response(serializer.data)
class GetListPrescriptionView(APIView):
    def get(self, request):
        prescriptions = Prescription.objects.all()
        serializer = PrescriptionSerializer(prescriptions, many=True)
        return Response(serializer.data)
class GetMedicalRecordByIdView(APIView):
    def get(self, request, pk):
        try:
            record = MedicalRecord.objects.get(pk=pk)
            serializer = MedicalRecordSerializer(record)
            return Response(serializer.data)
        except MedicalRecord.DoesNotExist:
            return Response({'detail': 'Medical Record not found'}, status=status.HTTP_404_NOT_FOUND)
class GetPrescriptionByIdView(APIView):
    def get(self, request, pk):
        try:
            prescription = Prescription.objects.get(pk=pk)
            serializer = PrescriptionSerializer(prescription)
            return Response(serializer.data)
        except Prescription.DoesNotExist:
            return Response({'detail': 'Prescription not found'}, status=status.HTTP_404_NOT_FOUND)
class GetListMedicalRecordByPatientIdView(APIView):
    def get(self, request, patient_id):
        records = MedicalRecord.objects.filter(patient_id=patient_id)
        serializer = MedicalRecordSerializer(records, many=True)
        return Response(serializer.data)
class GetListPrescriptionByPatientIdView(APIView):
    def get(self, request, patient_id):
        prescriptions = Prescription.objects.filter(patient_id=patient_id)
        serializer = PrescriptionSerializer(prescriptions, many=True)
        return Response(serializer.data)
class GetListMedicalRecordByDoctorIdView(APIView):
    def get(self, request, doctor_id):
        records = MedicalRecord.objects.filter(doctor_id=doctor_id)
        serializer = MedicalRecordSerializer(records, many=True)
        return Response(serializer.data)
class GetListPrescriptionByDoctorIdView(APIView):
    def get(self, request, doctor_id):
        prescriptions = Prescription.objects.filter(doctor_id=doctor_id)
        serializer = PrescriptionSerializer(prescriptions, many=True)
        return Response(serializer.data)
class GetListMedicalRecordByPatientIdAndDoctorIdView(APIView):
    def get(self, request, patient_id, doctor_id):
        records = MedicalRecord.objects.filter(patient_id=patient_id, doctor_id=doctor_id)
        serializer = MedicalRecordSerializer(records, many=True)
        return Response(serializer.data)
class GetListPrescriptionByPatientIdAndDoctorIdView(APIView):
    def get(self, request, patient_id, doctor_id):
        prescriptions = Prescription.objects.filter(patient_id=patient_id, doctor_id=doctor_id)
        serializer = PrescriptionSerializer(prescriptions, many=True)
        return Response(serializer.data)

class DeleteMedicalRecordView(APIView):
    def delete(self, request, pk):
        try:
            record = MedicalRecord.objects.get(pk=pk)
            record.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except MedicalRecord.DoesNotExist:
            return Response({'detail': 'Medical Record not found'}, status=status.HTTP_404_NOT_FOUND)
class DeletePrescriptionView(APIView):
    def delete(self, request, pk):
        try:
            prescription = Prescription.objects.get(pk=pk)
            prescription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Prescription.DoesNotExist:
            return Response({'detail': 'Prescription not found'}, status=status.HTTP_404_NOT_FOUND)