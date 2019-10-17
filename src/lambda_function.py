import os
import json
import boto3
import requests

from ynab import YNAB
from slack import build_message, response_types
from urllib.parse import parse_qs


def respond(err, res=None, **kwargs):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def handlePost(body):
    ynab = YNAB(body['user_id'][0])
    filtered_categories = ynab.search_categories(body['text'][0])
    response = build_message(filtered_categories)
    return response


def lambda_handler(event, context):
    operations = {
        'POST': handlePost
    }

    operation = event['httpMethod']
    if operation in operations:
        # If operation = GET pass along queryStringParams to handler
        # Otherwise parse the body as json and pass along to handler
        payload = event['queryStringParameters'] if operation == 'GET' else parse_qs(
            event['body'])
        return respond(None, operations[operation](payload))
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
