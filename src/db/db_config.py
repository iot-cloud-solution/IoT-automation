import os
import psycopg2
import boto3
import json

def get_secrets():
  secret_name = os.getenv("SECRET_NAME")
  region = os.getenv("AWS_REGION")

  client = boto3.client(
    service_name='secretsmanager',
    region_name=region
  )

  response = client.get_secret_value(
    SecretId=secret_name
  )

  if 'SecretString' in response:
    secret_dict = json.loads(response['SecretString'])
  else:
    secret_dict = json.loads(response['SecretBinary'])

  return secret_dict

 
def get_db_conexion():
  try:
    credentials = get_secrets()

    conn = psycopg2.connect(
      host = credentials['host'],
      database = credentials['database'],
      user = credentials['username'],
      password = credentials['password'],
    )

    return conn

  except psycopg2.OperationalError as e:
    print("Error al conectar con la db", e)
    return None
  
  except Exception as e:
    print("Error inesperado", e)
    return None
 