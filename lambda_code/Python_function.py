import boto3
import logging
import json
import gzip
import urllib
import time
from StringIO import StringIO
s3 = boto3.client('s3')

client = boto3.client('logs')

#listLog = client.describe_log_streams(logGroupName='ApacheAccessLogs_LG',orderBy='LogStreamName')

def create_bucket(bucketName):
    #Check if bucket already exist?
    s3Rec = boto3.resource('s3')
    if not s3Rec.Bucket(bucketName) in s3Rec.buckets.all():
        #Create a new bucket
        print("creating a bucket")
        s3.create_bucket(Bucket=bucketName, CreateBucketConfiguration={'LocationConstraint': 'us-west-2'})
        
def lambda_handler(event, context):

    prefixS3 = 'Logs_'
    
    #capture the CloudWatch log data
    outEvent = str(event['awslogs']['data'])
    
    #decode and unzip the log data
    outEvent = gzip.GzipFile(fileobj=StringIO(outEvent.decode('base64','strict'))).read()
    
    #convert the log data from JSON into a dictionary
    cleanEvent = json.loads(outEvent)

    bucketName = cleanEvent["logStream"].replace("/","-")
    print("bucketName", bucketName)
    #bucketS3 = "ip-10-0-2-20_access_logs.log"#logStreamName.replace("/", "_")
    create_bucket(bucketName)

    #create a temp file
    tempFile = open('/tmp/file', 'w+')
    
    #Create the S3 file key
    key = prefixS3 + str(int(time.time())) + ".log"
    
    #loop through the events line by line
    for t in cleanEvent['logEvents']:       
        #Transform the data and store it in the temp file. 
        tempFile.write(t['message'])

    #close the temp file
    tempFile.close()    
    
    #write the files to s3
    s3Results = s3.upload_file('/tmp/file', bucketName, key)
    print s3Results
