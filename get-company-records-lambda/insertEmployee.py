import json
import time
import pymysql
import os

def insert_employee(event, creds, context):
  
  db_user = creds['user']
  db_password = creds['pass']
  db_host = creds['db_host']
  db_name = creds['db_name']
  
  execution_start_time = time.time()

  body = json.loads(event.get('body', '{}'))
  first_name = body.get('first_name')
  last_name = body.get('last_name')
  job_title = body.get('job_title')
  email = body.get('email')
  department_id = body.get('departmentID')

  headers = {
      "Content-Type": "application/json; charset=UTF-8",
      "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  }

  if not first_name or not last_name or not job_title or not email or not department_id:
      return {
          'statusCode': 400,
          'headers': headers,
          'body': json.dumps({
              'status': {
                  'code': "400",
                  'name': "error",
                  'description': "Missing required fields",
                  'returnedIn': (time.time() - execution_start_time) * 1000 
              },
              'data': []
          })
      }

  try:
      conn = pymysql.connect(host=db_host,
                             user=db_user,
                             password=db_password,
                             db=db_name)

  except pymysql.MySQLError as e:
      return {
          'statusCode': 300,
          'headers': {
              "Content-Type": "application/json; charset=UTF-8",
              "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
              "Access-Control-Allow-Origin": "*",
              "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
          },
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
      with conn.cursor() as cursor:
          sql_query = "INSERT INTO personnel (firstName, lastName, jobTitle, email, departmentID) VALUES (%s, %s, %s, %s, %s)"
          cursor.execute(sql_query, (first_name, last_name, job_title, email, department_id))
          conn.commit()

      return {
          'statusCode': 200,
          'headers': {
              "Content-Type": "application/json; charset=UTF-8",
              "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
              "Access-Control-Allow-Origin": "*",
              "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
          },
          'body': json.dumps({
              'status': {
                  'code': "200",
                  'name': "ok",
                  'description': "success",
                  'returnedIn': (time.time() - execution_start_time) * 1000
              },
              'data': []
          })
      }

  except Exception as e:
      return {
          'statusCode': 400,
          'headers': {
              "Content-Type": "application/json; charset=UTF-8",
              "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
              "Access-Control-Allow-Origin": "*",
              "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
          },
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