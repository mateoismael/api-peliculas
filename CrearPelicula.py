import boto3
import uuid
import os
import json

def lambda_handler(event, context):
    try:
        # Entrada (json)
        print(json.dumps({
            "tipo": "INFO",
            "log_datos": {
                "message": "Inicio de la ejecución",
                "event": event
            }
        }))  # Log json en CloudWatch
        
        tenant_id = event['body']['tenant_id']
        pelicula_datos = event['body']['pelicula_datos']
        nombre_tabla = os.environ["TABLE_NAME"]
        
        # Proceso
        uuidv4 = str(uuid.uuid4())
        pelicula = {
            'tenant_id': tenant_id,
            'uuid': uuidv4,
            'pelicula_datos': pelicula_datos
        }
        
        # Conexión a DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(nombre_tabla)
        
        # Inserción en DynamoDB
        response = table.put_item(Item=pelicula)
        
        # Salida (json)
        print(json.dumps({
            "tipo": "INFO",
            "log_datos": {
                "message": "Película insertada correctamente",
                "pelicula": pelicula,
                "response": response
            }
        }))  # Log json en CloudWatch
        
        return {
            'statusCode': 200,
            'pelicula': pelicula,
            'response': response
        }
    
    except Exception as e:
        # Manejo de errores
        print(json.dumps({
            "tipo": "ERROR",
            "log_datos": {
                "message": "Error al procesar la película",
                "error": str(e)
            }
        }))  # Log de error en CloudWatch
        
        return {
            'statusCode': 500,
            'message': "Error interno del servidor"
        }
