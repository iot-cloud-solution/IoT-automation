from datetime import datetime, timedelta, timezone
from utils.dynamo_query import get_items_by_date
from utils.sns_alert import send_alert

TOPIC_ARN = "arn:aws:sns:us-east-2:445985103001:alertas_promedios"

def lambda_handler(event, context):

    now = datetime.now(timezone.utc)

    # ---- Obtener lunes de la semana pasada ----
    # weekday(): Lunes=0 ... Domingo=6
    monday_last_week = now - timedelta(days=now.weekday() + 7)
    sunday_last_week = monday_last_week + timedelta(days=6)

    # ---- Rango completo ----
    inicio = monday_last_week.replace(hour=0, minute=0, second=0, microsecond=0)
    fin = sunday_last_week.replace(hour=23, minute=59, second=59, microsecond=0)

    # ---- Timestamps como los guardas en DynamoDB ----
    start_ts = int(inicio.timestamp())
    end_ts = int(fin.timestamp())

    print(f"Buscando items entre {start_ts} y {end_ts}")

    # ---- Obtener datos ----
    items = get_items_by_date(start_ts, end_ts)

    if not items:
        send_alert(TOPIC_ARN, "No se encontraron datos de la semana pasada.")
        return {"status": "NO_DATA"}

    # ---- Valores ----
    temps = [float(i.get("temperature", 0)) for i in items]
    hums = [float(i.get("humidity", 0)) for i in items]

    temp_avg = sum(temps) / len(temps)
    hum_avg = sum(hums) / len(hums)

    msg = f"""
    *Promedio semanal*
Semana del {inicio.date()} al {fin.date()}:

    Temperatura promedio: {temp_avg:.2f}
    Humedad promedio: {hum_avg:.2f}
    Total de registros analizados: {len(items)}
"""

    send_alert(TOPIC_ARN, msg)

    return {"status": "OK", "message": msg}
