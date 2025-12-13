import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def send_alert(topic_arn, message):
    if not topic_arn:
        logger.error("SNS Topic ARN no proporcionado.")
        return {"status": "ERROR", "detail": "Topic ARN vacío"}

    if not message:
        logger.error("Mensaje vacío, no se envió alerta.")
        return {"status": "ERROR", "detail": "Mensaje vacío"}

    try:
        sns = boto3.client("sns")
        response = sns.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject="Alerta IoT – Promedios"
        )
        
        logger.info(f"Alerta SNS enviada correctamente: {response}")
        return {"status": "OK", "message_id": response.get("MessageId")}

    except Exception as e:
        logger.exception("Error enviando alerta por SNS.")
        return {"status": "ERROR", "detail": str(e)}


# 🚀 Handler que Lambda ejecutará cuando pruebes la función
def lambda_handler(event, context):
    topic_arn = "arn:aws:sns:us-east-2:445985103001:alertas_promedios"
    message = "🔔 Prueba de alerta SNS desde Lambda (enviada correctamente)."

    return send_alert(topic_arn, message)

