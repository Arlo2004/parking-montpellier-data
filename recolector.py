import requests
import csv
from datetime import datetime
import os

URL_API = "https://portail-api-data.montpellier3m.fr/offstreetparking?limit=1000"
CSV_FILE = "parkings_montpellier.csv"
file_exists =   os.path.exists(CSV_FILE)

try:
    response = requests.get(  URL_API, timeout=15  )
    if response.status_code== 200:
        data = response.json()
        fecha_lectura = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #corazon
        with open(CSV_FILE, mode="a",  newline="",  encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["fecha_lectura",  "nombre_parking", "plazas_libres", "capacidad_total",  "estado"])
            for parking in data:
                nombre = parking.get( "name", {} ).get("value", "Desconocido")
                plazas_libres = parking.get("availableSpotNumber", {}).get(  "value", 0  )
                estado = parking.get("status", {}).get("value", "Sin datos")
                capacidad =  parking.get("totalSpotNumber", {}).get("value",  "0"  )
                writer.writerow([fecha_lectura, nombre,  plazas_libres, capacidad, estado])
        print("Lectura exitosa")
    else:
        print("Error API")
except Exception as e:
    print(f"Error: {e}")
    exit(1)
