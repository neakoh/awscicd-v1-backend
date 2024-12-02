import json
import time
import pymysql
import os
import re

def update_employee(personnel_id, event, creds, context):
    
    db_user = creds['user']
    db_password = creds['pass']
    db_host = creds['db_host']
    db_name = creds['db_name']

    execution_start_time = time.time()

    # Get the personnel details from the event (assuming they're passed as JSON body)
    body = json.loads(event.get('body', '{}'))
    first_name = body.get('first_name')
    last_name = body.get('last_name')
    job_title = body.get('job_title')
    email = body.get('email')
    department_id = body.get('departmentID')

    # Validate input
    if not first_name or not last_name or not job_title or not email or not department_id:
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
                    'description': "Missing required fields",
                    'returnedIn': (time.time() - execution_start_time) * 1000  # in milliseconds
                },
                'data': []
            })
        }

    # Validate email format
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
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
                    'description': "Invalid email format",
                    'returnedIn': (time.time() - execution_start_time) * 1000  # in milliseconds
                },
                'data': []
            })
        }

    try:
        # Connect to the database
        conn = pymysql.connect(host=db_host,
                               user=db_user,
                               password=db_password,
                               db=db_name)

        # Prepare the SQL statement to update the personnel record
        with conn.cursor() as cursor:
            sql_query = """
                UPDATE personnel 
                SET firstName = %s, lastName = %s, jobTitle = %s, email = %s, departmentID = %s 
                WHERE id = %s
            """
            cursor.execute(sql_query, (first_name, last_name, job_title, email, department_id, personnel_id))
            conn.commit()  # Commit the transaction

            # Check if any rows were affected
            if cursor.rowcount == 0:
                return {
                    'statusCode': 404,
                    'headers': {
                        "Content-Type": "application/json; charset=UTF-8",
                        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                    },
                    'body': json.dumps({
                        'status': {
                            'code': "404",
                            'name': "not found",
                            'description': "Personnel not found",
                            'returnedIn': (time.time() - execution_start_time) * 1000  # in milliseconds
                        },
                        'data': []
                    })
                }

        # Successful response
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
                    'returnedIn': (time.time() - execution_start_time) * 1000,  # in milliseconds
                },
                'data': []
            })
        }

    except pymysql.MySQLError as e:
        # Database connection error handling
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
                    'description': f"Database error: {str(e)}",
                    'returnedIn': (time.time() - execution_start_time) * 1000  # in milliseconds
                },
                'data': []
            })
        }

    except Exception as e:
        # General error handling
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
                    'returnedIn': (time.time() - execution_start_time) * 1000  # in milliseconds
                },
                'data': []
            })
        }

    finally:
        # Close the database connection
        conn.close()