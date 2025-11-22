import os
from dotenv import load_dotenv
import psycopg2
 
load_dotenv()
 
def get_db_conexion():
  try:
    conn = psycopg2.connect(
      host= os.getenv("DB_HOST"),
      database= os.getenv("DATABASE"),
      user= os.getenv("USER_DB"),
      password= os.getenv("PASSWORD")
    )
    return conn

  except psycopg2.OperationalError as e:
    return("Error al conectar con la db", e)
 