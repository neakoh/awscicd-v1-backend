import json
import boto3
import time
import requests
import os

# Import functions from other files
from insertDepartment import insert_department
from getAllDepartments import get_all_departments
from getDepartmentByID import get_department_by_id
from deleteDepartmentByID import delete_department_by_id
from insertEmployee import insert_employee
from getAllPersonnel import get_all_personnel
from getPersonnelByID import get_personnel_by_id
from deleteEmployee import delete_employee
from updateEmployee import update_employee
from insertLocation import insert_location
from getAllLocations import get_all_locations
from deleteLocation import delete_location
from getAll import get_all

headers = {
      "Content-Type": "application/json; charset=UTF-8",
      "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  }

def get_secret(secret_name, region_name):
     session = boto3.session.Session()
     client = session.client(
         service_name='secretsmanager',
         region_name=region_name
     )
  
     try:
         get_secret_value_response = client.get_secret_value(
             SecretId=secret_name
         )
     except ClientError as e:
         raise e
  
     secret = get_secret_value_response['SecretString']
     return json.loads(secret)

def get_terraform_outputs():
  secrets = get_secret("HCP_API", "eu-west-2")
  url = f"https://app.terraform.io/api/v2/workspaces/{secrets.HCP_WORKSPACE_ID}/current-state-version-outputs"
  headers = {
      "Authorization": f"Bearer {secrets.HCP_API_TOKEN}",
      "Content-Type": "application/vnd.api+json"
  }
  try:
    response = requests.get(url, headers=headers)
    data = response.json()
    outputs = {}
    for i in data["data"]:
        if i["attributes"]["name"] == "rds_endpoint":
            outputs["rds_endpoint"] = i["attributes"]["value"]
        if i["attributes"]["name"] == "rds_endpoint":
            outputs["rds_name"] = i["attributes"]["value"]
    return outputs
  except requests.exceptions.RequestException as e:
      print(f"An error occurred: {e}")
      return None
  

def create_response(status_code, description, start_time, data=None):
  return {
      'statusCode': status_code,
      'headers': headers,
      'body': json.dumps({
          'status': {
              'code': str(status_code),
              'name': "ok" if status_code == 200 else "error",
              'description': description,
              'returnedIn': (time.time() - start_time) * 1000, 
          },
          'data': data or []
      })
  }

def lambda_handler(event, context):
  
  execution_start_time = time.time()

  secret = get_secret("rds-credentials-12", "eu-west-2")
  database = get_terraform_outputs()
  username = secret["username"]
  password = secret["password"]
  db_host = database['rds_endpoint']
  db_name = database['rds_name']
  creds = {"user":username, "pass":password, "db_host":db_host, "db_name":db_name}
  
  print("Received event:", json.dumps(event, indent=2))
  
  http_method = event.get('httpMethod')
  resource = event.get('resource')

  if resource == "/all" and http_method =="GET":
      return get_all(event, creds, execution_start_time)
  elif resource == "/personnel" and http_method == "POST":
      return insert_employee(event, creds, execution_start_time)
  elif resource == "/personnel" and http_method == "GET":
      return get_all_personnel(event, creds, execution_start_time)
  elif resource == "/personnel/{id}" and http_method == "GET":
      personnel_id = event.get('pathParameters', {}).get('id')
      return get_personnel_by_id(personnel_id, event, creds, execution_start_time)
  elif resource == "/personnel/{id}" and http_method == "DELETE":
      personnel_id = event.get('pathParameters', {}).get('id')  
      return delete_employee(personnel_id, event, creds, execution_start_time)
  elif resource == "/personnel/{id}" and http_method == "PUT":
      personnel_id = event.get('pathParameters', {}).get('id')
      return update_employee(personnel_id, event, creds, execution_start_time)

  # Department operations
  elif resource == "/departments" and http_method == "POST":
      return insert_department(event, creds, execution_start_time)
  elif resource == "/departments" and http_method == "GET":
      return get_all_departments(event, creds, execution_start_time)
  elif resource == "/departments/{id}" and http_method == "GET":
      department_id = event.get('pathParameters', {}).get('id')
      return get_department_by_id(department_id, event, creds, execution_start_time)
  elif resource == "/departments/{id}" and http_method == "DELETE":
      department_id = event.get('pathParameters', {}).get('id')
      return delete_department_by_id(department_id, event, creds, execution_start_time)

  # Location operations
  elif resource == "/locations" and http_method == "POST":
      return insert_location(event, creds, execution_start_time)
  elif resource == "/locations" and http_method == "GET":
      return get_all_locations(event, creds, execution_start_time)
  elif resource == "/locations/{id}" and http_method == "DELETE":
      location_id = event.get('pathParameters', {}).get('id')
      return delete_location(location_id, event, creds, execution_start_time)

  # If no matching path is found
  return create_response(404, "Not Found", execution_start_time, [event])