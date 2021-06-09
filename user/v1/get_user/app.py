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
            if 'brokerId' in event['queryStringParameters']:
                broker_id = event['queryStringParameters']['brokerId']
                result = table.query(
                    Select = 'SPECIFIC_ATTRIBUTES',
                    IndexName = 'type-brokerId-index',
                    KeyConditionExpression = Key('type').eq('USER') & Key('brokerId').eq(broker_id),
                    ProjectionExpression = '#type, brokerId, id, email, #name, creditCards, #status, phoneNumber,
                    ExpressionAttributeNames = {
                        "#name": "name",
                        "#status": "status",
                        "#type": "type"
                    }
                )
                response_body = {
                    "statusCode": 200,
                    "body": {
                        "users": result['Items']
                    }
                }
            elif 'email' in event['queryStringParameters'] and 'id' in event['queryStringParameters']:
                email = event['queryStringParameters']['email']
                user_id = event['queryStringParameters']['id']
                result = table.query(
                    KeyConditionExpression = Key('email').eq(email) & Key('id').eq(user_id)
                )
                if len(result['Items']) > 0:
                    response_body = {
                        "statusCode": 200,
                        "body": {
                            "user": result['Items'][0]
                        }
                    }
                else:
                    response_body = {
                        "statusCode": 200,
                        "body": {
                            "message": f"no user found with email {email}"
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