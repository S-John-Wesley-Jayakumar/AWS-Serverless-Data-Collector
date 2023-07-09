

import json
import mysql.connector

def db_connectioncheck():
    # RDS configuration -> use created rds instance credentials
    DB_HOST = "xxxxxxxxxxxxxxxxxxxxxxxxxxx"
    DB_PORT = 3306
    DB_NAME = "your-database-name"
    DB_USER = "xxxx"
    DB_PASSWORD = "xxxxxx"
    connect_timeout = 30

    try:
        # Connect to the RDS MySQL instance
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            connect_timeout=connect_timeout
        )
        cursor = conn.cursor()
        
        mesg = "Database is now available"
        # Close the cursor and the connection
        cursor.close()
        conn.close()
        
        return str(mesg)

    #Capyuring error in DB Server and return for brodcasting in slack
    except mysql.connector.Error as err:
        # converting error message into string
        error_str = "RDS Server Database is not available ... error occurred:---> " + str(err)
        # Capture MySQL error
        print(err)
        return error_str

import requests
import json

def send_slack_message(msg):
    # Prepare the message text
    message = msg  # "Captured Server Unavaiable error meassage "
    
    # Slack webhook URL
    webhook_url = '................................'#enter your slack webhook url
    
    # Send the message to Slack
    payload = {
        'text': message
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(webhook_url, json=payload, headers=headers)
    
    # Check the Slack API response
    if response.status_code == 200:
        print('Message sent successfully to Slack!.......................',message)
    else:
        print('Failed to send message to Slack.')
        print(response.text)




def lambda_handler(event, context):
  
    a = db_connectioncheck()
    
    send_slack_message(a) 
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
