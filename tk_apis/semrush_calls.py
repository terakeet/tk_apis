import requests
import re
import pandas as pd


def get_related_keywords(keyword: str, api_key: str):
    """
    :param keyword: the keyword you want to get related keywords for
    :param api_key: your semrush api key
    :return: a dataframe containing all the related keywords and their properties
    """
    r = requests.get(url='https://api.semrush.com/',
                     params={'key': api_key,
                             'type': 'phrase_related',
                             'database': 'us',
                             'phrase': keyword,
                             'export_columns': 'Ph,Nq,Cp,Co,Nr,Td,Rr,Fk,In'})

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


def get_top_related_keyword(keyword: str, api_key: str):
    """
    :param keyword: the keyword you want to get the related keywords for
    :param api_key: your semrush api key
    :return: a Series that is the first row of the dataframe of related keywords
    """
    semrush_result = get_related_keywords(keyword, api_key)
    try:
        return semrush_result.loc[0, ]
    except KeyError:
        return 0


def get_keyword_data(keyword: str, api_key: str):
    """
    :param keyword: the keyword you want to get data for
    :param api_key: your semrush api key
    :return: a dictionary with the information for your keyword
    """
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


def get_search_volume(keyword: str, api_key: str):
    """
    :param keyword: the keyword you want to get the search volume for
    :param api_key: your semrush api key
    :return: the search volume as an int, extracted from the full set of keyword information
    """
    semrush_result = get_keyword_data(keyword, api_key)
    try:
        return semrush_result['Search Volume']
    except KeyError:
        return 0  # this is a big interpretation that an error in SemRush means 0 volume


def get_organic_results(keyword: str, api_key: str, n: int = 10):
    """
    :param keyword: the keyword you want to get the organic results for
    :param api_key: your semrush api key
    :param n: the number of organic results to request
    :return: a dataframe containing the organic results
    """
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


