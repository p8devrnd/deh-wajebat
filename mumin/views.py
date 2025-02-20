from django.shortcuts import render
from django.views import View
from rest_framework.viewsets import ViewSet

from allocation import models as allocation_models
from rest_framework.decorators import action

from rest_framework.response import Response

from allocation.models import JamaatWajebaatMuminRegistration, JamaatMuminMaster, JamaatWajebaatAppointment
from django.utils import timezone
from django.db.models import Q

from allocation.serializer import JamaatWajebaatMuminRegistrationSerializer

import hashlib
import os
import time

"""
Template view for Jamaat admin auth
--------------------------------------
Includes:
- HTML for jamaat login
"""
class ATMuminSelectAppointment(View):
    template_name = 'mumin_self_allocation/main.html'

    def get(self, request, *args, **kwargs):

        all_appointments = allocation_models.JamaatWajebaatAppointment.objects.filter(event_flag=True, slots_left__gt=0).order_by('date','appointment_start_time')

        return render(request, self.template_name, context={'appointments':all_appointments})
    


class ATMuminViewSlotToken(View):
    template_name = 'mumin_self_allocation/mumin_registration_token.html'

    def get(self, request, *args, **kwargs):
        token = self.request.GET.get('token')

        registration_id = JamaatWajebaatMuminRegistration.objects.get(slot_token = token)

        return render(request, self.template_name, {'token':token, 'registration':registration_id})








"""
Mumin-side registration API
--------------------------------------
Includes:
- Fetch if a user has not registered for the event
"""


class ATJamaatMuminFetchRegistrationStatus(ViewSet):


    def __generate_unique_token(self, user_id):
        # Generate unique data to hash (e.g., current timestamp)
        unique_data = str(time.time()) + str(user_id)  # Combining current time and user ID
        
        # Generate a random salt
        salt = os.urandom(16)  # 16 bytes (128 bits) salt
        
        # Add the salt to the unique data
        data_to_hash = salt + unique_data.encode()

        # Hash the data using SHA-256
        hashed_data = hashlib.sha256(data_to_hash).hexdigest()

        # Use a portion of the hashed value as your token number
        token_number = hashed_data[:4]  # Take the first 8 characters as token number

        return token_number

    @action(detail=False, methods=['get'])
    def fetch_registration_status(self, request, *args, **kwargs):
        try:
            its = self.kwargs.get('its')

            if its is not None:
                current_date = timezone.now().date()

                mumin_hof_record =  JamaatMuminMaster.objects.filter(mumin_its=its)
                assert mumin_hof_record.exists(), 'This ITS is not an HOF or from Ezzy Mohalla.'

                takhmeem_done_log = JamaatWajebaatMuminRegistration.objects.filter(status=True, mumin_its__mumin_its=its)

                if takhmeem_done_log.exists():
                    return Response({
                        'status':400,
                        'error':'It seems you have already done Wajebaat Takhmeem.',
                    })


                takhmeem_reallocation_rq_check = JamaatWajebaatMuminRegistration.objects.filter(appointment_id__date__gte=current_date, mumin_its__mumin_its=its)

                if takhmeem_reallocation_rq_check.exists():
                    print('ok1')
                    return Response({
                        'status':300,
                        'error':'Your token is already generated. Click on following link to view the token number.',
                        'redirect_link': '/jamaat/mumin/mumin_registration_token?token='+takhmeem_reallocation_rq_check[0].slot_token
                    })

                else:
                    return Response({
                        'status':200,
                        'mumin_full_name':mumin_hof_record[0].full_name,
                        'message':'Please generate your token number.'
                    })
                
        except AssertionError as e:
            return Response({
                'status':400,
                'error':str(e)
            })

        except Exception as e:
            print(e)
            return Response({
                'status':500,
                'error':'Some issue has occured. Please try again later.'
            })
    


    def create(self, request):
        try:
            
            data = request.data.copy()

            current_date = timezone.now().date()

            unattended_registration = JamaatWajebaatMuminRegistration.objects.filter(mumin_its=data.get('mumin_its'), status=False, appointment_id__date__lt=current_date)

            appointment_instance = JamaatWajebaatAppointment.objects.get(id=int(data['appointment_id']))

            if unattended_registration.exists():
                unattended_registration.delete()


            hash_code = self.__generate_unique_token(int(data['mumin_its']))
            data['slot_token'] = data['slot_token']+''+hash_code+'-'+str(appointment_instance.slot_amount - appointment_instance.slots_left+1)


            print(data)




            registration_serializer = JamaatWajebaatMuminRegistrationSerializer(data=data)
            registration_serializer.is_valid(raise_exception=True)
            registration_obj = registration_serializer.save()

            appointment_id = registration_obj.appointment_id
            slots_left_current = appointment_id.slots_left


            JamaatWajebaatAppointment.objects.filter(id=appointment_id.id).update(slots_left=slots_left_current-1)

            return Response({
                'status':200,
                'new_token':data['slot_token'],
                'message':'Registration is done successfully!'
            })


        except Exception as e:
            print(e)
            return Response({
                'status':500,
                'error':'Some issue has occured. Please try again later.'
            })



    def destroy(self, request, *args, **kwargs):
        try:
            
            token = self.kwargs.get('token')

            registration_token = JamaatWajebaatMuminRegistration.objects.filter(slot_token=token)
            appointment_id = registration_token[0].appointment_id
            appointment_id_value = appointment_id.id
            slots_left = appointment_id.slots_left

            registration_token.delete()

            JamaatWajebaatAppointment.objects.filter(id=appointment_id_value).update(slots_left = slots_left+1)

            return Response({
                'status':204,
                'message':'Token removed sucessfully.'
            })

        except Exception as e:
            print(e)
            return Response({
                'status':500,
                'error':'Some issue has occured. Please try again later.'
            })

