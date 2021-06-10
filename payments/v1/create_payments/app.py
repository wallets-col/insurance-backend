import boto3
import json
import os
import datetime
import pytz
import uuid

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_PAYMENTS_TABLE'])
    print(event)
    if "body" in event and "payment" in event['body']:
        try:
            get_date = datetime.datetime.now(pytz.timezone('UTC')).astimezone(pytz.timezone('America/Panama')).strftime("%Y-%m-%dT%H:%M:%S")
            payment = json.loads(event['body'])
            payment = payment['payment']
            uuid_code = str(uuid.uuid4())
            item = {
                'email': payment['email'],
                'id': uuid_code,
                'date': get_date,
                'dueDate': payment['dueDate'],
                'name': payment['name'],
                'status': 'PENDING',
                'insurer': payment['insurer'],
                'amount': payment['amount'],
                'brokerName': payment['brokerName'],
                'brokerEmail': payment['brokerEmail'],
                'status-date': f"PENDING-{get_date}",
                'details': payment['details']
            }
            table.put_item(Item=item)
            response_body = {
                "statusCode": 200,
                "body": {
                    "payment": item
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
                "message": "Error en parámetros, debe enviar objeto payment en event"
            }
        }
    return json.dumps(response_body)