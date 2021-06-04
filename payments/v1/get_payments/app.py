import boto3
import json
import os
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_PAYMENTS_TABLE'])
    print(event)
    if "queryStringParameters" in event:
        try:
            if 'email' in event['queryStringParameters'] and 'status-date' in event['queryStringParameters']:
                email = event['queryStringParameters']['email']
                status_date = event['queryStringParameters']['statusDate']
                result = table.query(
                    Select = 'SPECIFIC_ATTRIBUTES',
                    KeyConditionExpression = Key('email').eq(email) & Key('status-date').begins_with(status_date),
                    ProjectionExpression = 'id, #date, amount, #status, issuedBy, details, dueDate, insurer, brokerEmail',
                    ExpressionAttributeNames = {
                        "#date": "date",
                        "#status": "status"
                    },
                )
                response_body = {
                    "statusCode": 200,
                    "body": {
                        "payments": result['Items']
                    }
                }
            elif 'email' in event['queryStringParameters'] and 'id' in event['queryStringParameters']:
                email = event['queryStringParameters']['email']
                result = table.query(
                    Select = 'SPECIFIC_ATTRIBUTES',
                    KeyConditionExpression = Key('email').eq(email) & Key('id').eq(event['queryStringParameters']['id']),
                    ProjectionExpression = 'email, id, #date, amount, #status, issuedBy, brokerEmail, details, dueDate, insurer',
                    ExpressionAttributeNames = {
                        "#date": "date",
                        "#status": "status"
                    },
                )
                response_body = {
                    "statusCode": 200,
                    "body": {
                        "payment": result['Items'][0]
                    }
                }
            else:
                response_body = {
                    "statusCode": 400,
                    "body": {
                        "message": "missing email"
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