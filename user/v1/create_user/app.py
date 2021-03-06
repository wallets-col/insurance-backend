import boto3
import json
import os
import datetime
import pytz
import uuid

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_USER_TABLE'])
    print(event)
    if "body" in event and "user" in event['body']:
        try:
            get_date = datetime.datetime.now(pytz.timezone('UTC')).astimezone(pytz.timezone('America/Panama')).strftime("%Y-%m-%dT%H:%M:%S")
            user = json.loads(event['body'])
            user = user['user']
            uuid_code = str(uuid.uuid4())
            if user['type'] == 'USER':
                item = {
                    'email': user['email'],
                    'id': uuid_code[0:13],
                    'name': user['name'],
                    'date': get_date,
                    'creditCards': [],
                    'status': 'ACTIVE',
                    'apiKey': uuid_code,
                    'type': 'USER',
                    'phoneNumber': user['phoneNumber'],
                    'brokerId': user['brokerId']
                }
                table.put_item(Item=item)
                response_body = {
                    "statusCode": 200,
                    "body": {
                        "user": item
                    }
                }
            elif user['type'] == 'BROKER':
                item = {
                    'email': user['email'],
                    'id': uuid_code[0:13],
                    'name': user['name'],
                    'date': get_date,
                    'status': 'ACTIVE',
                    'type': 'BROKER'
                }
                table.put_item(Item=item)
                response_body = {
                    "statusCode": 200,
                    "body": {
                        "user": item
                    }
                }
            else:
                response_body = {
                    "statusCode": 400,
                    "body": {
                        "message": "missing user"
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
                "message": "Error en par??metros, debe enviar objeto user en event"
            }
        }
    return json.dumps(response_body)