import boto3
import json
from update_functions import update_name

def lambda_handler(event, context):
    print(event)
    if "body" in event and "user" in event['body']:
        try:
            user = json.loads(event['body'])
            user = user['user']
            if "name" in user:
                update_name(user)
            response_body = {
                "statusCode": 200,
                "body": {
                    "message": "valores actualizados"
                }
            }
        except Exception as ex:
            print(ex)
            response_body = {
                "statusCode": 500,
                "body": {
                    "message": "error, ver logs"
                }
            }
    else:
        response_body = {
            "statusCode": 400,
            "body": {
                "message": "Error en parámetros, debe enviar objeto user en event"
            }
        }
    return json.dumps(response_body)