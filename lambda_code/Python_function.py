import boto3
import json

client = boto3.client('logs')

list = client.describe_log_streams(logGroupName='access_logs',orderBy='LogStreamName')

print("the first log stream",list[logStreams.logStreamName[0]])