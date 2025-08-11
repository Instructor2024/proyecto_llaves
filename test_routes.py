#!/usr/bin/env python
"""
Script para probar las rutas de Django y identificar problemas
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto_llaves.settings')
django.setup()

from django.urls import reverse, NoReverseMatch
from django.test import Client
from django.urls import get_resolver

def test_url_patterns():
    """Probar todos los patrones de URL definidos"""
    print("=== PRUEBA DE PATRONES DE URL ===")
    
    # Obtener el resolver de URLs
    resolver = get_resolver()
    
    # Listar todas las URLs registradas
    print("\nURLs registradas en el sistema:")
    for pattern in resolver.url_patterns:
        if hasattr(pattern, 'url_patterns'):
            # Es un include
            print(f"  Include: {pattern.pattern}")
            for sub_pattern in pattern.url_patterns:
                callback_name = 'N/A'
                if hasattr(sub_pattern, 'callback') and sub_pattern.callback is not None:
                    callback_name = sub_pattern.callback.__name__
                print(f"    - {sub_pattern.pattern} -> {callback_name}")
        else:
            # Es una URL directa
            callback_name = 'N/A'
            if hasattr(pattern, 'callback') and pattern.callback is not None:
                callback_name = pattern.callback.__name__
            print(f"  Direct: {pattern.pattern} -> {callback_name}")

def test_specific_urls():
    """Probar URLs específicas"""
    print("\n=== PRUEBA DE URLs ESPECÍFICAS ===")
    
    urls_to_test = [
        'add_personnel',
        'add_personnel_ajax', 
        'people_ajax',
        'people_management',
        'vistas_index',
        'login',
        'dashboard'
    ]
    
    for url_name in urls_to_test:
        try:
            url = reverse(url_name)
            print(f"✓ {url_name}: {url}")
        except NoReverseMatch as e:
            print(f"✗ {url_name}: ERROR - {e}")

def test_client_requests():
    """Probar requests HTTP reales"""
    print("\n=== PRUEBA DE REQUESTS HTTP ===")
    
    client = Client()
    
    # URLs a probar
    test_urls = [
        '/add-personnel/',
        '/add-personnel/ajax/',
        '/people/ajax/',
        '/people/management/',
        '/vistas/',
        '/login/',
        '/dashboard/'
    ]
    
    for url in test_urls:
        try:
            response = client.get(url)
            print(f"✓ {url}: {response.status_code}")
        except Exception as e:
            print(f"✗ {url}: ERROR - {e}")

def test_views_existence():
    """Verificar que las vistas existen"""
    print("\n=== PRUEBA DE EXISTENCIA DE VISTAS ===")
    
    from aplicacion_llaves import views
    
    views_to_test = [
        'add_personnel_view',
        'add_personnel_ajax',
        'people_ajax_view', 
        'people_management_view',
        'vistas_index_view',
        'login_admin',
        'dashboard_view'
    ]
    
    for view_name in views_to_test:
        if hasattr(views, view_name):
            print(f"✓ {view_name}: Existe")
        else:
            print(f"✗ {view_name}: NO EXISTE")

if __name__ == '__main__':
    print("Iniciando pruebas de rutas...")
    
    try:
        test_views_existence()
        test_url_patterns()
        test_specific_urls()
        test_client_requests()
        
        print("\n=== RESUMEN ===")
        print("Si ves errores arriba, esos son los problemas específicos.")
        print("Si todo está bien, las rutas deberían funcionar correctamente.")
        
    except Exception as e:
        print(f"Error general: {e}")
        import traceback
        traceback.print_exc()
