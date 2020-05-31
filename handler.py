import json
import logging
import boto3
import random
import requests
import os

# sqs = boto3.resource('sqs')
SQS_CLIENT = boto3.client('sqs')

def receive_payload(event, context):
    # add a random delay to the msg to avoid concurrent request to pod, because while multile request received, docker is failing.
    rand_delay_second = random.randint(1, 2)

    msg = str(event).replace("'",'"')

    # Create a new message
    # queue = sqs.get_queue_by_name(QueueName='dev-pull-quality-recognition')
    # response = queue.send_message(DelaySeconds=rand_delay_second,MessageBody=msg)
    response = SQS_CLIENT.send_message( QueueUrl=os.getenv('SQS_URL'), MessageBody='body')
    print(f'publish: {msg} the message in sqs \nwith DelaySeconds: {rand_delay_second} and\nstatus is: {response}')

    ##  api call to write in bigquery
    print("CT receive payload writing to bigquery")
    bq_res = requests.post(url='https://quality.dev.data.rea-asia.com/receive-ct-payload', json = event)


    return {
        'statusCode': 200,
        'body': json.dumps('successfully sent to sqs!')
    }



def invoke_qr_api(event, context):
    # r = requests.post(url='https://hooks.slack.com/services/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', json= {"text": "posted a new check"})
    # print("content:", r.content)
    try:
        quality_url = 'https://quality.dev.data.rea-asia.com/trigger-qr'
        # res_qr_model = requests.get(url=quality_url, verify=False, timeout=5)

    except requests.exceptions.Timeout as e:
        print ('request posted to quality-recognition end point.')
        # raise ValueError('A very specific bad thing happened.')

    print("invoke_qr_api, hello_again!")
    return {
        'statusCode': 200,
        'body': json.dumps('successfully triggered quality-recognition api!')
    }
