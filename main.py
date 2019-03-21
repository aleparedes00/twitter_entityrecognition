import csv

import pandas
import re

from twython import Twython


API_K = "ykzKfaaA5iOKkKpwnYJQOzhy1"
API_S_K = "KTZkmjmKFOFixISkk2wH4OlJfzHS3RIuyYWvocLEK2pQzKqUfX"
ACC_T = "1099709150530097153-Hc38YckiX42QepeOJhjkHVozD3c7RY"
ACC_S_T = "tT5jxIVKOL2WDbWhuH0d8s9iJ0VfI9RcYc8FCcRClaz6I"

"""

Doc CSV 
1 mot par ligne + space + tag
Tags: nom d'entreprise ou 0
1000 tweets en total
ML Model NER
"""


def write_tweet_on_file(my_list):
    with open('/tmp/dataset.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(my_list)


def enterprises_to_dict(entreprises: [])-> {}:
    _dict = {}
    for e in entreprises:
        _e = e.split(' ')
        if len(_e) > 1:
            _dict.update({_e[0]: e})
            _dict.update({_e[1]: e})
        else:
            _dict.update({e: e})
    return _dict


def split_dataset(tweet: str, enterprises: {})-> []:
    list_of_words = tweet.split(' ')
    list_entity = []
    big_list = []
    for word in list_of_words:
        if word in enterprises:
            list_entity = word, enterprises.get(word)
        else:
            if not word or '...' in word:
                continue
            list_entity = word, 'O'
        big_list.append(list_entity)
    write_tweet_on_file(big_list)
    return big_list


def data_cleaning(tweet: str)-> str:
    # removing URLs
    punctuations = "[^\w\s]"
    url_regex = "(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"
    tweet_without_url = re.sub(url_regex, '', tweet)
    tweet_without_p = re.sub(punctuations, '', tweet_without_url)
    # removing emojis (almost all of them)
    emojis = re.compile("["
                       "\U0001F600-\U0001F64F"
                       "\U0001F300-\U0001F5FF"
                       "\U0001F680-\U0001F6FF"
                       "\U0001F1E0-\U0001F1FF"
                       "]+", flags=re.UNICODE)
    clean_tweet = emojis.sub("", tweet_without_p)
    return clean_tweet


def main():
    twitter = Twython(API_K, API_S_K, ACC_T, ACC_S_T)
    enterprises = ['coca cola',
                   'facebook',
                   'microsoft',
                   'bofa_help',
                   'new york times',
                   'jetblue',
                   'mattel',
                   'directline_uk',
                   'tesco',
                   'royalmail',
                   'morrisons']
    enterprises = enterprises_to_dict(enterprises)
    i = 0
    for comp in enterprises.values():
        tweets = twitter.search(q=comp, result_type='mixed', lang='en', count="100")
        for e in tweets['statuses']:
            text = e['text'].lower()
            if comp in text:
                final_tweet = data_cleaning(text)
                i += 1
                split_dataset(final_tweet, enterprises)
    print(i)
    return 1
    # print_dict(enterprises_dict)


if __name__ == '__main__':
    main()

