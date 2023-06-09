import boto3
import logging
from botocore.exceptions import ClientError
import statistics

precio_historial = []


def process_records(records):
    global precio_historial
    for record in records:

        data = record['Data']
        data_str = data.decode('utf-8')
        data_dict = eval(data_str)
        precio = data_dict['close']
        precio_historial.append(precio)

        if len(precio_historial) >= 21:
            precio_historial_ = precio_historial[:-1]
            bollingerInferior = bollingerInf(precio_historial_)
            print("Precio", precio)
            print("Bollinger", bollingerInferior)
            print("\n\n")

            if precio < bollingerInferior:
                alert(precio, bollingerInferior)
            precio_historial = precio_historial[-20:]


def bollingerInf(precio):
    bollinger = None

    if isinstance(precio, list) and len(precio) >= 20:
        mediaMovil = sum(precio[-20:]) / len(precio[-20:])
        stdMovil = statistics.stdev(precio[-20:])
        bollinger = mediaMovil - (2 * stdMovil)

    return bollinger


def alert(precio, bollingerInferior):
    print("# "*29)
    print("#\t\t\t\t\t\t\t#")
    print("#\t\t\t\t\t\t\t#")
    print("#\t\t  ¡¡¡   A L E R T A   !!!\t\t#")
    print("#\t\t\t\t\t\t\t#")
    print("#\t\t\t\t\t\t\t#")
    print("# "*29)
    print("#\t\t\t\t\t\t\t#")
    print("#   -> El precio actual es menor al limite inferior <-  #")
    print("#\t\t\t\t\t\t\t#")
    print("# Precio actual:\t", precio, "\t\t#")
    print("# Franja inferior:\t", bollingerInferior, "\t\t#")
    print("#\t\t\t\t\t\t\t#")
    print("# "*29)


def main():
    stream_name = 'kinesis'

    try:
        kinesis_client = boto3.client('kinesis')

        response = kinesis_client.describe_stream(StreamName=stream_name)
        shard_id = response['StreamDescription']['Shards'][3]['ShardId']

        response = kinesis_client.get_shard_iterator(
            StreamName=stream_name,
            ShardId=shard_id,
            ShardIteratorType='TRIM_HORIZON'
        )
        shard_iterator = response['ShardIterator']

        max_records = 100
        record_count = 0

        while record_count < max_records:
            response = kinesis_client.get_records(
                ShardIterator=shard_iterator,
                Limit=1
            )

            shard_iterator = response['NextShardIterator']
            records = response['Records']
            record_count += len(records)
            process_records(records)
            try:
                print(records[0]["Data"])
            except KeyError:
                pass

    except ClientError:
        logger = logging.getLogger()
        logger.exception("Couldn't get records from stream %s.", stream_name)
        raise


if __name__ == "__main__":
    main()
