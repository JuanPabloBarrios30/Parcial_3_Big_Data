import json
from urllib.request import urlopen
import boto3

def f(event, context):
    
    with urlopen("https://totoro.banrep.gov.co/estadisticas-economicas/rest/consultaDatosService/consultaMercadoCambiario") as response:
        body = response.read()
        
    print(body)

    s3 = boto3.resource('s3')
    object = s3.Object('get-info-dolar-jp', 'dolar_timestamp.txt')
    object.put(Body=body)
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }