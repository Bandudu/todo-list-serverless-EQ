import os
import json
import decimalencoder
import boto3

dynamodb = boto3.resource('dynamodb')
translateaws = boto3.client('translate')


def lambda_handler(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    print ("entra en translate")
    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    result['Item']['text'] = translateaws.translate_text(Text=result['Item']['text'], SourceLanguageCode="auto", TargetLanguageCode=event['pathParameters']['language'])['TranslatedText']

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    result['Item']

    return response
