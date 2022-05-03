import requests
import json


def get_domain_authority(url: str, api_key: str):
    r = requests.post(url='https://lsapi.seomoz.com/v2/url_metrics',
                      data=json.dumps({'targets': [url]}),
                      headers={'Authorization': api_key,
                               'Content-Type': 'application/json'})

    text = json.loads(r.text)
    text = text['results'][0]

    return text['domain_authority']
