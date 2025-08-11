from .models import Administrators, Users, EnvironmentInstructorPrograms, Environments, People
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .forms import Administrators_Form
from django.http import JsonResponse, HttpResponseNotAllowed
import threading
import time
from django.db import transaction
from datetime import datetime
import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.db import connection
from django.core.paginator import Paginator
import hashlib
from django.db.models import Q
from base64 import b64encode 
from django.utils import timezone
import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse

@ensure_csrf_cookie
def login_admin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Buscar usuario por email en la tabla users de sicefa
            user = Users.objects.get(email=email)
            
            # Verificar contraseña (comparación directa)
            if user.password == password:
                # Crear un objeto de sesión personalizado
                request.session['user_id'] = user.id
                request.session['user_email'] = user.email
                request.session['user_name'] = user.nickname or user.email
                request.session['is_authenticated'] = True
                
                messages.success(request, 'Inicio de sesión exitoso.')
                return redirect('dashboard')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        except Users.DoesNotExist:
            messages.error(request, 'No existe ese usuario.')

    return render(request, 'aplicacion_llaves/llaves/interfaces/Login/login.html')

def dashboard_view(request):
    if not request.session.get('is_authenticated'):
        return redirect('login')
    
    nickname = request.session.get('user_name', 'Usuario')
    user_email = request.session.get('user_email', '')
    
    return render(request, 'aplicacion_llaves/llaves/interfaces/Dashboard/dashboard.html', {
        'nickname': nickname,
        'user_email': user_email
    })

def save_administrators(request):
    if request.method == 'POST':
        form = Administrators_Form(request.POST)
        if form.is_valid():
            save_administrators = form.save(commit=False)
            # Hash the password before saving if not already handled by the form
            if 'password' in form.cleaned_data:
                save_administrators.password = make_password(form.cleaned_data['password'])
            save_administrators.save()
            messages.success(request, 'Administrador guardado exitosamente.')
            return redirect('save_administrators')  # Or another view
        else:
            messages.error(request, 'Error en el formulario.')
            return render(request, 'form_administrators.html', {'form': form})
    form = Administrators_Form()
    return render(request, 'form_administrators.html', {'form': form})

def index_view(request):
    return render(request, 'aplicacion_llaves/index.html')

def form_administrators_view(request):
    return render(request, 'aplicacion_llaves/form_administrators.html')

def interfas_index_view(request):
    return render(request, 'aplicacion_llaves/llaves/interfas/index.html')

def llaves_index_view(request):
    return render(request, 'aplicacion_llaves/llaves/llaves/index.html')

def pantalla_view(request):
    return render(request, 'aplicacion_llaves/llaves/pantalla/pantalla.html')

def vistas_index_view(request):
    if not request.session.get('is_authenticated'):
        return redirect('login')
    
    nickname = request.session.get('user_name', 'Usuario')
    user_email = request.session.get('user_email', '')
    
    return render(request, 'aplicacion_llaves/llaves/vistas/Index.html', {
        'nickname': nickname,
        'user_email': user_email
    })

def vistas_fragme_14_15_view(request):
    if not request.session.get('is_authenticated'):
        return redirect('login')
    
    nickname = request.session.get('user_name', 'Usuario')
    user_email = request.session.get('user_email', '')
    
    # Consultar todos los registros de environment_instructor_programs
    try:
        programs = EnvironmentInstructorPrograms.objects.all().order_by('-created_at')
        
        # Obtener estadísticas
        total_programs = programs.count()
        active_programs = programs.filter(deleted_at__isnull=True).count()
        deleted_programs = programs.filter(deleted_at__isnull=False).count()
        
        # Paginación - configurable
        page_size = request.GET.get('page_size', 50)
        try:
            page_size = int(page_size)
        except ValueError:
            page_size = 50
        
        paginator = Paginator(programs, page_size)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'nickname': nickname,
            'user_email': user_email,
            'programs': page_obj,
            'page_obj': page_obj,
            'total_programs': total_programs,
            'active_programs': active_programs,
            'deleted_programs': deleted_programs,
            'page_size': page_size,
        }
    except Exception as e:
        context = {
            'nickname': nickname,
            'user_email': user_email,
            'programs': [],
            'total_programs': 0,
            'active_programs': 0,
            'deleted_programs': 0,
            'page_size': 50,
            'error': str(e)
        }
    
    return render(request, 'aplicacion_llaves/llaves/vistas/fragme_14_15.html', context)

