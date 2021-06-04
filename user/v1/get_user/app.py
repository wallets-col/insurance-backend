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
            if 'email' in event['queryStringParameters'] and 'clientEmail' in event['queryStringParameters']:
                email = event['queryStringParameters']['email']
                client_email = event['queryStringParameters']['clientEmail']
                result = table.query(
                    Select = 'SPECIFIC_ATTRIBUTES',
                    KeyConditionExpression = Key('email').eq(email) & Key('clientEmail').eq(client_email),
                    ProjectionExpression = 'email, clientEmail, #name, #date, #status, #type, apiKey, userCode',
                    ExpressionAttributeNames = {
                        "#name": "name",
                        "#date": "date",
                        "#status": "status",
                        "#type": "type"
                    },
                )
                response_body = {
                    "statusCode": 200,
                    "body": {
                        "user": result['Items'][0]
                    }
                }
            elif 'clientEmail' in event['queryStringParameters']:
                email = event['queryStringParameters']['clientEmail']
                result = table.query(
                    Select = 'SPECIFIC_ATTRIBUTES',
                    KeyConditionExpression = Key('clientEmail').eq(email),
                    IndexName = 'clientEmail-userEmail-index',
                    ProjectionExpression = 'userEmail, clientEmail, #name, #date, #status, apiKey, userCode',
                    ExpressionAttributeNames = {
                        "#name": "name",
                        "#date": "date",
                        "#status": "status"
                    },
                )
                response_body = {
                    "statusCode": 200,
                    "body": {
                        "users": result['Items']
                    }
                }
            else:
                response_body = {
                    "statusCode": 400,
                    "body": {
                        "message": "missing userEmail or clientEmail"
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
                "message": "Error en parámetros, debe enviar email"
            }
        }
    return json.dumps(response_body)