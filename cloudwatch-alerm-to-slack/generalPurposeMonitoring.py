import boto3
import json
import logging
import os
 
from base64 import b64decode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
 
SLACK_CHANNEL = os.environ['slackChannel']
HOOK_URL = os.environ['hookUrl']
 
logger = logging.getLogger()
logger.setLevel(logging.INFO)
 
 
def lambda_handler(event, context):
    logger.info("Event: " + str(event))
    message = json.loads(event['Records'][0]['Sns']['Message'])
    logger.info("Message: " + str(message))
 
    instanceid = message['Trigger']['Dimensions'][0]['value']
    alarm_name = message['AlarmName']
    new_state = message['NewStateValue']
    reason = message['NewStateReason']
    alarm_description = message['AlarmDescription']
 
    slack_message = {
        'channel': SLACK_CHANNEL,
        'text': "<!channel> \nアラーム名: %s\nステータス: %s\nアラーム理由: %s\n説明: %s\nインスタンス: %s" % (alarm_name, new_state, reason, alarm_description, instanceid)
    }
 
    req = Request(HOOK_URL, json.dumps(slack_message).encode('utf-8'))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to %s", slack_message['channel'])
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)
