import requests
import os
from dotenv import load_dotenv

# Configuración inicial
load_dotenv()
WEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")
# Regla de oro: Sacamos la llave de TheSportsDB de la URL y la llamamos desde el .env
TSDB_KEY = os.getenv("TSDB_API_KEY") 

def consultar_logistica_thesportsdb():
    equipo_user = input("Ingresa tu equipo (ej: Sacramento Kings, Arsenal): ").strip()

    # --- ① ZONA AZUL: Construcción de la solicitud ---
    # Inyectamos la variable de entorno en lugar del '123' hardcodeado
    tsdb_url = f"https://www.thesportsdb.com/api/v1/json/{TSDB_KEY}/searchteams.php"
    parametros = {"t": equipo_user}
    
    try:
        # --- ② ZONA VERDE: Llamada HTTP ---
        tsdb_resp = requests.get(tsdb_url, params=parametros, timeout=10) 

        # ERROR 1 (Clave Inválida): 401 Unauthorized o 403 Forbidden
        if tsdb_resp.status_code in [401, 403]:
            print("⚠️ Error de Seguridad (401/403): La API Key de TheSportsDB es inválida.")
            return

        if tsdb_resp.status_code != 200:
            print(f"⚠️ Error en el servidor de TheSportsDB: Código {tsdb_resp.status_code}")
            return

        tsdb_data = tsdb_resp.json()

        # --- ③ ZONA ROJA: Parseo y transformación del JSON ---
        # ERROR 2 (Lógico / 404): No se encontraron datos para ese equipo o devuelve nulo
        if not tsdb_data.get("teams"):
            print(f"❌ (404) No se encontró el equipo '{equipo_user}'. Verifica el nombre.")
            return

        equipo = tsdb_data["teams"][0]
        nombre_oficial = equipo["strTeam"]
        liga = equipo["strLeague"]
        estadio = equipo["strStadium"]
        ciudad = equipo["strLocation"] 

        # INTEGRACIÓN: Consultamos el clima de la ciudad
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={WEATHER_KEY}&units=metric&lang=es"
        weather_resp = requests.get(weather_url, timeout=10)
        
        if weather_resp.status_code == 200:
            w_data = weather_resp.json()
            temp = w_data['main']['temp']
            desc = w_data['weather'][0]['description']
            sugerencia = '¡Lleva abrigo al estadio!' if temp < 15 else 'Clima agradable para disfrutar el partido.'
        else:
            temp = "N/A"
            desc = "Datos no disponibles"
            sugerencia = "Revisa el pronóstico local por tu cuenta."

        # --- ④ ZONA MORADA: Formateo y salida al usuario ---
        print("\n" + "="*30)
        print(f"🏟️  LOGÍSTICA DE ESTADIO")
        print(f"Equipo  : {nombre_oficial} ({liga})")
        print(f"Estadio : {estadio}")
        print(f"Ciudad  : {ciudad}")
        print(f"Clima   : {temp}°C, {desc}")
        print("="*30)
        print(f"💡 Sugerencia: {sugerencia}\n")

    # ERROR 3 (Timeout): La petición excedió el límite de tiempo de 10 segundos
    except requests.exceptions.Timeout:
        print("⏱️ Error: La solicitud tardó demasiado (Timeout). Intenta de nuevo más tarde.")
        
    # ERROR 4 (Conexión): No hay internet, DNS fallido o servidor inalcanzable
    except requests.exceptions.ConnectionError:
        print("🔌 Error: Sin conexión a internet o el servidor no responde.")
        
    except Exception as e:
        print(f"🤯 Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    consultar_logistica_thesportsdb()