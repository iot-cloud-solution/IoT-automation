import os
import psycopg2
 
def get_db_conexion():
  try:
    print("HOST:", os.getenv("DB_HOST"))
    print("DB:", os.getenv("DATABASE"))
    print("USER:", os.getenv("USER_DB"))
    
    conn = psycopg2.connect(
      host= os.getenv("DB_HOST"),
      database= os.getenv("DATABASE"),
      user= os.getenv("USER_DB"),
      password= os.getenv("PASSWORD")
    )
    return conn

  except psycopg2.OperationalError as e:
    print("Error al conectar con la db", e)
    return None
 