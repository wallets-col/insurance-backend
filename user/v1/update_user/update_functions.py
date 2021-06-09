import boto3
import os
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_USER_TABLE'])

def update_user_code(user):
    update_response = table.update_item(
        Key={
            'id': user['id'],
            'email': user['email']
        },
        UpdateExpression = "set userCode = :wcode",
        ExpressionAttributeValues = {
            ':wcode': user['userCode']
        },
        ReturnValues = "UPDATED_NEW"
    )
    print(update_response)
    return update_response

def update_name(user):
    update_response = table.update_item(
        Key={
            'id': user['id'],
            'email': user['email']
        },
        UpdateExpression = "set #name = :name",
        ExpressionAttributeValues = {
            ':name': user['name']
        },
        ExpressionAttributeNames = {
            "#name": "name"
        },
        ReturnValues = "UPDATED_NEW"
    )
    print(update_response)
    return update_response