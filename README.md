# AWS-Serverless-Data-Collector

This project implements an automatic data collection and storage system using AWS Lambda and Slack integration. The system monitors server availability and sends notifications to a Slack community when a server is unavailable. The project utilizes various AWS services, including AWS Lambda, EventBridge, Amazon RDS (MySQL), CloudWatch, and SNS.


# Usage
To use this system, follow these steps:

1)Set up an AWS account if you don't have one already.

2)Login to the aws management console ,Create an Amazon RDS instance with a MySQL database. Make note of the endpoint, database name, username, and password.

3)Create an AWS Lambda function**(data-collector-lambda.py)** and configure it to fetch data from the API at specified intervals (eg: 1 minute) using AWS EventBridge add the Layer file attached above to the lambda .Write the Lambda function code **(data-collector-lambda)** to  fetch data and store it in the Amazon RDS database.

4)Configure a CloudWatch alarm to trigger when this lambda execution fails. Set up an SNS topic to send notifications when the alarm is triggered.

5)Create another Lambda function **(server-atert-brodcast-lambda.py)** to confirm the unavailability of the RDS Instance by connecting to it. This lambda function executes **send_slack_message(msg)**  to send a broadcast message to the specified Slack community.

6) Deploy and test the system to ensure that it accurately fetches server availability data, stores it in the database, and sends notifications to the Slack community when the server is unavailable.
