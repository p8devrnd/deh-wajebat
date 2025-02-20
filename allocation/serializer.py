from rest_framework.serializers import ModelSerializer
from .models import JamaatWajebaatAppointment, JamaatMuminMaster, JamaatWajebaatMuminRegistration

"""
Wajebaat Appointment serializer
----------------------------------
Includes:
- Create serializer
- List serializer
"""


class JamaatWajebaatAppointmentSerializer(ModelSerializer):
    class Meta:
        model = JamaatWajebaatAppointment
        fields = ['id','date','slot_amount','appointment_start_time','appointment_end_time','slots_left','display_name','jamaat_its','event_flag']



class JamaatWajebaatMuminSerializer(ModelSerializer):
    class Meta:
        model = JamaatMuminMaster
        fields = ['mumin_its','full_name','age','gender','sector', 'sub_sector','jamaat_its']




class JamaatWajebaatMuminRegistrationSerializer(ModelSerializer):
    class Meta:
        model = JamaatWajebaatMuminRegistration
        fields = ['slot_id','mumin_its','appointment_id','slot_token','status']



class JamaatWajebaatMuminRegistrationListSerializer(ModelSerializer):
    appointment_id = JamaatWajebaatAppointmentSerializer(read_only=True)
    mumin_its = JamaatWajebaatMuminSerializer(read_only=True)
    class Meta:
        model = JamaatWajebaatMuminRegistration
        fields = ['slot_id','mumin_its','appointment_id','slot_token','status']