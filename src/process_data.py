import boto3
import json
from datetime import datetime
from decimal import Decimal
from src.db.db_config import get_db_conexion

dynamodb = boto3.resource('dynamodb')
tabla = dynamodb.Table('iot_data_recursos')
conn = get_db_conexion()


# ------------------------------
# UTILIDADES
# ------------------------------

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


# ------------------------------
# DB HELPER GENÉRICO
# ------------------------------

def insertar_en_db(table_name, data):
    """
    Inserta un registro en la tabla SQL indicada.
    """
    try:
        cursor = conn.cursor()
        query = f"""
            INSERT INTO {table_name}
            (device_id, timestamp, temperature, humidity, light, nh3, no2, co, co2)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            data["device_id"],
            data["timestamp"],
            data["temperature"],
            data["humidity"],
            data["light"],
            data["nh3"],
            data["no2"],
            data["co"],
            data["co2"],
        ))

        conn.commit()

    except Exception as e:
        print(f"Error al insertar en {table_name}: {e}")
        conn.rollback()


# Mapa dinámico device_id → nombre tabla
DEVICE_TABLE_MAP = {
    "Sin_device1": "granja_device1",
    "Sin_device2": "granja_device2",
    "Con_device3": "granja_device3",
    "Con_device4": "granja_device4",
}


# ------------------------------
# LAMBDA HANDLER
# ------------------------------

def lambda_handler(event, context):
    try:
        response = tabla.scan()
        items = response.get("Items", [])

        for item in items:
            # Convertir timestamp y decimales
            ts_original = item.get("timestamp")
            item["timestamp"] = convertir_timestamp(ts_original) or "2025-01-01T00:00:00Z"
            item = decimal_a_nativo(item)

            # Preparar datos estandarizados
            data = {
                "device_id": item.get("device_id"),
                "timestamp": item.get("timestamp"),
                "temperature": item.get("temperature", 0),
                "humidity": item.get("humidity", 0),
                "light": item.get("light", 0),
                "nh3": item.get("NH3", 0),
                "no2": item.get("NO2", 0),
                "co": item.get("CO", 0),
                "co2": item.get("CO2", 0)
            }

            # Verificar si existe tabla mapeada
            tabla_destino = DEVICE_TABLE_MAP.get(data["device_id"])

            if tabla_destino:
                print(f"Insertando en tabla {tabla_destino} para device {data['device_id']}")
                insertar_en_db(tabla_destino, data)
            else:
                print(f"Device ID no reconocido: {data['device_id']}")

        return {
            "statusCode": 200,
            "body": "Todos los datos fueron procesados correctamente"
        }

    except Exception as e:
        print(f"Error en lambda_handler: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

