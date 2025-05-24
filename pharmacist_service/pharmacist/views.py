from rest_framework import viewsets
from .models import Prescription
from .serializers import PrescriptionSerializer
from .serializers import DrugDistributionSerializer
from .models import DrugDistribution
class DrugDistributionViewSet(viewsets.ModelViewSet):
    queryset = DrugDistribution.objects.all()
    serializer_class = DrugDistributionSerializer
class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer