import os
import shutil
import base64
import threading
import downloader
import transcript
from pprint import pprint
from flask import Flask, request, Response, jsonify

import importlib
import video_sentiment
import openai
import logging

openai.api_key = "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"


app = Flask(__name__)
# log = logging.getLogger('werkzeug')
# log.disabled = True


URLS = []
LOG_FILE = 'log.txt'
ONLY_RECORD_INSTAGRAM = True
ANALYSIS_DB = {}
STATISTICS = {}


STATISTICS["advice"] = ""



def on_init(truncate_log=True):
    # truncate log.txt
    if truncate_log:
        with open(LOG_FILE, 'w') as f:
            f.write('')
    for filename in os.listdir('videos'):
        if os.path.isfile('videos/' + filename):
            os.remove('videos/' + filename)
        elif os.path.isdir('videos/' + filename):
            shutil.rmtree('videos/' + filename)
    for filename in os.listdir('transcriptions'):
        if os.path.isfile('transcriptions/' + filename):
            os.remove('transcriptions/' + filename)
        elif os.path.isdir('transcriptions/' + filename):
            shutil.rmtree('transcriptions/' + filename)
    for filename in os.listdir('sounds'):
        if os.path.isfile('sounds/' + filename):
            os.remove('sounds/' + filename)
        elif os.path.isdir('sounds/' + filename):
            shutil.rmtree('sounds/' + filename)
    for filename in os.listdir('scrshots_videos'):
        if os.path.isfile('scrshots_videos/' + filename):
            os.remove('scrshots_videos/' + filename)
        elif os.path.isdir('scrshots_videos/' + filename):
            shutil.rmtree('scrshots_videos/' + filename)


def load_urls(filename):
    global ANALYSIS_DB
    urls = []
    sp_lines = []
    with open(filename, 'r') as f:
        sp_lines = f.read().splitlines()
    for line in sp_lines:
        if line.strip() == '': continue
        parsed_line = line.split(' ')
        urls.append(parsed_line[0])
        ANALYSIS_DB[parsed_line[0]] = parsed_line[1:-1]
    pprint(ANALYSIS_DB)
    pprint(urls)
    return urls

def populate_urls():
    global URLS
    URLS = load_urls(LOG_FILE)
    URLS = list(set(URLS))
    return URLS

def add_url(url, filename):
    global URLS
    if url in URLS: return
    with open(filename, 'a') as f:
        f.write(url + '\n')


def get_sentiment_keywords(input_text):
    output = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [{
            "role": "system",
            "content": "You are a text classification model that will process the inputs to classify amongst given tags. Don't output more than the tags themselves. Associate words such as killing, murdering with psychopathy, words such as commiting suicide with depression and such."
        },
            {"role": "user", 
        "content": f"I will give you a text input and I need you to extract tags related to it's psychological affects on people. Some possible tags are normal, psychopathic, offensive, racist, depressive, sad, suicidal, happy, humorous, lovely. If there is no psychological overlap, the only tag has to be normal.\n\nINPUT:{input_text}\nTAG OUTPUT:"}]
    )

    return output.choices[0].message.content.strip().replace(" ", "").split(",")


def get_advice(input_text):
    output = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [{
            "role": "system",
            "content": "You are a psychiatry AI model that processes the inputs to classify amongst given tags and gives advice. Associate words such as killing, murdering with psychopathy, words such as commiting suicide with depression and such. After identifying the tag, give proper advice. Your advice has to be unique and personalized."
        },
            {"role": "user", 
        "content": f"I will give you a text input and I need you to extract tags related to it's psychological affects on people. Some possible tags are normal, psychopathic, offensive, racist, depressive, sad, suicidal, happy, humorous, lovely. If there is no psychological overlap, the only tag has to be normal. Give proper psychological advice as if you were a psycholog using the information you have gathered.\n\nINPUT:{input_text}\nTAG OUTPUT:"}]
    )

    return output.choices[0].message.content.strip()


def download_from_url(url):
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "identity;q=1, *;q=0",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Range": "bytes=0-",
        "Referer": "https://www.instagram.com/",
        "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "video",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    filename = b"videos//"+base64.b64encode((url).encode())+b".mp4"
    downloader.download_video(url, headers, filename)
    speech_sentiment_score = None
    ocr_sentiment_score = None
    ocr_text = None
    transcribed = ""
    try:
        transcribed = transcript.getTranscipt(filename.decode(), (b"sounds//"+base64.b64encode((url).encode())+b".wav").decode())
        with open((b"transcriptions//"+base64.b64encode((url).encode())+b".txt").decode(), 'w') as f:
            f.write(transcribed)
        speech_sentiment_score = video_sentiment.run_sentiment_on_text(transcribed)
    except: pass
    try:
        ocr_sentiment_score, ocr_text = video_sentiment.run_sentiment_on_video(filename.decode())
    except: pass
    try: speech_sentiment_score = speech_sentiment_score['compound']
    except: pass
    keywords = None
    try: keywords = get_sentiment_keywords(transcribed)
    except: pass
    if ocr_text:
        nkeywords = get_sentiment_keywords(ocr_text)
        if keywords:
            keywords += nkeywords
        else: keywords = keywords
    for j in range(5):
        for i in keywords[::]:
            if ":" in i or "\n" in i or " " in i or "." in i or len(i) > 10:
                keywords.remove(i)
    print("KEYWORDS:", keywords)
    # try:
    #     keywords = list(set(keywords)).join(", ")
    # except: pass
    conc = ""
    advice = ""
    if transcribed: conc += transcribed + " "
    if ocr_text: conc += ocr_text
    if len(conc) > 10: advice = get_advice(conc)
    ANALYSIS_DB[url] = (str(speech_sentiment_score), str(ocr_sentiment_score), str(keywords))
    STATISTICS["advice"] = advice.split(":")[-1]
    pprint(ANALYSIS_DB)
    
    print("Speech sentiment score: ", speech_sentiment_score)
    print("OCR sentiment score: ", ocr_sentiment_score)
        

@app.route('/', methods=['GET', 'POST'])
def index():
    data = request.form['curr_url']
    resp = Response("OK", status=200, mimetype='text/plain')
    print(data)
    if ONLY_RECORD_INSTAGRAM and not 'instagram.com' in data: return resp
    if not data in URLS:
        add_url(data, LOG_FILE)
        URLS.append(data)
        download_from_url(data)
        # print(os.path.dirname(os.path.realpath(__file__)))
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        # importlib.reload(downloader)
        # t = threading.Thread(target=download_from_url, args=(data,))
        # t.start()
        # t.join()
    return resp


@app.route('/statistics', methods=['GET'])
def statistics():
    STATISTICS["urls"] = URLS
    STATISTICS["analysis_db"] = ANALYSIS_DB
    resp = jsonify(STATISTICS)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


if __name__ == '__main__':
    on_init(True)
    populate_urls()
    app.run('0.0.0.0', debug=True)