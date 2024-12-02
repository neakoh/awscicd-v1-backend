import json
import time
import pymysql
import os

def get_all_locations(event, creds, context):
  
  db_user = creds['user']
  db_password = creds['pass']
  db_host = creds['db_host']
  db_name = creds['db_name']

  execution_start_time = time.time()

  headers = {
      "Content-Type": "application/json; charset=UTF-8",
      "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  }

  try:
      conn = pymysql.connect(host=db_host,
                             user=db_user,
                             password=db_password,
                             db=db_name)

  except pymysql.MySQLError as e:
      return {
          'statusCode': 300,
          'headers': headers, 
          'body': json.dumps({
              'status': {
                  'code': "300",
                  'name': "failure",
                  'description': "database unavailable",
                  'returnedIn': (time.time() - execution_start_time) * 1000
              },
              'data': []
          })
      }

  try:
      sql_query = 'SELECT id, name FROM location'
      with conn.cursor() as cursor:
          cursor.execute(sql_query)

          results = cursor.fetchall()

      data = []
      for row in results:
          data.append(dict(zip([column[0] for column in cursor.description], row)))
      return {
          'statusCode': 200,
          'headers': headers, 
          'body': json.dumps({
              'status': {
                  'code': "200",
                  'name': "ok",
                  'description': "success",
                  'returnedIn': (time.time() - execution_start_time) * 1000 
              },
              'data': data
          })
      }

  except Exception as e:
      return {
          'statusCode': 400,
          'headers': headers,
          'body': json.dumps({
              'status': {
                  'code': "400",
                  'name': "error",
                  'description': f"An error occurred: {str(e)}",
                  'returnedIn': (time.time() - execution_start_time) * 1000 
              },
              'data': []
          })
      }

  finally:
      conn.close()