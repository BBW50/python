import urllib.request
import urllib.parse
import logging

# Chatworkの設定
CHATWORK_ROOM_ID = 'your-room-id'
CHATWORK_API_TOKEN = 'your-chatwork-api-key'

def send_chatwork(message):
    url = f'https://api.chatwork.com/v2/rooms/{CHATWORK_ROOM_ID}/messages'
    headers = {'X-ChatWorkToken': CHATWORK_API_TOKEN, 'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'body': message}
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req) as res:
            response = res.read().decode("utf-8")
            logger.info(f'Message sent successfully: {response}')
    except urllib.error.HTTPError as e:
        logger.error(f'Failed to send message: HTTPError: StatusCode: {e.code}, Reason: {e.reason}')

def lambda_handler(event, context):
    message = "Hello, Chatwork!" 
    send_chatwork(message)
    return {'statusCode': 200, 'body': 'Message sent successfully!'}


