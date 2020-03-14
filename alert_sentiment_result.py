import boto3
import logging
import os
import json
import urllib


# 
# Lambda requirements:
#   Access to read and write for S3

logger = logging.getLogger()
logger.setLevel(logging.INFO)
s3 = boto3.resource('s3')
s3_client = boto3.client('s3')
ses_client = boto3.client('ses',region_name=os.environ["AWS_REG"])


def lambda_handler(event, context):
    #Get the comprehend output
    bucket_name = event["Records"][0]['s3']['bucket']['name']
    key = urllib.parse.unquote(event["Records"][0]['s3']['object']['key'])
    
    obj = s3_client.get_object(Bucket=bucket_name, Key=key)
        
    logger.info('Invoked for bucket {} key {}'.format(bucket_name, key))
        
    transcript_result = json.loads(obj['Body'].read())
    sentiment = transcript_result["Sentiment"][0]["Sentiment"]

        
    logger.info('Read json sentiment: {}'.format(sentiment))
    
    if (str(sentiment).strip() == 'NEGATIVE') :
        logger.info('Negative sentiment, sending email')
        send_email( str(os.environ["CDN"])+ "/" +str(key).split("/")[-1] )
    else :
        logger.info('Nothing to do')

    return "ok"
    
def send_email(filename):
    
    BODY_HTML = """<html>
<head></head>
<body>
  <h1>We've detected an interaction (phone call) with a predominant negative sentiment</h1>
  <p>Please do the needfull regarding it, full transcript can be found here : {}</p>
</body>
</html>
            """
    
    BODY_TEXT = "bla bla bla"
    
    #Provide the contents of the email.
    response = ses_client.send_email(
        Destination={
                'ToAddresses': [
                    os.environ["RECIPIENT"],
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': os.environ["CHARSET"],
                        'Data': BODY_HTML.format(filename),
                    },
                    'Text': {
                        'Charset': os.environ["CHARSET"],
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': os.environ["CHARSET"],
                    'Data': os.environ["SUBJECT"],
                },
            },
            Source=os.environ["SENDER"])