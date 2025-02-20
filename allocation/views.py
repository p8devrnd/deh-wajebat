from django.shortcuts import render
from django.views import View
from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework.views import APIView
from django.http import HttpResponse, FileResponse

from django import template
import datetime
from django.forms.models import model_to_dict

from rest_framework.response import Response
from rest_framework.exceptions import APIException

from . import serializer, models
import jwt, os, csv, io
from rest_framework.decorators import action

from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins

from rest_framework.generics import ListAPIView
from django.db.models import Q

from io import StringIO
from rest_framework_csv import renderers as r



"""
Jamaat Appointment API
--------------------------------------
Includes:
- Create Jamaat Takhmeem
- HTML for jamaat wajebaat creating an appointment
"""

class ATJamaatWajebaatAppointmentViewSet(ViewSet):


    user = None

    def __fetch_user_request(self, request):
        authorization_header = request.headers.get('Authorization')

        if authorization_header and authorization_header.startswith('Bearer '):
            # Extract the token from the header
            token = authorization_header.split(' ')[1]

            try:
                # Decode the token and get user_id
                decoded_token = jwt.decode(token, os.environ.get('DEH_JWT_TOKEN_SECRET'), algorithms=['HS256'])
                user_id = decoded_token.get('its')

                # Fetch user from the database or any other source
                # For example, if using a custom user model:
                user = models.CustomJamaatUser.objects.get(its=user_id)

                # Return the user
                self.user = user

            except Exception as e:
                raise APIException('Token is corrupt or expired.')
        
        else:
            raise APIException('Token is missing.')


    def list(self, request):
        try:
            self.__fetch_user_request(request)

            appointments = models.JamaatWajebaatAppointment.objects.all().order_by('date','appointment_start_time')
            apointment_serializer = serializer.JamaatWajebaatAppointmentSerializer(appointments, many=True)
            return Response(apointment_serializer.data)
        except APIException as e:
            return Response({
                'status':500,
                'error':'Token seems to be missing or corrupt. Please contact fezzey072@gmail.com or +91 6354023460.'
            })
        except Exception as e:
            return Response({
                'status':500,
                'error':'Some issue has occured. Please try again later.'
            })

    def create(self, request):
        try:

            self.__fetch_user_request(request)

            data = request.data.copy()
            data['slots_left'] = data['slot_amount']
            data['jamaat_its'] = self.user.id
            data['event_flag'] = True

            time_query = Q(appointment_start_time = data['appointment_start_time']) | Q(appointment_end_time = data['appointment_end_time'])

            if models.JamaatWajebaatAppointment.objects.filter(date=data['date']).filter(time_query).exists():
                return Response({
                    'status':400,
                    'error':'Time slot is already booked and completed. Please select today or afterward dates.'
                }, status=400)

            apointment_serializer = serializer.JamaatWajebaatAppointmentSerializer(data=data)
            if apointment_serializer.is_valid():
                apointment_serializer.save()
                return Response({
                    'status':200,
                    'error':'Wajebaat appointment created successfully. View by Going Back'
                }, status=200)
            return Response({
                'status':400,
                'error':'Seems like some values are not valid format. Slot Amount should be numerical (> 0), Name should be string (not blank or empty)'
            })
        except APIException as e:
            return Response({
                'status':500,
                'error':'Token seems to be missing or corrupt. Please contact fezzey072@gmail.com or +91 6354023460.'
            })
        except Exception as e:
            return Response({
                'status':500,
                'error':'Some issue has occured. Please try again later.'
            })

    def partial_update(self, request, pk=None):
        try:

            self.__fetch_user_request(request)

            data = request.data.copy()

            appointment = models.JamaatWajebaatAppointment.objects.get(pk=pk)

            if 'slot_amount' in data.keys():
                
                data['slot_amount'] = int(data['slot_amount'])

                if int(data['slot_amount']) < appointment.slot_amount:
                    return Response({
                        'status':400,
                        'error':'Slot count cannot be small than already specified and entered.'
                    })
                
                
                data['slots_left'] = appointment.slots_left + data['slot_amount'] - appointment.slot_amount
                   

            apointment_serializer = serializer.JamaatWajebaatAppointmentSerializer(appointment, data=data, partial=True)
            if apointment_serializer.is_valid():
                apointment_serializer.save()
                return Response({
                    'status':200,
                    'error':'Edited the slot count successfully'
                })
            return Response(apointment_serializer.errors, status=400)
        except APIException as e:
            return Response({
                'status':500,
                'error':'Token seems to be missing or corrupt. Please contact fezzey072@gmail.com or +91 6354023460.'
            })
        except Exception as e:
            print(e)
            return Response({
                'status':500,
                'error':'Some issue has occured. Please try again later.'
            })


    def destroy(self, request, pk=None):
        try:

            self.__fetch_user_request(request)

            appointment = models.JamaatWajebaatAppointment.objects.get(pk=pk)
            if models.JamaatWajebaatMuminRegistration.objects.filter(appointment_id=appointment).exists():
                return Response({
                    'status':400,
                    'error':'It seems the appointments have registrations associated which prohibits from deleting this appointment.'
                })
            else:
                appointment.delete()
                return Response({
                    'status':200,
                    'error':'Deleted unused appointment slot successfully.'
                })
        except APIException as e:
            return Response({
                'status':500,
                'error':'Token seems to be missing or corrupt. Please contact fezzey072@gmail.com or +91 6354023460.'
            })
        except Exception as e:
            return Response({
                'status':500,
                'error':'Some issue has occured. Please try again later.'
            })











