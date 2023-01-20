import sys
import logging
import pymysql
import dbinfo
from urllib.parse import unquote

connection = pymysql.connect(host = dbinfo.db_host, port = dbinfo.db_port,
    user = dbinfo.db_username, passwd = dbinfo.db_password, db = dbinfo.db_name)


def lambda_handler(event, context):
    # event['body'] in 
    # command=comment_read&artwork_id=id
    # command=comment_update&artwork_id=id&comment_val=val&comment_date=date
    # command=like_read&artwork_id=id
    # command=like_update&artwork_id=id
    # command=unlike_update&artwork_id=id

    command = event['body'].split('command=')[1].split('&artwork_id=')[0]
    
    if command == 'comment_read':
        artwork_id = event['body'].split('&artwork_id=')[1]
        return comment_read(artwork_id)
    elif command == 'comment_update':
        artwork_id = event['body'].split('&artwork_id=')[1].split('&comment_val=')[0]
        comment_val = event['body'].split('&comment_val=')[1].split('&comment_date=')[0]
        comment_date = event['body'].split('&comment_date=')[1]
        return comment_update(artwork_id, comment_val, comment_date)
    elif command == 'like_read':
        artwork_id = event['body'].split('&artwork_id=')[1]
        return like_read(artwork_id)
    elif command == 'like_update':
        artwork_id = event['body'].split('&artwork_id=')[1]
        return like_update(artwork_id)
    elif command == 'unlike_update':
        artwork_id = event['body'].split('&artwork_id=')[1]
        return unlike_update(artwork_id)
    else:
        return {
            'statusCode': 400,
            'body': "Invalid command" 
        }
    
    
def comment_read(artwork_id):
    cursor = connection.cursor()
    query = f"select * from comment where BINARY artwork_id = '{artwork_id}'"
    cursor.execute(query)
    rows = cursor.fetchall()
    length = len(rows)
    body = f"{length}|"
    comments = list()
    for i in range(length):
        body += rows[i][1] + ">" + rows[i][2] + "|" 
    
    return {
        'statusCode': 200,
        'body': body
    }
        
def comment_update(artwork_id, comment_val, comment_date):
    decode_comment_val = unquote(comment_val, encoding='utf-8', errors='replace')
    if comment_val != "":
        cursor = connection.cursor()
        query = f"insert into comment values ({artwork_id}, '{decode_comment_val}', '{comment_date}')"
        cursor.execute(query)
        connection.commit()
        
        return {
            'statusCode': 200,
            'body': "Updating comment complete" 
        }
    else:

        return {
            'statusCode': 400,
            'body': "Comment value is null" 
        }
        
def like_read(artwork_id):
    cursor = connection.cursor()
    query = f"select like_num from artwork where BINARY artwork_id = '{artwork_id}'"
    cursor.execute(query)
    rows = cursor.fetchall()
    
    if len(rows) == 0:

        return {
            'statusCode': 400,
            'body': "Fail to read artwork_like data" 
        }
    else:

        return {
            'statusCode': 200,
            'body': rows[0][0]
        }
        
def like_update(artwork_id):
    cursor = connection.cursor() 
    read_query = f"select like_num from artwork where BINARY artwork_id = '{artwork_id}'"
    cursor.execute(read_query)
    rows = cursor.fetchall()
    
    if len(rows) == 0:

        return {
            'statusCode': 400,
            'body': "Fail to read artwork_like data" 
        }
    else:
        like_num = rows[0][0]
        query = f"update artwork set like_num = {like_num+1} where artwork_id = {artwork_id}"
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
            
        return {
            'statusCode': 200,
            'body': "Updating like_num complete" 
        }

def unlike_update(artwork_id):
    cursor = connection.cursor()
    read_query = f"select like_num from artwork where BINARY artwork_id = '{artwork_id}'"
    cursor.execute(read_query)
    rows = cursor.fetchall()
    
    if len(rows) == 0:

        return {
            'statusCode': 400,
            'body': "Fail to read artwork_like data" 
        }
    else:
        like_num = rows[0][0]
        query = f"update artwork set like_num = {like_num-1} where artwork_id = {artwork_id}"
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
            
        return {
            'statusCode': 200,
            'body': "Updating unlike_num complete" 
        }