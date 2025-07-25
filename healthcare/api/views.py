from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from api.models import Patients, Doctor, PatientDoctorMapping
from api.serializers import (
    PatientsSerializer,
    DoctorsSerializer,
    PatientDoctorMappingSerializer,
    PatientDoctorMappingCreateSerializer,
    RegisterSerializer
)
from django.contrib.auth.models import User

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class PatientsViewSet(viewsets.ModelViewSet):
    queryset = Patients.objects.all()
    serializer_class = PatientsSerializer
    permission_classes = [permissions.IsAuthenticated]


class DoctorsViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorsSerializer
    permission_classes = [permissions.IsAuthenticated]


class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    queryset = PatientDoctorMapping.objects.all()
    permission_classes = [permissions.IsAuthenticated]


    def get_serializer_class(self):
        if self.action == 'create':
            return PatientDoctorMappingCreateSerializer
        return PatientDoctorMappingSerializer

    def retrieve(self, request, pk=None):
        try:
            patient_id = int(pk)
        except ValueError:
            return Response({"error": "Invalid patient ID"}, status=status.HTTP_400_BAD_REQUEST)

        # Get patient object
        patient = Patients.objects.filter(id=patient_id).first()
        if not patient:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get all mappings for the patient
        mappings = PatientDoctorMapping.objects.filter(patient=patient)
        if not mappings.exists():
            return Response({"message": "No doctors assigned to this patient."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize doctors
        doctors = [mapping.doctor for mapping in mappings]
        doctor_serializer = DoctorsSerializer(doctors, many=True, context={'request': request})

        # Final response
        return Response({
            "patient_id": patient.id,
            "patient_name": patient.name,
            "assigned_doctors": doctor_serializer.data
        }, status=status.HTTP_200_OK)