"""
Jamaat Mumineen Master API
--------------------------------------
Includes:
- Upload mumineen using CSV 
- Delete a mumineen data
- Update the mumineen data
- List all mumineen
- Create a single mumin
"""

class JamaatMuminListPaginator(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 200


class ATJamaatWajebaatMumineenMasterViewSet(ViewSet):

    pagination_class = JamaatMuminListPaginator

    def __fetch_user_request(self, request):
        authorization_header = request.headers.get('Authorization')

        if authorization_header and authorization_header.startswith('Bearer '):
            # Extract the token from the header
            token = authorization_header.split(' ')[1]

            try:
                # Decode the token and get user_id
                decoded_token = jwt.decode(token, os.environ.get('DEH_JWT_TOKEN_SECRET'), algorithms=['HS256'])
                user_id = decoded_token.get('its')

                # Fetch user from the database or any other source
                # For example, if using a custom user model:
                user = models.CustomJamaatUser.objects.get(its=user_id)

                # Return the user
                self.user = user

            except Exception as e:
                raise APIException('Token is corrupt or expired.')
        
        else:
            raise APIException('Token is missing.')

    @action(detail=False, methods=['post'])
    def create_by_csv(self, request):
        # Your custom logic here
        
        try:

            self.__fetch_user_request(request)

            data = request.data
            file_obj = data['file']
            # Process the CSV file
            decoded_file = file_obj.read().decode('utf-8')

            # Process the CSV content
            csv_reader = csv.reader(io.StringIO(decoded_file))

            # Assuming the first row contains headers
            skipper = next(csv_reader)
            headers = ['mumin_its', 'full_name', 'age', 'gender', 'sector', 'sub_sector']

            bulk_save_arr = []

            for row in csv_reader:

                instance_data = dict(zip(headers, row))
                instance_data['jamaat_its'] = self.user
                bulk_save_arr.append(models.JamaatMuminMaster(**instance_data))


            models.JamaatMuminMaster.objects.bulk_create(bulk_save_arr) 

            return Response({
                'status':200,
                'message':'All mumineen data uploaded successfully.'
            })
        
        except APIException as e:
            return Response({
                'status':500,
                'error':'Token seems to be missing or corrupt. Please contact fezzey072@gmail.com or +91 6354023460.'
            })
        except Exception as e:
            return Response({
                'status':500,
                'error':'Some issue has occured. Please try again later.'
            })



    def list(self, request):
        try:

            self.__fetch_user_request(request)
            
            all_mumin_list = models.JamaatMuminMaster.objects.all()
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(all_mumin_list, request)
            
            mumin_master_serializer = serializer.JamaatWajebaatMuminSerializer(instance=page, many=True)
            return paginator.get_paginated_response({
                'status':200,
                'count': paginator.page.paginator.count,
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'results': mumin_master_serializer.data,
            })

        except APIException as e:
            return Response({
                'status':500,
                'error':'Token seems to be missing or corrupt. Please contact fezzey072@gmail.com or +91 6354023460.'
            })
        except Exception as e:
            print(e)
            return Response({
                'status':500,
                'error':'Some issue has occured. Please try again later.'
            })
        

    def create(self, request):
        try:
            
            self.__fetch_user_request(request)

            data = request.data.copy()

            mumin_serializer = serializer.JamaatWajebaatMuminSerializer(data=data)
            mumin_serializer.is_valid(raise_exception=True)
            mumin_serializer.save()

            return Response({
                'status':200,
                'message':'User has been created successfully!'
            })

        except APIException as e:
            return Response({
                'status':500,
                'error':'Token seems to be missing or corrupt. Please contact fezzey072@gmail.com or +91 6354023460.'
            })
        except Exception as e:
            print(e)
            return Response({
                'status':500,
                'error':'Some issue has occured. Please try again later.'
            })











"""
Jamaat Mumineen Registration
--------------------------------------
Includes:
- List the paginated registration data
- Mark the status of the token as Done/Not Done
"""

class MyUserRenderer(r.CSVRenderer):
    header = ['first', 'last', 'email']

class ATJamaatWajebaatMumineenRegistrationViewSet(ViewSet):

    pagination_class = JamaatMuminListPaginator

    def __fetch_user_request(self, request):
        authorization_header = request.headers.get('Authorization')

        if authorization_header and authorization_header.startswith('Bearer '):
            # Extract the token from the header
            token = authorization_header.split(' ')[1]

            try:
                # Decode the token and get user_id
                decoded_token = jwt.decode(token, os.environ.get('DEH_JWT_TOKEN_SECRET'), algorithms=['HS256'])
                user_id = decoded_token.get('its')

                # Fetch user from the database or any other source
                # For example, if using a custom user model:
                user = models.CustomJamaatUser.objects.get(its=user_id)

                # Return the user
                self.user = user

            except Exception as e:
                print(e)
                raise APIException('Token is corrupt or expired.')
        
        else:
            raise APIException('Token is missing.')

    def list(self, request):
        try:

            self.__fetch_user_request(request)

            all_registration_list = None

            
            all_registration_list = models.JamaatWajebaatMuminRegistration.objects.select_related('appointment_id','mumin_its').filter(
                Q(appointment_id__date=request.GET.get('date')) if request.GET.get('date') is not None and request.GET.get('date') != '' else Q(),
                Q(appointment_id__appointment_start_time=request.GET.get('appointment_start_time')) if request.GET.get('appointment_start_time') is not None and request.GET.get('appointment_start_time') != '' else Q()
            ).order_by('created_on')
            
            
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(all_registration_list, request)
            
            registration_data_serializer = serializer.JamaatWajebaatMuminRegistrationListSerializer(instance=page, many=True)


            return paginator.get_paginated_response({
                'status':200,
                'count': paginator.page.paginator.count,
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'results': registration_data_serializer.data,
            })

        except APIException as e:
            return Response({
                'status':500,
                'error':'Token seems to be missing or corrupt. Please contact fezzey072@gmail.com or +91 6354023460.'
            })
        except Exception as e:
            print(e)
            return Response({
                'status':500,
                'error':'Some issue has occured. Please try again later.'
            })


    @action(detail=False, methods=['put'])
    def toggle_takhmeem_status(self, request, pk=None):

        try:

            self.__fetch_user_request(request)


            data=request.data
            registration_instance = models.JamaatWajebaatMuminRegistration.objects.get(slot_id=pk)
            
            mumin_token_registration_serializer = serializer.JamaatWajebaatMuminRegistrationSerializer(instance=registration_instance, data=data, partial=True)

            
            

            mumin_token_registration_serializer.is_valid(raise_exception=True)

            print('chk 21')
            mumin_token_registration_serializer.save()

            return Response({
                'status':200,
                'message':'Token status change to Done.'
            })

        except APIException as e:
            print(e)
            return Response({
                'status':500,
                'error':'Token seems to be missing or corrupt. Please contact fezzey072@gmail.com or +91 6354023460.'
            })
        except Exception as e:
            print(e)
            return Response({
                'status':500,
                'error':'Some issue has occured. Please try again later.'
            })
        

    
        
class MyCSVView(APIView):
    renderer_classes = [r.CSVRenderer]

    def get(self, request, *args, **kwargs):
        

        try:
            all_registration_list = models.JamaatWajebaatMuminRegistration.objects.select_related('appointment_id','mumin_its').filter(
                Q(appointment_id__date=request.GET.get('date')) if request.GET.get('date') is not None and request.GET.get('date') != '' else Q(),
                Q(appointment_id__appointment_start_time=request.GET.get('appointment_start_time')) if request.GET.get('appointment_start_time') is not None and request.GET.get('appointment_start_time') != '' else Q()
            ).order_by('created_on')


            csv_data = []
            serialized_registration_list = serializer.JamaatWajebaatMuminRegistrationListSerializer(all_registration_list, many=True).data

            for registration_data in serialized_registration_list:
                obj = {
                    'Date':registration_data['appointment_id']['date'],
                    'ITS':registration_data['mumin_its']['mumin_its'],
                    'Name':registration_data['mumin_its']['full_name'],
                    'Slot_No':registration_data['slot_token'],
                    'Takhmeem_Time_Slot':f"{registration_data['appointment_id']['appointment_start_time']} to {registration_data['appointment_id']['appointment_end_time']}",
                    'Takhmeem_Status':'NOT DONE' if not registration_data['status'] else 'DONE'
                }

                csv_data.append(obj)

            return Response(csv_data)
        except APIException as e:
            print(e)
            return Response({
                'status':500,
                'error':'Token seems to be missing or corrupt. Please contact fezzey072@gmail.com or +91 6354023460.'
            })
        except Exception as e:
            print(e)
            return Response({
                'status':500,
                'error':'Some issue has occured. Please try again later.'
            })
        
    







"""
Template view for Jamaat allocation
--------------------------------------
Includes:
- HTML for jamaat wajebaat appointment home
- HTML for jamaat wajebaat creating an appointment
"""
class ATJamaatAdminWajebaatAppointment(View):
    template_name = 'wajebaat_appointment/main.html'

    def get(self, request, *args, **kwargs):

        appointment = models.JamaatWajebaatAppointment.objects.all().order_by('date','appointment_start_time')
        appointments_serializer = serializer.JamaatWajebaatAppointmentSerializer(instance=appointment, many=True)

        return render(request, self.template_name, context={'appointments':appointments_serializer.data})


class ATJamaatAdminCreateWajebaatAppointment(View):
    template_name = 'wajebaat_appointment/create_wajebaat_appointment.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    


class ATJamaatAdminWajebaatMuminMaster(View):
    template_name = 'wajebaat_mumin_master/main.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    


class ATJamaatAdminWajebaatMuminRegistration(View):
    template_name = 'wajebaat_registration_data/main.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
