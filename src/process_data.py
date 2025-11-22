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
      response = tabla.scan()
      items = response.get("Items", [])
  
      resultados = []
  
      for item in items:
        ts_original = item.get("timestamp")
        ts_convertido = convertir_timestamp(ts_original)
        item["timestamp"] = ts_convertido if ts_convertido else "ERROR"
        item = decimal_a_nativo(item)

        device_id = item.get("device_id")
        timestamp = item.get("timestamp", "2025-01-01T00:00:00Z")
        temperature = item.get("temperature", 0)
        humidity = item.get("humidity", 0)
        light = item.get("light", 0)
        nh3 = item.get("NH3", 0)
        no2 = item.get("NO2", 0)
        co = item.get("CO", 0)
        co2 = item.get("CO2", 0)

        if device_id == "Sin_device1":
            try:
                print("Este es device uno sin ventilador")
                cursor = conn.cursor()
                query = """
                INSERT INTO granja_device1(device_id, timestamp, temperature, humidity, light, nh3, no2, co, co2)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (device_id, timestamp, temperature, humidity, light, nh3, no2, co, co2))
                conn.commit()
            except Exception as e:
                print(f"Error al procesar los datos: {e}")
                conn.rollback()

        elif device_id == "Sin_device2":
            try:
                print("Este es device dos sin ventilador")
                cursor = conn.cursor()
                query = """
                INSERT INTO granja_device2(device_id, timestamp, temperature, humidity, light, nh3, no2, co, co2)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (device_id, timestamp, temperature, humidity, light, nh3, no2, co, co2))
                conn.commit()
            except Exception as e:
                print(f"Error al procesar los datos: {e}")
                conn.rollback()

        elif device_id == "Con_device3":
            try:
                print("Este es device uno con ventilador")
                cursor = conn.cursor()
                query = """
                INSERT INTO granja_device3(device_id, timestamp, temperature, humidity, light, nh3, no2, co, co2)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (device_id, timestamp, temperature, humidity, light, nh3, no2, co, co2))
                conn.commit()
            except Exception as e:
                print(f"Error al procesar los datos: {e}")
                conn.rollback()
                
        elif device_id == "Con_device4":
            try:
                print("Este es device dos con ventilador")
                cursor = conn.cursor()
                query = """
                INSERT INTO granja_device4(device_id, timestamp, temperature, humidity, light, nh3, no2, co, co2)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (device_id, timestamp, temperature, humidity, light, nh3, no2, co, co2))
                conn.commit()
            except Exception as e:
                print(f"Error al procesar los datos: {e}")
                conn.rollback()

      return {
        "statusCode": 200,
        "body": "Todos los datos fueron procesados",
      }
    
    except Exception as e:
        print(f"Error en lambda_handler: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
