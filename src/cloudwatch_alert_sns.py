import json
import urllib.request
from datetime import datetime

SLACK_WEBHOOK_URL = ''

def formatear_fecha(fecha_str):
    try:
        fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M:%S.%f%z")
        meses_es = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        ]
        mes_nombre = meses_es[fecha_obj.month - 1]
        return f"{fecha_obj.day} de {mes_nombre} de {fecha_obj.year}, {fecha_obj.strftime('%H:%M')} UTC"
    except Exception as e:
        print(f"Error al formatear fecha: {e}")
        return fecha_str

def lambda_handler(event, context):
    try:
        sns_message = event['Records'][0]['Sns']['Message']
        alarm = json.loads(sns_message)

        alarm_name = alarm.get('AlarmName', 'N/A')
        state = alarm.get('NewStateValue', 'N/A')
        reason = alarm.get('NewStateReason', 'N/A')
        description = alarm.get('AlarmDescription', 'Sin descripción')
        region = alarm.get('Region', 'N/A')
        raw_time = alarm.get('StateChangeTime', 'N/A')
        time = formatear_fecha(raw_time) if raw_time != 'N/A' else 'Sin fecha'

        border_color = "#00CED1"

        slack_payload = {
            "attachments": [
                {
                    "color": border_color,
                    "blocks": [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": f"🚨 Alerta de CloudWatch: {alarm_name}",
                                "emoji": True
                            }
                        },
                        { "type": "divider" },
                        {
                            "type": "section",
                            "fields": [
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Estado:*\n{'🔴 ALARM' if state == 'ALARM' else '🟢 OK'}"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Región:*\n{region}"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Hora:*\n{time}"
                                }
                            ]
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"*Descripción:*\n{description}\n\n*Motivo:*\n{reason}"
                            }
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
            print("Mensaje enviado con estilo:", response.read())

        return {'statusCode': 200, 'body': 'Mensaje enviado con formato legible'}
    
    except Exception as e:
        print("Error:", str(e))
        return {'statusCode': 500, 'body': str(e)}
