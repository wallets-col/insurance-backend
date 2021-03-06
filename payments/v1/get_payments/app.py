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
                status_date = event['queryStringParameters']['status-date']
                result = table.query(
                    Select = 'SPECIFIC_ATTRIBUTES',
                    IndexName = 'email-status-date-index',
                    KeyConditionExpression = Key('email').eq(email) & Key('status-date').begins_with(status_date),
                    ProjectionExpression = 'id, #date, amount, #status, brokerName, details, dueDate, insurer, brokerEmail',
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
            elif 'brokerEmail' in event['queryStringParameters'] and 'status-date' in event['queryStringParameters']:
                email = event['queryStringParameters']['brokerEmail']
                status_date = event['queryStringParameters']['status-date']
                result = table.query(
                    Select = 'SPECIFIC_ATTRIBUTES',
                    IndexName = 'brokerEmail-status-date-index',
                    KeyConditionExpression = Key('brokerEmail').eq(email) & Key('status-date').begins_with(status_date),
                    ProjectionExpression = 'id, #date, amount, #status, brokerName, details, dueDate, insurer, #email, #name',
                    ExpressionAttributeNames = {
                        "#date": "date",
                        "#status": "status",
                        "#email": "email",
                        "#name": "name"
                    }
                )
                response_body = {
                    "statusCode": 200,
                    "body": {
                        "payments": result['Items']
                    }
                }
            elif 'email' in event['queryStringParameters'] and 'id' in event['queryStringParameters']:
                email = event['queryStringParameters']['email']
                payment_id = event['queryStringParameters']['id']
                result = table.query(
                    Select = 'SPECIFIC_ATTRIBUTES',
                    KeyConditionExpression = Key('email').eq(email) & Key('id').eq(payment_id),
                    ProjectionExpression = 'email, id, #date, amount, #status, issuedBy, brokerEmail, details, dueDate, insurer',
                    ExpressionAttributeNames = {
                        "#date": "date",
                        "#status": "status"
                    },
                )
                if len(result['Items']) > 0:
                    response_body = {
                        "statusCode": 200,
                        "body": {
                            "payment": result['Items'][0]
                        }
                    }
                else:
                    response_body = {
                        "statusCode": 200,
                        "body": {
                            "message": f"no payment found with id {payment_id} for user {email}"
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
                "message": "Error en par??metros, debe enviar email"
            }
        }
    return json.dumps(response_body)