import sys
import logging
import pymysql
import dbinfo
from urllib.parse import unquote

connection = pymysql.connect(host = dbinfo.db_host, port = dbinfo.db_port,
    user = dbinfo.db_username, passwd = dbinfo.db_password, db = dbinfo.db_name)


def lambda_handler(event, context):
    # user_id=id&artimg_url=url&artwork_name=name&artwork_url=url&public_mode=0

    user_id = event['body'].split('user_id=')[1].split('&artimg_url=')[0]
    artimg_url = event['body'].split('artimg_url=')[1].split('&artwork_name=')[0]
    artwork_name = event['body'].split('artwork_name=')[1].split('&artwork_url=')[0]
    artwork_url = event['body'].split('artwork_url=')[1].split('&public_mode=')[0]
    public_mode = event['body'].split('public_mode=')[1]

    return update_db(user_id, artimg_url, artwork_name, artwork_url, public_mode)


def update_db(user_id, artimg_url, artwork_name, artwork_url, public_mode):
    user_id = unquote(user_id, encoding='utf-8', errors='replace')
    artimg_url = unquote(artimg_url, encoding='utf-8', errors='replace')
    artwork_name = unquote(artwork_name, encoding='utf-8', errors='replace')
    artwork_url = unquote(artwork_url, encoding='utf-8', errors='replace')
    artwork_url = "[AWS-S3-Bucket]/artwork/" + artwork_url + ".fbx"

    cursor = connection.cursor()
    query = f"insert into artwork (user_id, artimg_url, artwork_name, artwork_url, public_mode, like_num) values ('{user_id}', '{artimg_url}', '{artwork_name}', '{artwork_url}', {public_mode}, 0)"
    cursor.execute(query)
    connection.commit()
    
    if (user_id == "") or (artimg_url == "") or (artwork_name == ""):

        return {
            'statusCode': 400,
            'body': "Data value is null" 
        }
    else:

        return {
            'statusCode': 200,
            'body': "Updating artlist info complete" 
        }
        