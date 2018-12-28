from __future__ import print_function
import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import json
import uuid
import time



USER_POOL_ID = 'eu-central-1_CakwLVb47'
CLIENT_ID = '1mll39npejv4maltcii43u8mv3'


def hello(event, context):

    return  [
        {
            "name":"A",
            "age":20,
            "cars":["qwe","ewq"]
        },

        {
            "name":"C",
            "age":22,
            "cars":["qwe","ewq"]
        },

        {
            "name":"B",
            "age":21,
            "cars":["qwe","ewq"]
        },
        ]


def psadmin(event, context):
    client = boto3.client('cognito-idp')
    UserPool_Id = USER_POOL_ID
    List_Group_Name = list()
    dicti = {}
    response = client.list_users(
        UserPoolId=UserPool_Id
    )
    List_Group_Users = list()
    dictionnaire={}
    for user in response["Users"]:
        dictionnaire["UserName"]=user["Username"]

        response2 = client.admin_list_groups_for_user(
            Username=user["Username"],
            UserPoolId=UserPool_Id
        )
        List_Group_Name=list()
        for group in  response2["Groups"]:
            List_Group_Name.append(group["GroupName"])

        dictionnaire["Groups"]=List_Group_Name
        List_Group_Users.append(dictionnaire)
        dictionnaire={}

    return(List_Group_Users)


def groupadd(event, context):
    UserPool_Id = USER_POOL_ID
    Client_Id = CLIENT_ID

    client = boto3.client('cognito-idp')

    body = event
    username = body['username']
    adding = client.admin_add_user_to_group(
        UserPoolId=UserPool_Id,
        Username=username,
        GroupName='Users')
    return username
