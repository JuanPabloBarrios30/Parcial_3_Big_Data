import boto3
import json
from datetime import datetime


def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('get-info-dolar-jp')
    obj = bucket.Object('dolar_timestamp.txt')
    body = obj.get()['Body'].read()
    print(json.loads(body))
    archivo = json.loads(body)

    csv = 'Fecha,Dolar\n'

    for i in range(0, len(archivo)):

        timestap = int(archivo[i][0])/1000
        dt_object = datetime.fromtimestamp(timestap)
        csv += str(dt_object)
        csv += ','
        csv += str(archivo[i][1])
        csv += '\n'

    print(csv)

    s3 = boto3.resource('s3')
    object = s3.Object('transform-dolar-jp', 'dolar_timestamp.csv')
    object.put(Body=csv)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
