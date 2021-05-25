import os
import json

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')

def translate(event, context):

    # get language from request
    language=event['pathParameters']['lang']
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    databaseItem = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    
        
    # get translate service
    translateaws = boto3.client(service_name='translate', region_name='us-east-1')
    
    translated_text = translateaws.translate_text(Text=databaseItem['Item']['text'], 
                SourceLanguageCode="auto", TargetLanguageCode=language)
    
    # translate text
    databaseItem['Item']['text']=translated_text.get('TranslatedText')

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(databaseItem['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response