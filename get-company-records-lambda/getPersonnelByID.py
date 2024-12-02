import json
import time
import pymysql
import os

def get_personnel_by_id(personnel_id, event, creds, context):
  
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
                  'description': f"Database connection error: {str(e)}",
                  'returnedIn': (time.time() - execution_start_time) * 1000 
              },
              'data': []
          })
      }


  if not personnel_id:
      return {
          'statusCode': 400,
          'headers': headers,
          'body': json.dumps({
              'status': {
                  'code': "400",
                  'name': "error",
                  'description': "Missing personnel ID",
                  'returnedIn': (time.time() - execution_start_time) * 1000
              },
              'data': []
          })
      }

  try:
      with conn.cursor() as cursor:
          sql_query = 'SELECT `id`, `firstName`, `lastName`, `email`, `jobTitle`, `departmentID` FROM `personnel` WHERE `id` = %s'
          cursor.execute(sql_query, (personnel_id,))

          personnel = cursor.fetchall()

          if not personnel:
              return {
                  'statusCode': 404,
                  'headers': headers,
                  'body': json.dumps({
                      'status': {
                          'code': "404",
                          'name': "not found",
                          'description': "Personnel not found",
                          'returnedIn': (time.time() - execution_start_time) * 1000 
                      },
                      'data': []
                  })
              }

          personnel_data = []
          for row in personnel:
              personnel_data.append({
                  'id': row[0],
                  'firstName': row[1],
                  'lastName': row[2],
                  'email': row[3],
                  'jobTitle': row[4],
                  'departmentID': row[5]
              })

          sql_query = 'SELECT id, name FROM department ORDER BY id'
          cursor.execute(sql_query)

          departments = cursor.fetchall()

          department_data = []
          for row in departments:
              department_data.append({
                  'id': row[0],
                  'name': row[1]
              })

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
              'data': {
                  'personnel': personnel_data,
                  'department': department_data
              }
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