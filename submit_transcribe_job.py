import boto3
import json
import datetime
client = boto3.client('transcribe')
import uuid

def lambda_handler(event, context):
    #print(event)
    # TODO implement
    try:
        job_name = event["jobName"]+"-"+uuid.uuid4().hex #RANDOMNESS
        media_format = event["mediaFormat"]
        file_uri = event["fileUri"]
        language_code = "es-US"

        response = client.start_transcription_job(
            TranscriptionJobName=job_name,
            LanguageCode=language_code,
            MediaFormat=media_format,
            Media={
                'MediaFileUri': file_uri
            }
        )
        # BELOW IS THE CODE TO FIX SERIALIZATION ON DATETIME OBJECTS
        if "CreationTime" in response["TranscriptionJob"]:
            response["TranscriptionJob"]["CreationTime"] = str(response["TranscriptionJob"]["CreationTime"])
        if "CompletionTime" in response["TranscriptionJob"]:
            response["TranscriptionJob"]["CompletionTime"] = str(response["TranscriptionJob"]["CompletionTime"])
        return response["TranscriptionJob"]
    except Exception as e:
        raise(e)


def my_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
