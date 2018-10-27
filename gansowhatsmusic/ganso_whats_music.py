import requests
from webwhatsapi import WhatsAPIDriver


def get_youtube_urls(message):
    result = []
    urls = ('youtu.be', 'youtube.com', )

    parts = message.split(' ')
    for part in parts:
        for url in urls:
            if url in part:
                result.append(part)

    return result


def get_mp3_link(url):
    print('Download: ', url)
    ganso_music_url = 'http://www.gansomusic.com.br/download/'
    data = {
        'url': url,
        'download-link': '1',
    }
    response = requests.post(ganso_music_url, data=data)
    if response.status_code == 200:
        print('Download finished')
        return response.text
    else:
        error = 'Error in Download'
        print(error)
        return error


def whatsapi_callback(messages):
    print('messages', messages)
    for message in messages:
        print('message', message)
        for msg in message['messages']:
            print('msg', msg)
            youtube_urls = get_youtube_urls(msg['message'])
            for url in youtube_urls:
                print('url', url)
                driver.send_to_whatsapp_id(message['id'], 'Downloading...')
                mp3 = get_mp3_link(url)
                driver.send_to_whatsapp_id(message['id'], mp3)


driver = WhatsAPIDriver('lrcezimbra')
driver.create_callback(whatsapi_callback)
