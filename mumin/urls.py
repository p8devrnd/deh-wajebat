from django.urls import path
from . import views



urlpatterns = [
    path('mumin_self_allocation/home', views.ATMuminSelectAppointment.as_view(), name='mumin-select-appointment'),
    path('mumin_registration_token', views.ATMuminViewSlotToken.as_view(), name='mumin-registration-token'),


    path('api_mumin_registration_status/<int:its>', views.ATJamaatMuminFetchRegistrationStatus.as_view({'get':'fetch_registration_status'}), name='mumin-registration-status'),
    path('api_mumin_appointment_register', views.ATJamaatMuminFetchRegistrationStatus.as_view({'post':'create'}), name='mumin-appointment-register'),
    path('api_mumin_appointment_cancel_token/<str:token>', views.ATJamaatMuminFetchRegistrationStatus.as_view({'delete':'destroy'}), name='mumin-appointment-cancel-token'),

]