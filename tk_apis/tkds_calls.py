import requests


def get_url_category(url, title, snippet, api_key):
    payload = '"' + str(url).replace('"', r'\"') + '","' + \
              str(title).replace('"', r'\"') + '","' + \
              str(snippet).replace('"', r'\"') + '"'

    r = requests.post(url='https://mvzktxazpd.execute-api.us-east-1.amazonaws.com/prod/classifiers/url/v3',
                      data=payload,
                      headers={'Content-Type': 'text/csv',
                               'x-api-key': api_key})

    text = r.text.split(',')
    return text[0]


