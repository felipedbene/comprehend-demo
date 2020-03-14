import boto3
from urllib.request import urlopen
import json
import uuid

s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        #print(event)
        transcript_name = event["jobName"]+ ".json"
        tempName = event["fileUri"].split("/")
        fileNameOrig = tempName[-1].rstrip(".wav")
        recType = tempName[-2]
        file_name = recType + "/" + fileNameOrig + ".json" 
        transcript_path = "/tmp/"+transcript_name
        transcripts_bucket = event["transcriptDestination"]
        link = event["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
        f = urlopen(link)
        transcript_str = f.read()
        transcript_obj = json.loads(transcript_str)
        with open(transcript_path, 'w') as outfile:
            json.dump(transcript_obj, outfile)

        response = s3.upload_file(transcript_path, transcripts_bucket, "transcripts/"+file_name)
        return {"Done": True}
    except Exception as e:
        raise e
