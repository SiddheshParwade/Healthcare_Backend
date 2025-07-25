from django.urls import path, include
from api.views import PatientsViewSet, DoctorsViewSet, PatientDoctorMappingViewSet, RegisterView
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register(r'patients', PatientsViewSet)
router.register(r'doctors', DoctorsViewSet)
router.register(r'mappings', PatientDoctorMappingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
