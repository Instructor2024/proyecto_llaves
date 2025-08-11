import serial.tools.list_ports
import sys

print("=== VERIFICACIÓN DE PUERTOS SERIALES ===")
print()

# Listar todos los puertos disponibles
ports = serial.tools.list_ports.comports()

if not ports:
    print("❌ No se detectaron puertos seriales")
    print()
    print("🔧 SOLUCIONES:")
    print("1. Conecta el lector AS608 por USB")
    print("2. Instala los drivers USB-TTL si es necesario")
    print("3. Verifica en Administrador de dispositivos")
    print("4. Reinicia el dispositivo")
else:
    print(f"✅ Se detectaron {len(ports)} puerto(s):")
    print()
    
    for i, port in enumerate(ports, 1):
        print(f"Puerto {i}:")
        print(f"  - Dispositivo: {port.device}")
        print(f"  - Descripción: {port.description}")
        print(f"  - Hardware ID: {port.hwid}")
        print(f"  - VID:PID: {port.vid}:{port.pid}")
        print()

print("=== INFORMACIÓN ADICIONAL ===")
print("El lector AS608 típicamente aparece como:")
print("- 'USB Serial Device'")
print("- 'CH340' o 'CH341'")
print("- 'CP210x'")
print("- 'FTDI'")
print()
print("Si no aparece, prueba:")
print("1. Cambiar cable USB")
print("2. Cambiar puerto USB")
print("3. Instalar drivers específicos")