def profile_administrator_view(request):
    if not request.session.get('is_authenticated'):
        return redirect('login')
    
    nickname = request.session.get('user_name', 'Usuario')
    user_email = request.session.get('user_email', '')
    
    return render(request, 'aplicacion_llaves/llaves/interfaces/Profile/administrator_profile.html', {
        'nickname': nickname,
        'user_email': user_email
    })

def login_dashboard_view(request):
    return render(request, 'aplicacion_llaves/llaves/interfaces/Login/dashboard.html')

def login_login_view(request):
    return render(request, 'aplicacion_llaves/llaves/interfaces/Login/login.html')

def environments_view(request):
    if not request.session.get('is_authenticated'):
        return redirect('login')
    
    nickname = request.session.get('user_name', 'Usuario')
    user_email = request.session.get('user_email', '')
    
    # Consultar todos los registros de environments
    try:
        environments = Environments.objects.all().order_by('-created_at')
        
        # Obtener estadísticas
        total_environments = environments.count()
        available_environments = environments.filter(status='Disponible').count()
        unavailable_environments = environments.exclude(status='Disponible').count()
        deleted_environments = environments.filter(deleted_at__isnull=False).count()
        
        # Paginación - configurable
        page_size = request.GET.get('page_size', 50)
        try:
            page_size = int(page_size)
        except ValueError:
            page_size = 50
        
        paginator = Paginator(environments, page_size)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'nickname': nickname,
            'user_email': user_email,
            'environments': page_obj,
            'page_obj': page_obj,
            'total_environments': total_environments,
            'available_environments': available_environments,
            'unavailable_environments': unavailable_environments,
            'deleted_environments': deleted_environments,
            'page_size': page_size,
        }
    except Exception as e:
        context = {
            'nickname': nickname,
            'user_email': user_email,
            'environments': [],
            'total_environments': 0,
            'available_environments': 0,
            'unavailable_environments': 0,
            'deleted_environments': 0,
            'page_size': 50,
            'error': str(e)
        }
    
    return render(request, 'aplicacion_llaves/llaves/interfaces/Environments/environments.html', context)

def dashboard_html_view(request):
    return render(request, 'aplicacion_llaves/llaves/interfaces/Dashboard/dashboard.html')

def change_password_view(request):
    if not request.session.get('is_authenticated'):
        return redirect('login')
    
    nickname = request.session.get('user_name', 'Usuario')
    user_email = request.session.get('user_email', '')
    
    return render(request, 'aplicacion_llaves/llaves/interfaces/Profile/change_password.html', {
        'nickname': nickname,
        'user_email': user_email
    })

def logout_view(request):
    # Cerrar sesión personalizada
    request.session.flush()
    messages.success(request, 'Sesión cerrada exitosamente.')
    return redirect('login')

