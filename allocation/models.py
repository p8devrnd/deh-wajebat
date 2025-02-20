from jamaat_auth.models import CustomJamaatUser
from django.db import models
from datetime import date, time


class JamaatWajebaatAppointment(models.Model):
    date = models.DateField(null=False, blank=False)
    slot_amount = models.IntegerField(default=0)
    display_name = models.CharField(default='')
    event_flag = models.BooleanField(default=True)
    appointment_start_time = models.TimeField(default=time(0,0,0))
    appointment_end_time = models.TimeField(default=time(0,0,0))
    slots_left = models.IntegerField(null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    jamaat_its = models.ForeignKey(CustomJamaatUser, on_delete=models.CASCADE)

    class Meta:
        db_table = 'wajebaat_appointment_master'



class JamaatMuminMaster(models.Model):
    mumin_its = models.BigAutoField(primary_key=True)
    full_name = models.CharField(max_length=400, default='N/A')
    age = models.IntegerField(null=False, blank=False)
    gender = models.CharField(max_length=20, null=False, blank=False)
    sector = models.CharField(max_length=400, default='N/A')
    sub_sector = models.CharField(max_length=400, default='N/A')
    jamaat_its = models.ForeignKey(CustomJamaatUser, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wajebaat_master_mumin_list'






class JamaatWajebaatMuminRegistration(models.Model):
    slot_id = models.BigAutoField(primary_key=True)
    appointment_id = models.ForeignKey(JamaatWajebaatAppointment, on_delete=models.CASCADE, related_name='appointment')
    mumin_its = models.ForeignKey(JamaatMuminMaster, on_delete=models.CASCADE, related_name='mumin')
    slot_token = models.CharField(max_length=100, null=False, blank=False)
    status = models.BooleanField(max_length=20, default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wajebaat_appointment_mumin_registration'