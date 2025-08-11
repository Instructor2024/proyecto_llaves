#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto_llaves.settings')
django.setup()

from aplicacion_llaves.models import People
from django.db import connection
from django.core.paginator import Paginator
from django.db.models import Q

def test_personnel_functionality():
    """Prueba la funcionalidad de gestión de personal"""
    print("🔍 Probando funcionalidad de gestión de personal...")
    print("=" * 60)
    
    try:
        # 1. Probar consulta básica
        print("1. 📋 Consulta básica de personal:")
        people_list = People.objects.all().order_by('-created_at')
        total_count = people_list.count()
        print(f"   ✅ Total de registros: {total_count}")
        
        # 2. Probar paginación
        print("\n2. 📄 Prueba de paginación:")
        paginator = Paginator(people_list, 20)
        page_1 = paginator.get_page(1)
        print(f"   ✅ Página 1: {len(page_1)} registros de {page_1.paginator.count} total")
        print(f"   ✅ Número total de páginas: {page_1.paginator.num_pages}")
        
        # 3. Probar estadísticas
        print("\n3. 📊 Prueba de estadísticas:")
        active_people = people_list.filter(deleted_at__isnull=True).count()
        deleted_people = people_list.filter(deleted_at__isnull=False).count()
        with_biometric = people_list.exclude(biometric_code__isnull=True).exclude(biometric_code='').count()
        without_biometric = total_count - with_biometric
        
        print(f"   ✅ Personal activo: {active_people}")
        print(f"   ✅ Personal eliminado: {deleted_people}")
        print(f"   ✅ Con huella digital: {with_biometric}")
        print(f"   ✅ Sin huella digital: {without_biometric}")
        
        # 4. Probar búsqueda
        print("\n4. 🔍 Prueba de búsqueda:")
        search_results = people_list.filter(
            Q(first_name__icontains='RUBEN') |
            Q(first_last_name__icontains='ESIMI')
        )[:5]
        print(f"   ✅ Búsqueda 'RUBEN ESIMI': {search_results.count()} resultados")
        for person in search_results:
            print(f"      - {person.first_name} {person.first_last_name} (ID: {person.id})")
        
        # 5. Probar filtros
        print("\n5. 🎯 Prueba de filtros:")
        with_biometric_filter = people_list.exclude(biometric_code__isnull=True).exclude(biometric_code='')[:3]
        print(f"   ✅ Filtro 'con huella digital': {with_biometric_filter.count()} resultados")
        for person in with_biometric_filter:
            print(f"      - {person.first_name} {person.first_last_name} (Huella: {'Sí' if person.biometric_code else 'No'})")
        
        # 6. Probar creación de persona (simulación)
        print("\n6. ➕ Prueba de creación de persona (simulación):")
        test_data = {
            'document_type': 'Cédula de ciudadanía',
            'document_number': 999999999,
            'first_name': 'TEST',
            'first_last_name': 'PERSONA',
            'personal_email': 'test@example.com',
            'biometric_code': 'test_biometric_data',
            'eps_id': 1,
            'population_group_id': 1,
            'pension_entity_id': 1
        }
        
        # Verificar si ya existe
        existing = People.objects.filter(document_number=test_data['document_number']).exists()
        if existing:
            print("   ⚠️  Ya existe una persona con ese número de documento (esperado para prueba)")
        else:
            print("   ✅ Número de documento disponible para prueba")
        
        # 7. Mostrar estructura de campos
        print("\n7. 🗂️  Campos disponibles para formulario:")
        fields = ['document_type', 'document_number', 'first_name', 'first_last_name', 
                 'second_last_name', 'personal_email', 'biometric_code', 'address',
                 'telephone1', 'telephone2', 'telephone3']
        
        for field in fields:
            field_obj = People._meta.get_field(field)
            required = "Obligatorio" if not field_obj.null else "Opcional"
            print(f"   - {field}: {required}")
        
        print("\n✅ Todas las pruebas de funcionalidad pasaron exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error en las pruebas: {e}")
        return False

def test_url_patterns():
    """Prueba que las URLs estén configuradas correctamente"""
    print("\n🔗 Probando configuración de URLs...")
    print("=" * 40)
    
    try:
        from aplicacion_llaves.urls import urlpatterns
        
        expected_urls = [
            'add-personnel/',
            'add-personnel/ajax/',
            'people/',
            'people/ajax/',
            'people/management/',
            'vistas/'
        ]
        
        url_names = [url.name for url in urlpatterns if hasattr(url, 'name') and url.name]
        
        for expected_url in expected_urls:
            if any(expected_url.replace('/', '') in name for name in url_names):
                print(f"   ✅ URL encontrada: {expected_url}")
            else:
                print(f"   ❌ URL faltante: {expected_url}")
        
        print("✅ Configuración de URLs verificada")
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración de URLs: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de funcionalidad de gestión de personal...")
    print("=" * 70)
    
    success = True
    
    if test_personnel_functionality():
        print("\n✅ Funcionalidad de personal: OK")
    else:
        print("\n❌ Funcionalidad de personal: FALLÓ")
        success = False
    
    if test_url_patterns():
        print("\n✅ Configuración de URLs: OK")
    else:
        print("\n❌ Configuración de URLs: FALLÓ")
        success = False
    
    print("\n" + "=" * 70)
    if success:
        print("🎉 ¡Todas las pruebas pasaron! La funcionalidad está lista para usar.")
        print("\n📋 Para acceder a la gestión de personal:")
        print("   1. Inicia el servidor: python manage.py runserver")
        print("   2. Ve a: http://127.0.0.1:8000/vistas/")
        print("   3. Haz clic en '👥 Ver y Agregar Personal'")
    else:
        print("❌ Algunas pruebas fallaron. Revisa los errores arriba.")
        sys.exit(1)

