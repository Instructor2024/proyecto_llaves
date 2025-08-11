import serial
import serial.tools.list_ports
import time

def test_as608_connection():
    print("=== PRUEBA DE CONEXIÓN AS608 ===")
    print()
    
    # Listar puertos disponibles
    ports = serial.tools.list_ports.comports()
    print(f"Puertos detectados: {len(ports)}")
    
    for port in ports:
        print(f"- {port.device}: {port.description}")
    print()
    
    # Buscar puerto del AS608
    as608_port = None
    for port in ports:
        if any(keyword in port.description.upper() for keyword in ['USB', 'TTL', 'CH340', 'CP210']):
            as608_port = port.device
            print(f"✅ Puerto AS608 detectado: {port.device}")
            break
    
    if not as608_port:
        print("❌ No se detectó el lector AS608")
        print("🔧 Soluciones:")
        print("1. Conecta el lector por USB")
        print("2. Instala drivers USB-TTL")
        print("3. Verifica en Administrador de dispositivos")
        return False
    
    # Probar conexión
    try:
        print(f"🔌 Probando conexión en {as608_port}...")
        ser = serial.Serial(as608_port, 57600, timeout=5)
        time.sleep(2)
        
        # Comando de prueba
        ser.write(b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x01\x00\x05')
        response = ser.read(12)
        
        if len(response) >= 12:
            print("✅ Conexión exitosa con AS608")
            ser.close()
            return True
        else:
            print("❌ No se recibió respuesta del lector")
            ser.close()
            return False
            
    except serial.SerialException as e:
        print(f"❌ Error de conexión: {e}")
        return False
    except Exception as e:
        print(f"❌ Error general: {e}")
        return False

if __name__ == "__main__":
    test_as608_connection()
