#!/usr/bin/env python
"""
Script final de verificación para confirmar que todo funciona correctamente
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto_llaves.settings')
django.setup()

from django.urls import reverse, NoReverseMatch
from django.test import Client
from aplicacion_llaves.models import People

def verificar_rutas():
    """Verificar que todas las rutas estén disponibles"""
    print("=== VERIFICACIÓN DE RUTAS ===")
    
    rutas_importantes = [
        'add_personnel',
        'add_personnel_ajax',
        'people_ajax',
        'people_management',
        'vistas_index',
        'login',
        'dashboard'
    ]
    
    todas_ok = True
    for ruta in rutas_importantes:
        try:
            url = reverse(ruta)
            print(f"✓ {ruta}: {url}")
        except NoReverseMatch as e:
            print(f"✗ {ruta}: ERROR - {e}")
            todas_ok = False
    
    return todas_ok

def verificar_vistas():
    """Verificar que todas las vistas existan"""
    print("\n=== VERIFICACIÓN DE VISTAS ===")
    
    from aplicacion_llaves import views
    
    vistas_importantes = [
        'add_personnel_view',
        'add_personnel_ajax',
        'people_ajax_view',
        'people_management_view',
        'vistas_index_view',
        'login_admin',
        'dashboard_view'
    ]
    
    todas_ok = True
    for vista in vistas_importantes:
        if hasattr(views, vista):
            print(f"✓ {vista}: Existe")
        else:
            print(f"✗ {vista}: NO EXISTE")
            todas_ok = False
    
    return todas_ok

def verificar_base_datos():
    """Verificar conexión a la base de datos"""
    print("\n=== VERIFICACIÓN DE BASE DE DATOS ===")
    
    try:
        # Intentar conectar a la base de datos
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✓ Conexión a base de datos: OK")
        
        # Verificar tabla people
        count = People.objects.count()
        print(f"✓ Tabla 'people': {count} registros encontrados")
        
        return True
    except Exception as e:
        print(f"✗ Error en base de datos: {e}")
        return False

def verificar_archivos_importantes():
    """Verificar que los archivos importantes existan"""
    print("\n=== VERIFICACIÓN DE ARCHIVOS ===")
    
    archivos_importantes = [
        'aplicacion_llaves/urls.py',
        'aplicacion_llaves/views.py',
        'aplicacion_llaves/models.py',
        'aplicacion_llaves/templates/aplicacion_llaves/llaves/vistas/add_personnel.html',
        'aplicacion_llaves/templates/aplicacion_llaves/llaves/vistas/Index.html',
        'aplicacion_llaves/static/css/personnel.css',
        'proyecto_llaves/urls.py',
        'proyecto_llaves/settings.py'
    ]
    
    todas_ok = True
    for archivo in archivos_importantes:
        if os.path.exists(archivo):
            print(f"✓ {archivo}: Existe")
        else:
            print(f"✗ {archivo}: NO EXISTE")
            todas_ok = False
    
    return todas_ok

def verificar_configuracion():
    """Verificar configuración de Django"""
    print("\n=== VERIFICACIÓN DE CONFIGURACIÓN ===")
    
    from django.conf import settings
    
    configuraciones_ok = True
    
    # Verificar DEBUG
    if settings.DEBUG:
        print("✓ DEBUG: Activado (correcto para desarrollo)")
    else:
        print("⚠ DEBUG: Desactivado (puede causar problemas en desarrollo)")
    
    # Verificar ALLOWED_HOSTS
    if '*' in settings.ALLOWED_HOSTS or 'localhost' in settings.ALLOWED_HOSTS:
        print("✓ ALLOWED_HOSTS: Configurado correctamente")
    else:
        print("✗ ALLOWED_HOSTS: No configurado correctamente")
        configuraciones_ok = False
    
    # Verificar INSTALLED_APPS
    if 'aplicacion_llaves' in settings.INSTALLED_APPS:
        print("✓ aplicacion_llaves: En INSTALLED_APPS")
    else:
        print("✗ aplicacion_llaves: NO está en INSTALLED_APPS")
        configuraciones_ok = False
    
    return configuraciones_ok

def main():
    """Función principal de verificación"""
    print("🔍 INICIANDO VERIFICACIÓN FINAL DEL SISTEMA")
    print("=" * 50)
    
    resultados = []
    
    resultados.append(("Rutas", verificar_rutas()))
    resultados.append(("Vistas", verificar_vistas()))
    resultados.append(("Base de Datos", verificar_base_datos()))
    resultados.append(("Archivos", verificar_archivos_importantes()))
    resultados.append(("Configuración", verificar_configuracion()))
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 50)
    
    todas_ok = True
    for componente, resultado in resultados:
        if resultado:
            print(f"✅ {componente}: OK")
        else:
            print(f"❌ {componente}: PROBLEMAS DETECTADOS")
            todas_ok = False
    
    print("\n" + "=" * 50)
    if todas_ok:
        print("🎉 ¡TODAS LAS VERIFICACIONES PASARON EXITOSAMENTE!")
        print("\n📋 INSTRUCCIONES PARA USAR LA APLICACIÓN:")
        print("1. El servidor ya está ejecutándose en http://127.0.0.1:8000/")
        print("2. Ve a http://127.0.0.1:8000/vistas/")
        print("3. Haz clic en '👥 Ver y Agregar Personal'")
        print("4. ¡Disfruta de todas las funcionalidades mejoradas!")
    else:
        print("⚠️  SE DETECTARON PROBLEMAS QUE NECESITAN ATENCIÓN")
        print("Revisa los errores arriba y corrígelos antes de usar la aplicación.")
    
    print("\n" + "=" * 50)

if __name__ == '__main__':
    main()






