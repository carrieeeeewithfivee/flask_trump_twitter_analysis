from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__, template_folder='templates')
import pickle
import nltk
nltk.download('averaged_perceptron_tagger')
import json

#parameters for word cloud
stop_words = ['President','Trump','Donald','and','want','need','they','This']
global stage
stage = 0

#parameters for both sentiment and word cloud
global year
year = 0 

#parameters for sentiment analysis
global values #sentiment values 
values = []
global labels
labels = []
global legend
legend = []

global fc_values #favorite counts
fc_values = []
global fc_legend

global rc_values #retweet counts
rc_values = []
global rc_legend

@app.route('/')
def home_page():
    global values
    global labels
    global legend
    global fc_values
    global fc_legend
    global rc_values
    global rc_legend
    rc_values = []
    fc_values = []
    values = []
    labels = []
    try:
        data_file = "static/sen_data/sen_condensed_all.json"
        legend = 'All Years Sentiment Analysis'
        global year
        if year!=0:
            for i in range(2009, 2021):
                if year==i:
                    data_file = "static/sen_data/sen_condensed_" + str(year) + ".json"
                    legend = str(year) + ' Sentiment Analysis'
        with open(data_file) as json_file:
            sen_json = json.load(json_file)
            for sen in sen_json[:]:
                labels.append(str(sen['time']))
                values.append(float(sen['weight']))
    except Exception as e:
        print("Error : "+ e)
    
    try:
        data_file = "static/fc_data/fc_condensed_all.json"
        fc_legend = 'All Years Favorite Count'
        if year!=0:
            for i in range(2009, 2021):
                if year==i:
                    data_file = "static/fc_data/fc_condensed_" + str(year) + ".json"
                    fc_legend = str(year) + ' Favorite Count'
        with open(data_file) as json_file:
            fc_json = json.load(json_file)
            for fc in fc_json[:]:
                fc_values.append(float(fc['weight']))
    except Exception as e:
        print("Error : "+ e)
    
    try:
        data_file = "static/rc_data/rc_condensed_all.json"
        rc_legend = 'All Years Retweet Count'
        if year!=0:
            for i in range(2009, 2021):
                if year==i:
                    data_file = "static/rc_data/rc_condensed_" + str(year) + ".json"
                    rc_legend = str(year) + ' Retweet Count'
        with open(data_file) as json_file:
            rc_json = json.load(json_file)
            for rc in rc_json[:]:
                rc_values.append(float(rc['weight']))
    except Exception as e:
        print("Error : "+ e)
    return render_template('twitter.html', stop_words = stop_words, values=values, labels=labels, legend=legend, rc_values=rc_values, rc_legend=rc_legend,fc_values=fc_values, fc_legend=fc_legend)

@app.route('/reset')
def reset():
    global stage
    stage = 0
    try:
        stop_words.pop(len(stop_words)-1)
    except Exception as e:
        pass
    print(stop_words)
    return redirect('/')

@app.route('/noun')
def noun():
    global stage
    stage = 1
    return redirect('/')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form.get('stop_words', None)
    stop_words.append(text)
    return render_template('twitter.html', stop_words = stop_words)

@app.route('/twitter_word_cloud', methods=['GET']) #all
def twitter_word_cloud():
    try:
        global year
        data_file = "static/wordcloud_data/fre_condensed_all.json"
        if year!=0:
            for i in range(2009, 2021):
                if year==i:
                    data_file = "static/wordcloud_data/fre_condensed_" + str(year) + ".json"
        print(data_file)
        with open(data_file) as json_file:
            words_json = json.load(json_file)
            for words in words_json[:]:
                global stage
                if stage == 1:
                    if (not nltk.pos_tag([words['text']])[0][1].startswith('NNP') and words['text']!="Coronavirus"):
                        words_json.remove(words)
                    elif words['text'] in stop_words:
                        words_json.remove(words)
                else:
                    if words['text'] in stop_words:
                        words_json.remove(words)
        return json.dumps(words_json)
    except Exception as e:
        return '[]'

#change year
@app.route('/all')
def all():
    global year
    year = 0
    return redirect('/')
@app.route('/2020')
def _2020():
    global year
    year = 2020
    return redirect('/')
@app.route('/2019')
def _2019():
    global year
    year = 2019
    return redirect('/')
@app.route('/2018')
def _2018():
    global year
    year = 2018
    return redirect('/')
@app.route('/2017')
def _2017():
    global year
    year = 2017
    return redirect('/')
@app.route('/2016')
def _2016():
    global year
    year = 2016
    return redirect('/')
@app.route('/2015')
def _2015():
    global year
    year = 2015
    return redirect('/')
@app.route('/2014')
def _2014():
    global year
    year = 2014
    return redirect('/')
@app.route('/2013')
def _2013():
    global year
    year = 2013
    return redirect('/')
@app.route('/2012')
def _2012():
    global year
    year = 2012
    return redirect('/')
@app.route('/2011')
def _2011():
    global year
    year = 2011
    return redirect('/')
@app.route('/2010')
def _2010():
    global year
    year = 2010
    return redirect('/')
@app.route('/2009')
def _2009():
    global year
    year = 2009
    return redirect('/')

if __name__ == '__main__':
    #app.debug = True
    app.run()