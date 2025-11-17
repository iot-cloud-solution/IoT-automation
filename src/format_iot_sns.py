import json
import urllib.request
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import os

load_dotenv()
webhook_url = os.getenv("WEBHOOK_URL")
SLACK_WEBHOOK_URL = 'https://app.slack.com/client/T08TJ6NQGM6/C090FSKGYPN'

def convertir_epoch_a_fecha(epoch_ms):
    try:
        local_zone = timezone(timedelta(hours=-6))
        dt = datetime.fromtimestamp(epoch_ms / 1000, tz=local_zone)
        meses_es = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        ]
        mes_nombre = meses_es[dt.month - 1]
        return f"{dt.day} de {mes_nombre} de {dt.year}, {dt.strftime('%H:%M')} UTC"
    except Exception as e:
        print(f"Error al convertir fecha: {e}")
        return "Sin fecha"

def lambda_handler(event, context):
    try:
        print("Evento recibido:", json.dumps(event))

        device = event.get('clientId', 'Desconocido')
        timestamp_epoch = event.get('timestamp', 0)
        timestamp = convertir_epoch_a_fecha(timestamp_epoch)
        event_type = event.get('eventType', 'Desconocido').lower()

        color = "#FF0000" if event_type == "disconnected" else "#36A64F"

        disconnect_reason = event.get('disconnectReason', 'N/A')
        client_initiated = event.get('clientInitiatedDisconnect', False)

        slack_payload = {
            "attachments": [
                {
                    "color": color,
                    "blocks": [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": f"⚠️ Dispositivo: {device}",
                                "emoji": True
                            }
                        },
                        {"type": "divider"},
                        {
                            "type": "section",
                            "fields": [
                                {"type": "mrkdwn", "text": f"*Hora del evento:*\n{timestamp}"},
                                {"type": "mrkdwn", "text": f"*Motivo:*\n{disconnect_reason}"},
                                {"type": "mrkdwn", "text": f"*Evento:*\n{event_type}"},
                                {"type": "mrkdwn", "text": f"*Iniciado por cliente:*\n{client_initiated}"}
                            ]
                        }
                    ]
                }
            ]
        }

        req = urllib.request.Request(
            SLACK_WEBHOOK_URL,
            data=json.dumps(slack_payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as response:
            print("Mensaje enviado a Slack:", response.read())

        return {'statusCode': 200, 'body': 'Mensaje enviado correctamente a Slack'}

    except Exception as e:
        print("Error:", str(e))
        return {'statusCode': 500, 'body': str(e)}
