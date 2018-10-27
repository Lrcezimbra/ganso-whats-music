from unittest.mock import MagicMock, patch

from gansowhatsmusic import get_youtube_urls, get_mp3_link, whatsapi_callback


def test_found_youtube_url():
    messages = [
        (
            'Hi!',
            []
        ),
        (
            'Download this songs: https://www.youtube.com/watch?v=b_cNrFAVMTo',
            ['https://www.youtube.com/watch?v=b_cNrFAVMTo'],
        ),
        (
            'https://www.youtube.com/watch?v=b_cNrFAVMTo and',
            ['https://www.youtube.com/watch?v=b_cNrFAVMTo'],
        ),
        (
            'https://www.youtube.com/watch?v=5FHkTfpU678',
            ['https://www.youtube.com/watch?v=5FHkTfpU678']
        ),
    ]
    for message, expected_result in messages:
        result = get_youtube_urls(message)
        assert result == expected_result


@patch('gansowhatsmusic.ganso_whats_music.requests')
def test_get_mp3_link(requests):
    url = 'https://www.youtube.com/watch?v=b_cNrFAVMTo'
    expected_post_url = 'http://www.gansomusic.com.br/download/'
    expected_data = {
        'url': url,
        'download-link': '1',
    }

    get_mp3_link(url)

    requests.post.assert_called_with(expected_post_url, data=expected_data)


def test_reply_youtube_with_mp3():
    """ Reply messages with YouTube link with MP3 links"""
    pass


@patch('gansowhatsmusic.ganso_whats_music.driver')
def test_whatsapi_callback(driver, monkeypatch):
    mp3_url = 'https://mp3url.com/'
    response = MagicMock()
    response.text = mp3_url
    monkeypatch.setattr('requests.post', MagicMock(return_value=response))
    messages = [
        {
            'contact': 'Contact',
            'id': '555199887766-1234567890@g.us',
            'messages': [
                {
                    'message': 'https://www.youtube.com/watch?v=b_cNrFAVMTo',
                    'timestamp': 1509673602
                }
            ]
        }
    ]
    whatsapi_callback(messages)
    driver.send_to_whatsapp_id.assert_called_with(messages[0]['id'], mp3_url)
