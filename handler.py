from __future__ import print_function
import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import json
import uuid
import time
from dynamodb_json import json_util as jsoni

dynamodb = boto3.client('dynamodb')


def ddbMGgetPS(event, context):
    allitems = dynamodb.scan(TableName='MN-DEV')
    node = allitems['Items'][0]
    for key, value in node.items():
        valic = value
        for kei, val in valic.items():
            if(kei == "S" or kei == "N"):
                value = val
                node[key]
        print(value)
    return jsoni.loads(allitems['Items'])

def ddbgetPS(event, context):
    allitems = dynamodb.scan(TableName='DEV_FPS')
    node = allitems['Items'][0]
    for key, value in node.items():
        valic = value
        for kei, val in valic.items():
            if(kei == "S" or kei == "N"):
                value = val
                node[key]
        print(value)
    return jsoni.loads(allitems['Items'])    

