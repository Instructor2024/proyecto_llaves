#!/usr/bin/env python
import os
import sys
import subprocess
import time

def check_django_setup():
    """Verifica que Django esté configurado correctamente"""
    print("🔍 Verificando configuración de Django...")
    
    try:
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto_llaves.settings')
        django.setup()
        
        from aplicacion_llaves.models import People
        count = People.objects.count()
        print(f"✅ Django configurado correctamente")
        print(f"✅ Base de datos conectada - {count} registros en tabla people")
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración de Django: {e}")
        return False

def start_server():
    """Inicia el servidor Django"""
    print("\n🚀 Iniciando servidor Django...")
    print("=" * 50)
    
    try:
        # Verificar que estamos en el directorio correcto
        if not os.path.exists('manage.py'):
            print("❌ Error: No se encontró manage.py. Asegúrate de estar en el directorio correcto.")
            return False
        
        # Iniciar el servidor
        print("📡 Servidor iniciándose en http://127.0.0.1:8000/")
        print("⏳ Esperando que el servidor esté listo...")
        
        # Iniciar el servidor en segundo plano
        process = subprocess.Popen([
            sys.executable, 'manage.py', 'runserver'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Esperar un momento para que el servidor se inicie
        time.sleep(3)
        
        if process.poll() is None:
            print("✅ Servidor iniciado correctamente!")
            print("\n" + "=" * 50)
            print("🎉 ¡SERVIDOR FUNCIONANDO!")
            print("=" * 50)
            print("\n📋 INSTRUCCIONES PARA ACCEDER:")
            print("1. Abre tu navegador web")
            print("2. Ve a: http://127.0.0.1:8000/vistas/")
            print("3. Inicia sesión con tus credenciales")
            print("4. En la pestaña 'Agregar Instru/Aseo/Vigilante'")
            print("5. Haz clic en '👥 Ver y Agregar Personal'")
            print("\n🔧 FUNCIONALIDADES DISPONIBLES:")
            print("✅ Ver 146,515 registros de personal existente")
            print("✅ Buscar y filtrar personal")
            print("✅ Agregar nuevo personal a la base de datos")
            print("✅ Estadísticas en tiempo real")
            print("✅ Registro de huellas digitales")
            print("\n⚠️  Para detener el servidor, presiona Ctrl+C")
            
            try:
                # Mantener el servidor corriendo
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Deteniendo servidor...")
                process.terminate()
                print("✅ Servidor detenido")
            
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Error al iniciar servidor:")
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando aplicación de gestión de personal...")
    print("=" * 60)
    
    if check_django_setup():
        start_server()
    else:
        print("❌ No se pudo iniciar la aplicación")
        sys.exit(1)