@csrf_exempt
def people_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            # Añadir nueva persona
            try:
                people = People.objects.create(
                    document_type=request.POST.get('document_type'),
                    document_number=request.POST.get('document_number'),
                    date_of_issue=request.POST.get('date_of_issue') or None,
                    first_name=request.POST.get('first_name'),
                    first_last_name=request.POST.get('first_last_name'),
                    second_last_name=request.POST.get('second_last_name'),
                    date_of_birth=request.POST.get('date_of_birth') or None,
                    blood_type=request.POST.get('blood_type'),
                    gender=request.POST.get('gender'),
                    eps_id=request.POST.get('eps_id'),
                    marital_status=request.POST.get('marital_status'),
                    military_card=request.POST.get('military_card') or None,
                    socioeconomical_status=request.POST.get('socioeconomical_status'),
                    sisben_level=request.POST.get('sisben_level'),
                    address=request.POST.get('address'),
                    telephone1=request.POST.get('telephone1') or None,
                    telephone2=request.POST.get('telephone2') or None,
                    telephone3=request.POST.get('telephone3') or None,
                    personal_email=request.POST.get('personal_email'),
                    misena_email=request.POST.get('misena_email'),
                    sena_email=request.POST.get('sena_email'),
                    avatar=request.POST.get('avatar'),
                    biometric_code=request.POST.get('biometric_code'),
                    population_group_id=request.POST.get('population_group_id'),
                    pension_entity_id=request.POST.get('pension_entity_id'),
                    created_at=timezone.now(),
                    updated_at=timezone.now()
                )
                return JsonResponse({'success': True, 'message': 'Persona agregada exitosamente'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
        
        elif action == 'edit':
            # Editar persona existente
            try:
                people_id = request.POST.get('id')
                people = get_object_or_404(People, id=people_id)
                
                people.document_type = request.POST.get('document_type')
                people.document_number = request.POST.get('document_number')
                people.date_of_issue = request.POST.get('date_of_issue') or None
                people.first_name = request.POST.get('first_name')
                people.first_last_name = request.POST.get('first_last_name')
                people.second_last_name = request.POST.get('second_last_name')
                people.date_of_birth = request.POST.get('date_of_birth') or None
                people.blood_type = request.POST.get('blood_type')
                people.gender = request.POST.get('gender')
                people.eps_id = request.POST.get('eps_id')
                people.marital_status = request.POST.get('marital_status')
                people.military_card = request.POST.get('military_card') or None
                people.socioeconomical_status = request.POST.get('socioeconomical_status')
                people.sisben_level = request.POST.get('sisben_level')
                people.address = request.POST.get('address')
                people.telephone1 = request.POST.get('telephone1') or None
                people.telephone2 = request.POST.get('telephone2') or None
                people.telephone3 = request.POST.get('telephone3') or None
                people.personal_email = request.POST.get('personal_email')
                people.misena_email = request.POST.get('misena_email')
                people.sena_email = request.POST.get('sena_email')
                people.avatar = request.POST.get('avatar')
                people.biometric_code = request.POST.get('biometric_code')
                people.population_group_id = request.POST.get('population_group_id')
                people.pension_entity_id = request.POST.get('pension_entity_id')
                people.updated_at = timezone.now()
                
                people.save()
                return JsonResponse({'success': True, 'message': 'Persona actualizada exitosamente'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
        
        elif action == 'delete':
            # Eliminar persona (soft delete)
            try:
                people_id = request.POST.get('id')
                people = get_object_or_404(People, id=people_id)
                people.deleted_at = timezone.now()
                people.save()
                return JsonResponse({'success': True, 'message': 'Persona eliminada exitosamente'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
        
        elif action == 'get_person':
            # Obtener datos de una persona específica
            try:
                people_id = request.POST.get('id')
                people = get_object_or_404(People, id=people_id)
                return JsonResponse({
                    'success': True,
                    'data': {
                        'id': people.id,
                        'document_type': people.document_type,
                        'document_number': people.document_number,
                        'date_of_issue': people.date_of_issue.strftime('%Y-%m-%d') if people.date_of_issue else '',
                        'first_name': people.first_name,
                        'first_last_name': people.first_last_name,
                        'second_last_name': people.second_last_name,
                        'date_of_birth': people.date_of_birth.strftime('%Y-%m-%d') if people.date_of_birth else '',
                        'blood_type': people.blood_type,
                        'gender': people.gender,
                        'eps_id': people.eps_id,
                        'marital_status': people.marital_status,
                        'military_card': people.military_card,
                        'socioeconomical_status': people.socioeconomical_status,
                        'sisben_level': people.sisben_level,
                        'address': people.address,
                        'telephone1': people.telephone1,
                        'telephone2': people.telephone2,
                        'telephone3': people.telephone3,
                        'personal_email': people.personal_email,
                        'misena_email': people.misena_email,
                        'sena_email': people.sena_email,
                        'avatar': people.avatar,
                        'biometric_code': people.biometric_code,
                        'population_group_id': people.population_group_id,
                        'pension_entity_id': people.pension_entity_id,
                    }
                })
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
    
    # GET request - mostrar la vista
    search_query = request.GET.get('search', '')
    filter_type = request.GET.get('filter_type', '')
    page_size = int(request.GET.get('page_size', 50))
    
    # Consulta base
    people_list = People.objects.filter(deleted_at__isnull=True)
    
    # Aplicar filtros de búsqueda
    if search_query:
        people_list = people_list.filter(
            Q(first_name__icontains=search_query) |
            Q(first_last_name__icontains=search_query) |
            Q(second_last_name__icontains=search_query) |
            Q(document_number__icontains=search_query) |
            Q(personal_email__icontains=search_query) |
            Q(misena_email__icontains=search_query) |
            Q(sena_email__icontains=search_query)
        )
    
    # Aplicar filtros adicionales
    if filter_type == 'with_biometric':
        people_list = people_list.exclude(biometric_code__isnull=True).exclude(biometric_code='')
    elif filter_type == 'without_biometric':
        people_list = people_list.filter(Q(biometric_code__isnull=True) | Q(biometric_code=''))
    
    # Ordenar por nombre
    people_list = people_list.order_by('first_name', 'first_last_name')
    
    # Paginación
    paginator = Paginator(people_list, page_size)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estadísticas
    total_people = people_list.count()
    with_biometric = people_list.exclude(biometric_code__isnull=True).exclude(biometric_code='').count()
    without_biometric = total_people - with_biometric
    
    context = {
        'page_obj': page_obj,
        'page_size': page_size,
        'search_query': search_query,
        'filter_type': filter_type,
        'total_people': total_people,
        'with_biometric': with_biometric,
        'without_biometric': without_biometric,
    }
    
    return render(request, 'aplicacion_llaves/llaves/interfaces/People/people.html', context)

@csrf_exempt
def people_ajax_view(request):
    """Maneja las solicitudes AJAX para la gestión de personal (editar, eliminar, obtener)"""
    if not request.session.get('is_authenticated'):
        return JsonResponse({'success': False, 'message': 'No autorizado'})
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'get':
            # Obtener datos de una persona específica
            person_id = request.POST.get('id')
            try:
                person = People.objects.get(id=person_id)
                return JsonResponse({
                    'success': True,
                    'person': {
                        'id': person.id,
                        'first_name': person.first_name,
                        'first_last_name': person.first_last_name,
                        'second_last_name': person.second_last_name,
                        'personal_email': person.personal_email,
                        'document_type': person.document_type,
                        'document_number': person.document_number,
                        'biometric_code': person.biometric_code,
                        'created_at': person.created_at.strftime('%d/%m/%Y %H:%M') if person.created_at else None
                    }
                })
            except People.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Persona no encontrada'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
        
        elif action == 'edit':
            # Editar una persona existente
            try:
                person_id = request.POST.get('person_id')
                nombres = request.POST.get('nombres', '').strip()
                apellidos = request.POST.get('apellidos', '').strip()
                correo = request.POST.get('correo', '').strip()
                tipo_documento = request.POST.get('tipo_documento')
                numero_documento = request.POST.get('numero_documento', '').strip()
                datos_huella = request.POST.get('datos_huella', '').strip()
                
                # Validaciones
                if not nombres or not apellidos or not tipo_documento or not numero_documento:
                    return JsonResponse({
                        'success': False, 
                        'message': 'Todos los campos obligatorios deben estar completos'
                    })
                
                # Obtener la persona
                try:
                    person = People.objects.get(id=person_id)
                except People.DoesNotExist:
                    return JsonResponse({'success': False, 'message': 'Persona no encontrada'})
                
                # Verificar si el número de documento ya existe en otra persona
                existing_person = People.objects.filter(document_number=numero_documento).exclude(id=person_id).first()
                if existing_person:
                    return JsonResponse({
                        'success': False, 
                        'message': f'Ya existe otra persona con el número de documento {numero_documento}'
                    })
                
                # Actualizar datos
                person.first_name = nombres.upper()
                person.first_last_name = apellidos.upper()
                person.personal_email = correo if correo else None
                person.document_type = tipo_documento
                person.document_number = numero_documento
                person.biometric_code = datos_huella if datos_huella and datos_huella != 'Huella no registrada' else None
                person.save()
                
                return JsonResponse({
                    'success': True, 
                    'message': f'Personal actualizado exitosamente'
                })
                
            except Exception as e:
                return JsonResponse({
                    'success': False, 
                    'message': f'Error al actualizar personal: {str(e)}'
                })
        
        elif action == 'delete':
            # Eliminar una persona (marcar como eliminada)
            try:
                person_id = request.POST.get('id')
                person = People.objects.get(id=person_id)
                person.deleted_at = timezone.now()
                person.save()
                
                return JsonResponse({
                    'success': True, 
                    'message': 'Personal eliminado exitosamente'
                })
                
            except People.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Persona no encontrada'})
            except Exception as e:
                return JsonResponse({
                    'success': False, 
                    'message': f'Error al eliminar personal: {str(e)}'
                })
    
    return JsonResponse({'success': False, 'message': 'Acción no válida'})

def people_management_view(request):
    if not request.session.get('is_authenticated'):
        return redirect('login')
    
    nickname = request.session.get('user_name', 'Usuario')
    user_email = request.session.get('user_email', '')
    
    # Consultar todos los registros de people
    try:
        people_list = People.objects.all().order_by('-created_at')
        
        # Obtener estadísticas
        total_people = people_list.count()
        active_people = people_list.filter(deleted_at__isnull=True).count()
        deleted_people = people_list.filter(deleted_at__isnull=False).count()
        with_biometric = people_list.exclude(biometric_code__isnull=True).exclude(biometric_code='').count()
        without_biometric = total_people - with_biometric
        
        # Aplicar filtros de búsqueda
        search_query = request.GET.get('search', '')
        filter_type = request.GET.get('filter_type', '')
        
        if search_query:
            people_list = people_list.filter(
                Q(first_name__icontains=search_query) |
                Q(first_last_name__icontains=search_query) |
                Q(second_last_name__icontains=search_query) |
                Q(document_number__icontains=search_query) |
                Q(personal_email__icontains=search_query) |
                Q(misena_email__icontains=search_query) |
                Q(sena_email__icontains=search_query)
            )
        
        # Aplicar filtros adicionales
        if filter_type == 'with_biometric':
            people_list = people_list.exclude(biometric_code__isnull=True).exclude(biometric_code='')
        elif filter_type == 'without_biometric':
            people_list = people_list.filter(Q(biometric_code__isnull=True) | Q(biometric_code=''))
        elif filter_type == 'active':
            people_list = people_list.filter(deleted_at__isnull=True)
        elif filter_type == 'deleted':
            people_list = people_list.filter(deleted_at__isnull=False)
        
        # Paginación - configurable
        page_size = request.GET.get('page_size', 50)
        try:
            page_size = int(page_size)
        except ValueError:
            page_size = 50
        
        paginator = Paginator(people_list, page_size)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'nickname': nickname,
            'user_email': user_email,
            'people': page_obj,
            'page_obj': page_obj,
            'total_people': total_people,
            'active_people': active_people,
            'deleted_people': deleted_people,
            'with_biometric': with_biometric,
            'without_biometric': without_biometric,
            'page_size': page_size,
            'search_query': search_query,
            'filter_type': filter_type,
        }
    except Exception as e:
        context = {
            'nickname': nickname,
            'user_email': user_email,
            'people': [],
            'total_people': 0,
            'active_people': 0,
            'deleted_people': 0,
            'with_biometric': 0,
            'without_biometric': 0,
            'page_size': 50,
            'search_query': '',
            'filter_type': '',
            'error': str(e)
        }
    
    return render(request, 'aplicacion_llaves/llaves/vistas/people_management.html', context)

def add_personnel_view(request):
    if not request.session.get('is_authenticated'):
        return redirect('login')
    
    nickname = request.session.get('user_name', 'Usuario')
    user_email = request.session.get('user_email', '')
    
    # Consultar todos los registros de people (solo activos)
    try:
        people_list = People.objects.all().order_by('-created_at')
        
        # Obtener estadísticas
        total_people = people_list.count()
        active_people = people_list.count()  # Todas las personas activas
        deleted_people = 0  # No mostramos eliminadas
        with_biometric = people_list.exclude(biometric_code__isnull=True).exclude(biometric_code='').count()
        without_biometric = total_people - with_biometric
        
        # Aplicar filtros de búsqueda
        search_query = request.GET.get('search', '')
        filter_type = request.GET.get('filter_type', '')
        
        if search_query:
            people_list = people_list.filter(
                Q(first_name__icontains=search_query) |
                Q(first_last_name__icontains=search_query) |
                Q(second_last_name__icontains=search_query) |
                Q(document_number__icontains=search_query) |
                Q(personal_email__icontains=search_query) |
                Q(misena_email__icontains=search_query) |
                Q(sena_email__icontains=search_query)
            )
        
        # Aplicar filtros adicionales
        if filter_type == 'with_biometric':
            people_list = people_list.exclude(biometric_code__isnull=True).exclude(biometric_code='')
        elif filter_type == 'without_biometric':
            people_list = people_list.filter(Q(biometric_code__isnull=True) | Q(biometric_code=''))
        elif filter_type == 'active':
            people_list = people_list.filter(deleted_at__isnull=True)
        elif filter_type == 'deleted':
            people_list = people_list.filter(deleted_at__isnull=False)
        
        # Paginación
        paginator = Paginator(people_list, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'nickname': nickname,
            'user_email': user_email,
            'people': page_obj,
            'page_obj': page_obj,
            'total_people': total_people,
            'active_people': active_people,
            'deleted_people': deleted_people,
            'with_biometric': with_biometric,
            'without_biometric': without_biometric,
            'search_query': search_query,
            'filter_type': filter_type,
        }
    except Exception as e:
        context = {
            'nickname': nickname,
            'user_email': user_email,
            'people': [],
            'total_people': 0,
            'active_people': 0,
            'deleted_people': 0,
            'with_biometric': 0,
            'without_biometric': 0,
            'search_query': '',
            'filter_type': '',
            'error': str(e)
        }
    
    return render(request, 'aplicacion_llaves/llaves/vistas/add_personnel.html', context)

@csrf_exempt
@require_POST
@transaction.atomic
def edit_person_ajax(request):
    """Maneja las solicitudes AJAX para editar personal (sin pisar la huella si no se envía)."""
    if not request.session.get('is_authenticated'):
        return JsonResponse({'success': False, 'message': 'No autorizado'})

    try:
        person_id = request.POST.get('person_id')
        nombres = (request.POST.get('nombres') or '').strip()
        apellidos = (request.POST.get('apellidos') or '').strip()
        correo = (request.POST.get('correo') or '').strip()
        tipo_documento = request.POST.get('tipo_documento') or ''
        numero_documento = (request.POST.get('numero_documento') or '').strip()

        # Validaciones
        if not (person_id and nombres and apellidos and tipo_documento and numero_documento):
            return JsonResponse({'success': False, 'message': 'Todos los campos obligatorios deben estar completos'})

        from .models import People
        try:
            persona = People.objects.select_for_update().get(id=person_id)
        except People.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Persona no encontrada'})

        # Duplicado de documento (excluyendo el propio)
        if People.objects.filter(document_number=numero_documento).exclude(id=person_id).exists():
            return JsonResponse({'success': False, 'message': f'Ya existe otra persona registrada con el número de documento {numero_documento}'})

        # ---------- HUELLAS ----------
        update_bio = False
        biometric_blob = None

        # Preferido: template_json (lista[int] del sensor)
        template_json_str = request.POST.get('template_json') or ''
        if template_json_str:
            try:
                tpl = json.loads(template_json_str)
                if not (isinstance(tpl, list) and all(isinstance(x, int) for x in tpl)):
                    return JsonResponse({'success': False, 'message': 'template_json inválido (se espera lista de enteros)'})
                # Si el campo es BinaryField/LongBlob guarda como bytes UTF-8:
                biometric_blob = json.dumps(tpl).encode('utf-8')
                # Si tu campo fuera TextField/JSONField, usa en su lugar:
                # biometric_blob = json.dumps(tpl)
                update_bio = True
            except Exception:
                return JsonResponse({'success': False, 'message': 'template_json no es JSON válido'})

        # Compatibilidad: huella_b64 (bytes crudos)
        elif request.POST.get('huella_b64'):
            huella_b64 = request.POST.get('huella_b64') or ''
            if ',' in huella_b64 and 'base64' in huella_b64[:50]:
                huella_b64 = huella_b64.split(',', 1)[1]
            try:
                biometric_blob = base64.b64decode(huella_b64.encode('ascii'))
                update_bio = True
            except Exception:
                return JsonResponse({'success': False, 'message': 'huella_b64 inválida'})

        # Si no llegó nada, NO tocamos la huella existente
        # -----------------------------------------------

        # Actualizar datos básicos
        persona.document_type = tipo_documento
        persona.document_number = numero_documento
        persona.first_name = nombres.upper()
        persona.first_last_name = apellidos.upper()
        persona.personal_email = correo or None

        # Actualizar huella solo si llegó nueva
        if update_bio:
            persona.biometric_code = biometric_blob

        persona.save()

        return JsonResponse({
            'success': True,
            'message': f'Personal actualizado exitosamente. ID: {persona.id}',
            'fingerprint_updated': update_bio
        })

    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error al actualizar personal: {e}'})

@csrf_exempt
def delete_person_ajax(request):

    """Maneja las solicitudes AJAX para eliminar personal"""
    if not request.session.get('is_authenticated'):
        return JsonResponse({'success': False, 'message': 'No autorizado'})
    
    if request.method == 'POST':
        try:
            person_id = request.POST.get('person_id')
            
            if not person_id:
                return JsonResponse({
                    'success': False, 
                    'message': 'ID de persona requerido'
                })
            
            # Buscar la persona
            try:
                persona = People.objects.get(id=person_id)
            except People.DoesNotExist:
                return JsonResponse({
                    'success': False, 
                    'message': 'Persona no encontrada'
                })
            
            # Eliminar persona permanentemente
            persona.delete()
            
            return JsonResponse({
                'success': True, 
                'message': f'Personal eliminado exitosamente. ID: {persona.id}'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'message': f'Error al eliminar personal: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})
@csrf_exempt
def get_person_ajax(request):
    if not request.session.get('is_authenticated'):
        return JsonResponse({'success': False, 'message': 'No autorizado'})

    if request.method == 'GET':
        try:
            person_id = request.GET.get('person_id')
            if not person_id:
                return JsonResponse({'success': False, 'message': 'ID de persona requerido'})

            from .models import People
            try:
                persona = People.objects.get(id=person_id)
            except People.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Persona no encontrada'})

            bio_raw = persona.biometric_code
            if bio_raw is not None:
                if isinstance(bio_raw, memoryview):
                    bio_raw = bio_raw.tobytes()
                if isinstance(bio_raw, (bytes, bytearray)):
                    datos_huella = b64encode(bio_raw).decode('ascii')
                elif isinstance(bio_raw, str):
                    datos_huella = bio_raw
                else:
                    datos_huella = ''
            else:
                datos_huella = ''

            return JsonResponse({
                'success': True,
                'data': {
                    'id': persona.id,
                    'nombres': persona.first_name,
                    'apellidos': persona.first_last_name,
                    'correo': persona.personal_email or '',
                    'tipo_documento': persona.document_type,
                    'numero_documento': persona.document_number,
                    'datos_huella': datos_huella
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al obtener datos: {e}'})

    return JsonResponse({'success': False, 'message': 'Método no permitido'})
# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from datetime import datetime
import json, base64, time

from .models import People


# ===================== 1) Crear personal =====================
@csrf_exempt
@require_POST
def add_personnel_ajax(request):
    if not request.session.get('is_authenticated'):
        return JsonResponse({'ok': False, 'error': 'No autorizado'}, status=401)

    try:
        nombres = (request.POST.get('nombres') or '').strip()
        apellidos = (request.POST.get('apellidos') or '').strip()
        correo = (request.POST.get('correo') or '').strip()
        tipo_documento = request.POST.get('tipo_documento') or ''
        numero_documento = (request.POST.get('numero_documento') or '').strip()
        telefono = (request.POST.get('telefono') or '').strip()
        genero = request.POST.get('genero') or None
        direccion = (request.POST.get('direccion') or '').strip()
        eps_id = int(request.POST.get('eps_id') or 1)
        population_group_id = int(request.POST.get('population_group_id') or 1)

        # opcional
        fecha_nacimiento = request.POST.get('fecha_nacimiento') or None
        date_of_birth = None
        if fecha_nacimiento:
            try:
                date_of_birth = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
            except Exception:
                pass

        if not (nombres and apellidos and tipo_documento and numero_documento):
            return JsonResponse({'ok': False, 'error': 'Todos los campos obligatorios deben estar completos'})

        if People.objects.filter(document_number=numero_documento).exists():
            return JsonResponse({'ok': False, 'error': f'Ya existe una persona con documento {numero_documento}'})

        # ---------- HUELLAS (preferir template_json, compat huella_b64) ----------
        biometric_blob = None  # lo que guardaremos en biometric_code

        template_json_str = request.POST.get('template_json') or ''
        if template_json_str:
            try:
                tpl = json.loads(template_json_str)
                if not (isinstance(tpl, list) and all(isinstance(x, int) for x in tpl)):
                    return JsonResponse({'ok': False, 'error': 'template_json inválido (se espera lista de enteros)'}, status=400)
                # Si biometric_code es BinaryField/LongBlob:
                biometric_blob = json.dumps(tpl).encode('utf-8')
                # Si fuera TextField/JSONField, usar:
                # biometric_blob = json.dumps(tpl)
            except Exception:
                return JsonResponse({'ok': False, 'error': 'template_json no es JSON válido'}, status=400)
        else:
            # Compatibilidad: base64 (bytes crudos). NO recomendado para verificar.
            huella_b64 = request.POST.get('huella_b64') or ''
            if huella_b64:
                if ',' in huella_b64 and 'base64' in huella_b64[:50]:
                    huella_b64 = huella_b64.split(',', 1)[1]
                try:
                    biometric_blob = base64.b64decode(huella_b64.encode('ascii'))
                except Exception:
                    return JsonResponse({'ok': False, 'error': 'huella_b64 inválida'}, status=400)
        # -------------------------------------------------------------------------

        nueva_persona = People.objects.create(
            document_type=tipo_documento,
            document_number=numero_documento,
            first_name=nombres.upper(),
            first_last_name=apellidos.upper(),
            personal_email=correo or None,
            telephone1=telefono or None,
            date_of_birth=date_of_birth,
            gender=genero or None,
            address=direccion or None,
            biometric_code=biometric_blob,  # JSON bytes (o str si TextField)
            eps_id=eps_id,
            population_group_id=population_group_id,
            pension_entity_id=1,
        )

        return JsonResponse({'ok': True, 'id': nueva_persona.id, 'message': 'Personal agregado exitosamente'})

    except Exception as e:
        return JsonResponse({'ok': False, 'error': f'Error al agregar personal: {e}'}, status=400)



# ===================== 2) Capturar huella =====================
@csrf_exempt
@require_POST
def capture_fingerprint_ajax(request):
    """
    Captura la huella y devuelve:
      - template_json: lista[int] (como JSON) -> usar para GUARDAR/VERIFICAR
      - huella_b64: string base64 (opcional, solo UI)
    """
    try:
        from pyfingerprint.pyfingerprint import PyFingerprint, FINGERPRINT_CHARBUFFER1

        PORT = 'COM7'
        BAUD = 57600

        sensor = PyFingerprint(PORT, BAUD, 0xFFFFFFFF, 0x00000000)
        if not sensor.verifyPassword():
            return JsonResponse({'ok': False, 'error': 'Contraseña del sensor incorrecta'}, status=400)

        timeout = time.time() + 10
        while not sensor.readImage():
            if time.time() > timeout:
                return JsonResponse({'ok': False, 'error': 'Tiempo agotado esperando la huella'}, status=408)
            time.sleep(0.1)

        sensor.convertImage(FINGERPRINT_CHARBUFFER1)

        # Plantilla correcta para guardar/verificar:
        template_list = sensor.downloadCharacteristics(FINGERPRINT_CHARBUFFER1)  # list[int]

        # Base64 solo como preview/compat
        b64_preview = base64.b64encode(bytes(template_list)).decode("ascii")

        return JsonResponse({
            'ok': True,
            'template_json': template_list,
            'huella_b64': b64_preview
        })

    except Exception as e:
        return JsonResponse({'ok': False, 'error': f'Error de captura: {e}'}, status=500)



# ===================== 3) Verificar huella =====================
@csrf_exempt
@require_POST
def verify_fingerprint_ajax(request):
    """
    Verifica la huella capturada con la registrada (usa comparación del sensor).
    """
    try:
        person_id = request.POST.get('person_id')
        if not person_id:
            return JsonResponse({'ok': False, 'error': 'ID de persona requerido'}, status=400)

        try:
            persona = People.objects.get(id=person_id)
        except People.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'Persona no encontrada'}, status=404)

        if not persona.biometric_code:
            return JsonResponse({'ok': False, 'error': 'La persona no tiene huella registrada'}, status=400)

        from pyfingerprint.pyfingerprint import (
            PyFingerprint,
            FINGERPRINT_CHARBUFFER1,
            FINGERPRINT_CHARBUFFER2
        )

        PORT = 'COM7'
        BAUD = 57600

        sensor = PyFingerprint(PORT, BAUD, 0xFFFFFFFF, 0x00000000)
        if not sensor.verifyPassword():
            return JsonResponse({'ok': False, 'error': 'Contraseña del sensor incorrecta'}, status=400)

        # Capturar huella actual
        timeout = time.time() + 10
        while not sensor.readImage():
            if time.time() > timeout:
                return JsonResponse({'ok': False, 'error': 'Tiempo agotado esperando la huella'}, status=408)
            time.sleep(0.1)

        sensor.convertImage(FINGERPRINT_CHARBUFFER1)

        # --- Cargar plantilla guardada (JSON) en buffer 2 ---
        raw = persona.biometric_code
        # Si viene como bytes (BinaryField/LongBlob) -> decodificar a str
        if isinstance(raw, (bytes, bytearray, memoryview)):
            raw = bytes(raw).decode('utf-8')

        try:
            stored_list = json.loads(raw)  # list[int]
            if not (isinstance(stored_list, list) and all(isinstance(x, int) for x in stored_list)):
                return JsonResponse({'ok': False, 'error': 'Plantilla almacenada inválida'}, status=500)
        except Exception:
            return JsonResponse({'ok': False, 'error': 'No se pudo leer la plantilla almacenada'}, status=500)

        sensor.uploadCharacteristics(FINGERPRINT_CHARBUFFER2, stored_list)

        # Comparar en el sensor (más robusto que bytes==bytes)
        score = sensor.compareCharacteristics()

        if score > 0:
            return JsonResponse({'ok': True, 'match': True, 'score': score, 'message': 'Huella verificada correctamente'})
        else:
            return JsonResponse({'ok': True, 'match': False, 'score': score, 'message': 'La huella no coincide'})

    except Exception as e:
        return JsonResponse({'ok': False, 'error': f'Error verificando huella: {e}'}, status=500)
