from rest_framework import serializers
from api.models import Patients, Doctor, PatientDoctorMapping
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class PatientsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Patients
        fields = "__all__"

class DoctorsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"


class PatientDoctorMappingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctorMapping
        fields = ['id', 'patient', 'doctor']

class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    patient = PatientsSerializer(read_only=True)
    doctor = DoctorsSerializer(read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = ['id', 'assigned_at', 'patient', 'doctor']
