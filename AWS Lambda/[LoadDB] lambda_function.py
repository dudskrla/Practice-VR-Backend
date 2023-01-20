import sys
import logging
import pymysql
import dbinfo

from urllib.parse import unquote

connection = pymysql.connect(host = dbinfo.db_host, port = dbinfo.db_port,
    user = dbinfo.db_username, passwd = dbinfo.db_password, db = dbinfo.db_name)


def lambda_handler(event, context):
    answer = load_db()
    if answer['body'].isspace():
        return {
            'statusCode': 400,
            'body': "Reply value is null" 
        }
    else:
        return answer
        
    
def load_db():
    cursor = connection.cursor()
    query = f"select * from artwork"
    cursor.execute(query)
    rows = cursor.fetchall()
    
    body = ""
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            body += str(rows[i][j]) + ">"
        body = body[:-1] + "|"
    body = body[:-1]
        
    if len(rows) == 0:
        return {
            'statusCode': 400,
            'body': "Fail to read artwork_like data" 
        }
    else:
        return {
        'statusCode': 200,
        'body': body
        }