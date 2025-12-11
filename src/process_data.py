import boto3
import json
from datetime import datetime
from decimal import Decimal
from src.db.db_config import get_db_conexion
 
dynamodb = boto3.resource('dynamodb')
tabla = dynamodb.Table('tabla-granja')
 
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
        conn= get_db_conexion()
        cursor = conn.cursor()
        
        query = f"""
        INSERT INTO {nombre_tabla}(device_id, timestamp, temperature, humidity, light, nh3, no2, co, co2)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (device_id, timestamp) DO NOTHING;
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

 
def lambda_handler(event, context):
    
    print("🔍 Obtieniendo datos de DynamoDB...")
    items = []
    response = tabla.scan()

    items.extend(response.get('Items', []))
    while 'LastEvaluatedKey' in response:
      response = tabla.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
      items.extend(response.get('Items', []))

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
          print("Este es device uno sin ventilador")
          insertar_en_tabla("granja_device1", datos)

      elif device_id == "Sin_device2":
          print("Este es device dos sin ventilador")
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
    