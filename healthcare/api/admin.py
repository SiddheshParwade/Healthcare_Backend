from django.contrib import admin
from .models import Patients, Doctor, PatientDoctorMapping

admin.site.register(Patients)
admin.site.register(Doctor)
admin.site.register(PatientDoctorMapping)