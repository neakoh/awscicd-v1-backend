import json
import time
import pymysql
import os

def get_all(event, creds, context):
  
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

      all_data = {}

      all_data['personnel'] = get_all_personnel(conn)

      all_data['locations'] = get_all_locations(conn)

      all_data['departments'] = get_all_departments(conn)

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
              'data': all_data
          })
      }

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
      if conn:
          conn.close()

def get_all_personnel(conn):
  with conn.cursor() as cursor:
      sql_query = """
          SELECT 
              p.id, p.lastName, p.firstName, p.jobTitle, p.email, 
              d.name as department, l.name as location 
          FROM 
              personnel p 
          LEFT JOIN 
              department d ON (d.id = p.departmentID) 
          LEFT JOIN 
              location l ON (l.id = d.locationID) 
          ORDER BY 
              p.id, p.lastName, p.firstName, d.name, l.name
      """
      cursor.execute(sql_query)
      results = cursor.fetchall()
      return format_results(cursor, results)

def get_all_locations(conn):
  with conn.cursor() as cursor:
      sql_query = 'SELECT id, name FROM location'
      cursor.execute(sql_query)
      results = cursor.fetchall()
      return format_results(cursor, results)

def get_all_departments(conn):
  with conn.cursor() as cursor:
      sql_query = """
          SELECT 
              d.id, d.name, l.id as locationID  
          FROM 
              department d 
          LEFT JOIN 
                  location l ON (l.id = d.locationID) 
          ORDER BY 
              d.id
      """
      cursor.execute(sql_query)
      results = cursor.fetchall()
      return format_results(cursor, results)

def format_results(cursor, results):
  data = []
  for row in results:
      data.append(dict(zip([column[0] for column in cursor.description], row)))
  return data