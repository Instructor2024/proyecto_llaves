from django.urls import path, include
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='login/', permanent=False)),  # Redirect root to login
    path('login/', views.login_admin, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('save-administrators/', views.save_administrators, name='save_administrators'),
    path('index/', views.index_view, name='index'),
    path('form-administrators-view/', views.form_administrators_view, name='form_administrators_view'),
    path('interfas/', views.interfas_index_view, name='interfas_index'),
    path('llaves/', views.llaves_index_view, name='llaves_index'),
    path('pantalla/', views.pantalla_view, name='pantalla'),
    path('vistas/', views.vistas_index_view, name='vistas_index'),
    path('vistas/fragme_14_15/', views.vistas_fragme_14_15_view, name='vistas_fragme_14_15'),
    
    # Environments
    path('environments/', views.environments_view, name='environments'),
    
    # Gestión de Personal
    path('add-personnel/', views.add_personnel_view, name='add_personnel'),
    path('add-personnel/ajax/', views.add_personnel_ajax, name='add_personnel_ajax'),
    path('people/', views.people_view, name='people'),
    path('people/ajax/', views.people_ajax_view, name='people_ajax'),
    path('people/management/', views.people_management_view, name='people_management'),
    path('edit-person/ajax/', views.edit_person_ajax, name='edit_person_ajax'),
    path('delete-person/ajax/', views.delete_person_ajax, name='delete_person_ajax'),
    path('get-person/ajax/', views.get_person_ajax, name='get_person_ajax'),
    path('capture-fingerprint/ajax/', views.capture_fingerprint_ajax, name='biometria_capturar'),
    path('verify-fingerprint/ajax/', views.verify_fingerprint_ajax, name='verify_fingerprint_ajax'),
    
    # Profile
    path('change-password/', views.change_password_view, name='change_password'),
    path('profile-administrator/', views.profile_administrator_view, name='profile_administrator'),
    
    # Logout
    path('logout/', views.logout_view, name='logout'),
]