import requests

def send(token, message):

    response = requests.post(
        'https://notify-api.line.me/api/notify',
        headers={
            'Authorization': f'Bearer {token}'
        },
        data={
            'message':message
        }
    )
    return response