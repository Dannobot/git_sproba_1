from __future__ import print_function
import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import json
import uuid
import time
import psycopg2

USER_POOL_ID = 'eu-central-1_sv3IArE82'
CLIENT_ID = '3scu9bmh1afbq0fqbi78ti3spg'
hosty = 'mysecondtry.crnnnvtksbkt.eu-central-1.rds.amazonaws.com'
client = boto3.client('cognito-idp')

def userGrup_triger(event, context):
    # тригер що додає юзера у групу
    username = event['userName']
    
    data = json.dumps(event)
    y = json.loads(data)

    adding = client.admin_add_user_to_group(
        UserPoolId=USER_POOL_ID,
        Username=username,
        GroupName='Users')
    return y

#############################RDS###############################
def in_rds(event):
    result = []
    conn = psycopg2.connect(dbname='databasetest', user='dodo_mc', password='danqwe1996', host=hosty)
    # добавляє юзера в таблицю
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO dev_users (Email, Username, Name, Surname, Password) VALUES (%s, %s, %s, %s, %s )',
            (event['Email'], event['Username'], event['Name'], event['Surname'], event['Password'],))
        cursor.execute('SELECT * FROM dev_users')
        conn.commit()

        for row in cursor:
            result.append(list(row))

        cursor.close()

def createUser_in_table(event, context):
    return in_rds(event)


def out_rds(event):

    result = []
    tables = ['Id','Name','Surname','Username','Email','Password']
    conn = psycopg2.connect(dbname='databasetest', user='dodo_mc', password='danqwe1996', host=hosty)
    
    # з виводить всі дані юзаре по емайлу
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM dev_users WHERE email = (%s) ", (event['Email'], ))
        conn.commit()
        
        for row in cursor:
            for i in row:
                result.append(i)
        sresult = dict(zip(tables, result))
        cursor.close()   
        return sresult

def outUser_data_fromTable(event, context):
    return out_rds(event)


def get_rds(event):
    # виводить тейбл news
    result = []
    tables = ['Id','Title','Description','Author_id']
    result2 = []
    conn = psycopg2.connect(dbname='databasetest', user='dodo_mc', password='danqwe1996', host=hosty)

    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM dev_newsbd')
        conn.commit()

        for row in cursor:
            result.append(list(row))
        
        
        for i in result:
            result2.append(dict(zip(tables, i)))
            
        return result2
        cursor.close()

def getNews_data(event, context):
    return get_rds(event)



def add_news_rds(event):

    result = []
    conn = psycopg2.connect(dbname='databasetest', user='dodo_mc', password='danqwe1996', host=hosty)
    
    with conn.cursor() as cursor:
        # add news
        cursor.execute('INSERT INTO dev_newsbd (title, description, author_id) VALUES (%s, %s, %s)',
            (event['Title'], event['Description'], event['Author_id'],))
        cursor.execute('SELECT * FROM dev_newsbd')
        conn.commit()
        
        for row in cursor:
            result.append(list(row))
        cursor.close()


def addNews_data(event, context):
    add_news_rds(event)


def delete_news_rds(event):

    conn = psycopg2.connect(dbname='databasetest', user='dodo_mc', password='danqwe1996', host=hosty)
    # delete news
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM dev_newsbd WHERE id = {Id}'.format(**event))
        conn.commit()
        cursor.close()


def deleteNews_data(event, context):
    delete_news_rds(event)

#############################AdminReg###############################
# тут свій клієнт з секретом
CLIENT_ID = '3g1e79srtskt37hdsv2e8m29f4'
CLIENT_SECRET = 'fo6qr0809h95cs17airirindtk46q39k8ndkhsj4r53t3n5gsvm'


def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'), 
        msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2

ERROR = 0
SUCCESS = 1
USER_EXISTS = 2
    
def sign_up(username, password):
    try:
        resp = client.sign_up(
            ClientId=CLIENT_ID,
            SecretHash=get_secret_hash(username),
            Username=username,
            Password=password)
        print(resp)
    except client.exceptions.UsernameExistsException as e:
        return USER_EXISTS
    except Exception as e:
        print(e)
        return ERROR
    return SUCCESS
    
    
def adminreg(event, context):

    body = event
    username = body['username']
    password = body['password']
    is_new = "false"
    user_id = str(uuid.uuid4())
    signed_up = sign_up(username, password)
    if signed_up == ERROR:
        return {'status': 'fail', 'msg': 'failed to sign up'}
    if signed_up == SUCCESS:
        is_new = "true"
        return {'status': 'good', 'msg': 'sign up'}
####################################################################
