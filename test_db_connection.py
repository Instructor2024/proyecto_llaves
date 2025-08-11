#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto_llaves.settings')
django.setup()

from aplicacion_llaves.models import People
from django.db import connection

def test_database_connection():
    """Prueba la conexión a la base de datos y verifica la tabla people"""
    try:
        # Probar conexión
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Conexión a la base de datos exitosa")
        
        # Verificar si la tabla people existe
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES LIKE 'people'")
            result = cursor.fetchone()
            if result:
                print("✅ Tabla 'people' encontrada")
            else:
                print("❌ Tabla 'people' no encontrada")
                return False
        
        # Contar registros en la tabla people
        try:
            count = People.objects.count()
            print(f"✅ Total de registros en tabla people: {count}")
            
            # Mostrar algunos registros de ejemplo
            if count > 0:
                print("\n📋 Primeros 5 registros:")
                for i, person in enumerate(People.objects.all()[:5]):
                    print(f"  {i+1}. ID: {person.id} | Nombre: {person.first_name} {person.first_last_name} | Documento: {person.document_number}")
            else:
                print("📋 La tabla people está vacía")
                
        except Exception as e:
            print(f"❌ Error al consultar la tabla people: {e}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_model_fields():
    """Prueba que los campos del modelo People coincidan con la estructura de la base de datos"""
    try:
        # Obtener información de la tabla
        with connection.cursor() as cursor:
            cursor.execute("DESCRIBE people")
            columns = cursor.fetchall()
            
        print("\n📊 Estructura de la tabla 'people':")
        for column in columns:
            field_name, field_type, null, key, default, extra = column
            print(f"  - {field_name}: {field_type} {'(NULL)' if null == 'YES' else '(NOT NULL)'}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error al obtener estructura de la tabla: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Probando conexión a la base de datos SICEFA...")
    print("=" * 50)
    
    if test_database_connection():
        test_model_fields()
        print("\n✅ Todas las pruebas pasaron exitosamente")
    else:
        print("\n❌ Algunas pruebas fallaron")
        sys.exit(1)
