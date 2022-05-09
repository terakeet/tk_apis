import requests
import re
import pandas as pd


def get_keyword_data(keyword: str, api_key: str):
    r = requests.get(url='https://api.semrush.com/',
                     params={'key': api_key,
                             'type': 'phrase_this',
                             'database': 'us',
                             'phrase': keyword})

    temp = r.text
    if re.search('^ERROR', temp):
        temp = temp.split(' :: ')
        keys = [temp[0]]
        values = [temp[1]]
    else:
        temp = temp.splitlines()

        keys = temp[0].split(';')
        values = temp[1].split(';')

    res = {keys[i]: values[i] for i in range(len(keys))}
    return res


def get_organic_results(keyword: str, api_key: str, n: int = 10):
    r = requests.get(url='https://api.semrush.com/',
                     params={'key': api_key,
                             'type': 'phrase_organic',
                             'database': 'us',
                             'columns': 'Dn,Ur',
                             'display_limit': n,
                             'phrase': keyword})
    temp = r.text
    if re.search('^ERROR', temp):
        temp = temp.split(' :: ')
        keys = [temp[0]]
        values = [temp[1]]
    else:
        temp = temp.splitlines()

        keys = temp[0].split(';')
        values = []
        for i in range(1, len(temp)):
            values.append(temp[i].split(';'))

    out = pd.DataFrame(data=values,
                           columns=keys)

    return out


def get_search_volume(keyword: str, api_key: str):
    semrush_result = get_keyword_data(keyword, api_key)
    try:
        return semrush_result['Search Volume']
    except KeyError:
        return 0  # this is a big interpretation that an error in SemRush means 0 volume


