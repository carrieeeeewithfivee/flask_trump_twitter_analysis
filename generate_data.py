# slight configuration can get different results for needed data
from pathlib import Path
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os,glob
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from collections import Counter  # to get words-frequency
import json  # to convert python dictionary to string format
import contractions
import re
import time
from datetime import datetime
import itertools
import statistics

#path to data
path = Path().absolute()
datapath = str(path).replace('\\', '/')+'/trump_tweet_data_archive/'

# get all (noun) words, most common first 1000 for every year
def wordcloud():
    word_list = []
    is_noun = lambda pos: pos[:2] == 'NN'
    for filename in sorted(glob.glob(os.path.join(datapath, '*.json'))):
        text = ""
        with open(filename) as json_file:
            data = json.load(json_file)
            for tweet in data:
                text = text + " " + tweet['text']

        #remove http links
        text = contractions.fix(text)
        text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",text).split())
        words = re.sub("[^\w]", " ",  text).split()
        stop_words = set(stopwords.words('english'))
        #stop_words.update(['President','Trump','Donald','and','want','need','they','This','Trump2016'])

        words = [word.capitalize() for word in words if word not in stop_words and len(word) > 3]
        words = [word for (word, pos) in nltk.pos_tag(words) if is_noun(pos)] 
        word_list.extend(words)

        words_freq = Counter(word_list)
        words_freq = words_freq.most_common(1000)
        words_json = [{'text': i[0], 'weight': i[1]} for i in words_freq]
        name = os.path.basename(filename)
        with open('word_frequency.json', 'w') as outfile:
            json.dump(words_json, outfile)

def extract_key(v):
    return v[0]

#setiment analy by year
def setiment():
    analyzer = SentimentIntensityAnalyzer()
    for filename in sorted(glob.glob(os.path.join(datapath, '*.json'))):
        senti = []
        with open(filename) as json_file:
            data = json.load(json_file)
            dates = []
            for tweet in data:
                #get time
                ts = time.strftime('%Y-%m-%d', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
                #get text score
                vs = analyzer.polarity_scores(tweet['text'])
                senti.append([ts,vs['compound']])
        senti.sort(key=lambda x:x[0])
        #merge days
        result = [[k,statistics.mean(x[1] for x in g)] for k, g in itertools.groupby(senti, extract_key)]
        words_json = [{'time': i[0], 'weight': i[1]} for i in result]
        name = os.path.basename(filename)
        with open('sen_' + name, 'w') as outfile:
            json.dump(words_json, outfile)

def normalize(value, min_num, max_num):
    normalized_x = 2*(value-min_num)/(max_num-min_num) -1
    return normalized_x

#get retweet and favorite count
def fc_rc():
for filename in sorted(glob.glob(os.path.join(datapath, '*.json'))):
    with open(filename) as json_file:
        rc_list = []
        fc_list = []
        rc_num = []
        fc_num = []
        data = json.load(json_file)
        for tweet in data:
            #get time
            ts = time.strftime('%Y-%m-%d', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
            #get retweet count
            rc = tweet['retweet_count']
            #get favorite count
            fc = tweet['favorite_count']
            fc_list.append([ts,int(fc)])
            rc_list.append([ts,int(rc)])

        rc_list.sort(key=lambda x:x[0])
        fc_list.sort(key=lambda x:x[0])
        #merge months
        rc_result = [[k,statistics.mean(x[1] for x in g)] for k, g in itertools.groupby(rc_list, extract_key)]
        fc_result = [[k,statistics.mean(x[1] for x in g)] for k, g in itertools.groupby(fc_list, extract_key)]

        for num in rc_result:
            rc_num.append(num[1])
        for num in fc_result:
            fc_num.append(num[1])

    #normalize data
    rc_max_num = max(rc_num)
    rc_min_num = min(rc_num)
    rc_result = [[i[0],normalize(i[1],rc_min_num,rc_max_num)] for i in rc_result]

    fc_max_num = max(fc_num)
    fc_min_num = min(fc_num)
    fc_result = [[i[0],normalize(i[1],fc_min_num,fc_max_num)] for i in fc_result]

    rc_words_json = [{'time': i[0], 'weight': i[1]} for i in rc_result]
    fc_words_json = [{'time': i[0], 'weight': i[1]} for i in fc_result]

    name = os.path.basename(filename)
    with open('rc_' + name, 'w') as outfile:
        json.dump(rc_words_json, outfile)
    with open('fc_' + name, 'w') as outfile:
        json.dump(fc_words_json, outfile)

if __name__ == '__main__':
    fc_rc()