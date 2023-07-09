import requests
import mysql.connector
import json

def getdata():
    try:
        response = requests.get("http://api.open-notify.org/iss-now.json")
        response.raise_for_status()  # Raise an exception if the request fails
        data = response.json()

        print("Data Fetched Sucessfully from API")
        
        return data

    except requests.exceptions.RequestException as e:
        # Handle request exception
        print("Error occurred while fetching data:", e)
        return None


def insert_data_to_database(data):
        # RDS configuration -> use created rds instance credentials
        DB_HOST = "xxxxxxxxxxxxxxxxxxxxxxxxxxx"
        DB_PORT = 3306
        DB_NAME = "your-database-name"
        DB_USER = "xxxx"
        DB_PASSWORD = "xxxxxx"
        connect_timeout = 30

  
        # Connect to the RDS MySQL instance
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            connect_timeout=connect_timeout
        )
        cursor = conn.cursor()
        
        cursor.execute("CREATE DATABASE IF NOT EXISTS rdslam")
        cursor.execute("USE rdslam")

        # Create the table if it doesn't exist
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS datatable (
            id INT AUTO_INCREMENT PRIMARY KEY,
            latitude FLOAT,
            longitude FLOAT
        )
        '''
        cursor.execute(create_table_query)

        # Extract latitude and longitude from the data
        latitude = data['iss_position']['latitude']
        longitude = data['iss_position']['longitude']

        # Insert latitude and longitude values into the database
        cursor.execute("INSERT INTO datatable (latitude, longitude) VALUES (%s, %s)", (latitude, longitude))

        # Commit the changes
        conn.commit()        
        
        cursor.execute("USE rdslam")
        
        select_query = "SELECT * FROM datatable"
        cursor.execute(select_query)
        # Fetch all records and print them
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        
        
        print("Data inserted to RDS")

        # Close the cursor and the connection
        cursor.close()
        conn.close()



def lambda_handler(event, context):
    # Fetch data from the API
    data = getdata()
    
    if data is not None:
        print("Data fetched successfully:", data)
        
        # Insert data into the database
        a = insert_data_to_database(data)

        
    else:
        print("Failed to fetch data from the API")
    
    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }
