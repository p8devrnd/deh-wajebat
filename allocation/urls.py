from django.urls import path
from . import views


urlpatterns = [
    path('wajebaat_appointment', views.ATJamaatAdminWajebaatAppointment.as_view(), name='jamaat-wajebaat-appointment'),
    path('create_wajebaat_appointment', views.ATJamaatAdminCreateWajebaatAppointment.as_view(), name='jamaat-create-wajebaat-appointment'),
    path('wajebaat_mumin_master', views.ATJamaatAdminWajebaatMuminMaster.as_view(), name='jamaat-mumin-master'),
    path('wajebaat_registration_data', views.ATJamaatAdminWajebaatMuminRegistration.as_view(), name='jamaat-wajebaat-registration-data'),
    


    path('api_wajebaat_create_appointment', views.ATJamaatWajebaatAppointmentViewSet.as_view({'post':'create'}), name='jamaat-create-wajebaat-appointment-api-view'),
    path('api_wajebaat_list_appointment', views.ATJamaatWajebaatAppointmentViewSet.as_view({'get':'list'}), name='jamaat-list-wajebaat-appointment-api-view'),
    path('api_wajebaat_delete_appointment/<int:pk>', views.ATJamaatWajebaatAppointmentViewSet.as_view({'delete':'destroy'}), name='jamaat-destroy-wajebaat-appointment-api-view'),
    path('api_wajebaat_edit_appointment/<int:pk>', views.ATJamaatWajebaatAppointmentViewSet.as_view({'put':'partial_update'}), name='jamaat-update-wajebaat-appointment-api-view'),


    path('api_wajebaat_mumin_create_by_csv', views.ATJamaatWajebaatMumineenMasterViewSet.as_view({'post':'create_by_csv'}), name='jamaat-create-wajebaat-mumin-by-csv'),
    path('api_wajebaat_mumin_list', views.ATJamaatWajebaatMumineenMasterViewSet.as_view({'get':'list'}), name='jamaat-list-wajebaat-mumin'),


    path('api_wajebaat_registration_data', views.ATJamaatWajebaatMumineenRegistrationViewSet.as_view({'get':'list'}), name='jamaat-create-wajebaat-mumin-by-csv'),
    path('api_toggle_takhmeem_status/<int:pk>', views.ATJamaatWajebaatMumineenRegistrationViewSet.as_view({'put':'toggle_takhmeem_status'}), name='jamaat-toggle-wajebaat-takhmeem-status'),

    path('export_csv',views.MyCSVView.as_view(), name='export-data'),
]