import json
import boto3
import time
from decimal import Decimal

dynamo_db = boto3.resource('dynamodb')
d_table = dynamo_db.Table('tabla-granja')

def lambda_handler(event, context):
    try:
        print("EVENT RAW:", json.dumps(event))
        payload = event  # IoT envía el JSON del mensaje directamente

        unique_id = int(time.time())
        payload['id'] = unique_id
        payload['timestamp'] = str(payload['timestamp'])

        for key in payload:
            if isinstance(payload[key], float):
                payload[key] = Decimal(str(payload[key]))
                
        print("Payload: ", payload)

        response = d_table.put_item(Item=payload)

        return {
            'statusCode': 200,
            'body': json.dumps('Payload procesado correctamente')
        }

    except Exception as e:
        print("Error: ", e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error al procesar el payload')
        }