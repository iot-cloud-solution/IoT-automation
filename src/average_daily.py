from datetime import datetime, timedelta, timezone
from utils.dynamo_query import get_items_by_date
from utils.sns_alert import send_alert

TOPIC_ARN = "arn:aws:sns:us-east-2:445985103001:alertas_promedios"

def lambda_handler(event, context):

    # ---- Fecha actual y ayer ----
    now = datetime.now(timezone.utc)
    yesterday = now - timedelta(days=1)

    # ---- Rango de ayer en UTC ----
    inicio = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    fin = yesterday.replace(hour=23, minute=59, second=59, microsecond=0)

    # ---- Convertir a timestamps como DynamoDB los guarda ----
    start_ts = int(inicio.timestamp())
    end_ts = int(fin.timestamp())

    print(f"Buscando datos entre {start_ts} y {end_ts}")

    # ---- Obtener datos ----
    items = get_items_by_date(start_ts, end_ts)

    if not items:
        send_alert(TOPIC_ARN, f"No hay datos del día {yesterday.date()}.")
        return {"status": "NO_DATA"}

    # ---- Cálculos ----
    temps = [float(i.get("temperature", 0)) for i in items]
    hums = [float(i.get("humidity", 0)) for i in items]

    temp_avg = sum(temps) / len(temps)
    hum_avg = sum(hums) / len(hums)

    msg = f"""
    *Promedio Diario* — {yesterday.date()}  
    Temperatura: {temp_avg:.2f}  
    Humedad: {hum_avg:.2f}  
    Registros procesados: {len(items)}
    """

    send_alert(TOPIC_ARN, msg)

    return {"status": "OK", "message": msg}
