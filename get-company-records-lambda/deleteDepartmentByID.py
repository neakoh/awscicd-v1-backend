import json
import time
import pymysql

def delete_department_by_id(department_id, event, creds, context):

  db_user = creds['user']
  db_password = creds['pass']
  db_host = creds['db_host']
  db_name = creds['d']

  execution_start_time = time.time()

  headers = {
      "Content-Type": "application/json; charset=UTF-8",
      "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  }

  if not department_id:
      return {
          'statusCode': 400,
          'headers': headers,
          'body': json.dumps({
              'status': {
                  'code': "400",
                  'name': "error",
                  'description': "Missing department ID",
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

      with conn.cursor() as cursor:
          
          sql_query = 'DELETE FROM department WHERE id = %s'
          cursor.execute(sql_query, (department_id,)) 
          conn.commit()

          if cursor.rowcount == 0:
              return {
                  'statusCode': 404,
                  'headers': headers,
                  'body': json.dumps({
                      'status': {
                          'code': "404",
                          'name': "not found",
                          'description': "Department not found",
                          'returnedIn': (time.time() - execution_start_time) * 1000 
                      },
                      'data': []
                  })
              }

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
                  'data': []
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