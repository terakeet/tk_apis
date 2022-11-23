import requests
import json


def get_url_data(url: str, api_key: str, params: dict = None):
    """
    :param url: the url whose domain authority you want to get
    :param params: a dictionary containing keys(strings) and values(lists) of additional parameters desired
    :param api_key: your moz api key
    :return: the domain authority score
    """

    payload = {
        'targets': [url]
    }

    if params is not None:
        valid_vals = sum(list(map(lambda x: isinstance(x, list), params.values())))

        if valid_vals == len(params):
            payload = {**payload, **params}
            print('valid vals check passed')
            print(payload)
        else:
            raise TypeError("All parameter values must be lists.")

    print(json.dumps(payload))
    r = requests.post(url='https://lsapi.seomoz.com/v2/url_metrics',
                      data=json.dumps(payload),
                      headers={'Authorization': api_key,
                               'Content-Type': 'application/json'})

    text = json.loads(r.text)
    text = text['results'][0]

    return text
