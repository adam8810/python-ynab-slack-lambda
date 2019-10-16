import os
import json
import boto3
import requests
from ynab import YNAB
from slack import build_message, response_types


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def handlePost(body):
    ynab = YNAB(body['user_id'])
    filtered_categories = ynab.search_categories(body['text'])
    return build_message(filtered_categories)


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    operations = {
        'POST': handlePost
    }

    operation = event['httpMethod']
    if operation in operations:
        # If operation = GET pass along queryStringParams to handler
        # Otherwise parse the body as json and pass along to handler
        payload = event['queryStringParameters'] if operation == 'GET' else json.loads(
            event['body'])
        return respond(None, operations[operation](payload))
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
