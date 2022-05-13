import requests
import json


def get_domain_authority(url: str, api_key: str):
    """
    :param url: the url whose domain authority you want to get
    :param api_key: your moz api key
    :return: the domain authority score
    """
    r = requests.post(url='https://lsapi.seomoz.com/v2/url_metrics',
                      data=json.dumps({'targets': [url]}),
                      headers={'Authorization': api_key,
                               'Content-Type': 'application/json'})

    text = json.loads(r.text)
    text = text['results'][0]

    return text['domain_authority']
