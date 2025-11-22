from src.db.db_config import get_db_conexion

def lambda_handler(event, context):
  con = get_db_conexion()
  if con:
    return "Conexion exitosa"
  else:
    return "Error al conectar con la base de datos"
  
  