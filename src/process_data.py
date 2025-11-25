import boto3
import json
from datetime import datetime
from decimal import Decimal
from src.db.db_config import get_db_conexion
 
dynamodb = boto3.resource('dynamodb')
tabla = dynamodb.Table('iot_data_recursos')
conn= get_db_conexion()
 
def convertir_timestamp(timestamp_str):
    try:
        timestamp_int = int(timestamp_str)
        if len(str(timestamp_int)) > 10:
            timestamp_int = timestamp_int / 1000
        dt = datetime.utcfromtimestamp(timestamp_int)
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception as e:
        print(f"Error al convertir timestamp: {timestamp_str} - {e}")
        return None
 
def reconvertir_fecha_a_timestamp(fecha_legible):
    try:
        dt = datetime.strptime(fecha_legible, "%Y-%m-%dT%H:%M:%SZ")
        return int(dt.timestamp())
    except Exception as e:
        print(f"Error al reconvertir fecha: {fecha_legible} - {e}")
        return None
 
def decimal_a_nativo(obj):
    if isinstance(obj, list):
        return [decimal_a_nativo(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: decimal_a_nativo(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    else:
        return obj
    
def insertar_en_tabla(nombre_tabla, datos):
    try:
        cursor = conn.cursor()
        query = f"""
        INSERT INTO {nombre_tabla}(device_id, timestamp, temperature, humidity, light, nh3, no2, co, co2)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            datos["device_id"],
            datos["timestamp"],
            datos["temperature"],
            datos["humidity"],
            datos["light"],
            datos["nh3"],
            datos["no2"],
            datos["co"],
            datos["co2"]
        ))
        conn.commit()
        print(f"✅ Datos insertados en {nombre_tabla}")
    except Exception as e:
        print(f"❌ Error al insertar en {nombre_tabla}: {e}")
        conn.rollback()
# def insert_data_in_db(table_name):
#     try:
#         print("Este es device uno sin ventilador")
#         cursor = conn.cursor()
#         query = f"""
#         INSERT INTO {table_name}(device_id, timestamp, temperature, humidity, light, nh3, no2, co, co2)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """
#         cursor.execute(query, (device_id, timestamp, temperature, humidity, light, nh3, no2, co, co2))
#         conn.commit()
#     except Exception as e:
#         print(f"Error al procesar los datos: {e}")
#         conn.rollback()
 
def lambda_handler(event, context):
    try:
        device_id = event.get("device_id")
        timestamp = event.get("timestamp")
        temperature = event.get("temperature")
        humidity = event.get("humidity")
        light = event.get("light")
        nh3 = event.get("nh3")
        no2 = event.get("no2")
        co = event.get("co")
        co2 = event.get("co2")

        datos = {
            "device_id": device_id,
            "timestamp": timestamp,
            "temperature": temperature,
            "humidity": humidity,
            "light": light,
            "nh3": nh3,
            "no2": no2,
            "co": co,
            "co2": co2
        }

        if device_id == "Sin_device1":
            print("Este es device dos sin ventilador")
            insertar_en_tabla("granja_device1", datos)

        elif device_id == "Sin_device2":
            print("Este es device tres con ventilador")
            insertar_en_tabla("granja_device2", datos)

        elif device_id == "Con_device3":
            print("Este es device tres con ventilador")
            insertar_en_tabla("granja_device3", datos)

        elif device_id == "Con_device4":
            print("Este es device cuatro con ventilador")
            insertar_en_tabla("granja_device4", datos)

        return {
            "statusCode": 200,
            "body": "Todos los datos fueron insertados correctamente"
        }

    except Exception as e:
        print(f"Error en lambda_handler: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
    