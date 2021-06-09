import boto3
import json
import os
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_USER_TABLE'])
    print(event)
    if "queryStringParameters" in event:
        try:
            if 'id' in event['queryStringParameters'] and 'email' in event['queryStringParameters']:
                user_id = event['queryStringParameters']['id']
                email = event['queryStringParameters']['email']
                result = table.delete_item(
                    Key={
                        'id': user_id,
                        'email': email
                    }
                )
                response_body = {
                    "statusCode": 200,
                    "body": {
                        "message": "user deleted"
                    }
                }
            else:
                response_body = {
                    "statusCode": 400,
                    "body": {
                        "message": "missing id or email"
                    }
                }
        except Exception as ex:
            print(ex)
            response_body = {
                "statusCode": 500,
                "body": {
                    "message": "error"
                }
            }
    else:
        response_body = {
            "statusCode": 400,
            "body": {
                "message": "Error en parámetros, debe enviar campo id y campo email"
            }
        }
    return json.dumps(response_body)