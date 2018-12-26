import json
import uuid
import boto3
import os


def hello(event, context):
    body = {
        "message": "v: 1.1"
    }

    response = {
        "body": json.dumps(body)
    }

    return response





def imageR(event, context):
    body = {
        "message": "V: image"
    }

    response = {
        "body": json.dumps(body)
    }

    return response