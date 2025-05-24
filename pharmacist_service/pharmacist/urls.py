from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PrescriptionViewSet, DrugDistributionViewSet

router = DefaultRouter()
router.register(r'pharmacist', PrescriptionViewSet)
router.register(r'drugdistributions', DrugDistributionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
