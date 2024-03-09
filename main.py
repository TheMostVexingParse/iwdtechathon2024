import base64
import threading
import downloader
import transcript
from flask import Flask, request, Response
app = Flask(__name__)



URLS = []
LOG_FILE = 'log.txt'
ONLY_RECORD_INSTAGRAM = True



def load_urls(filename):
    with open(filename, 'r') as f:
        return f.read().splitlines()

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
    transcribed = transcript.getTranscipt(filename.decode(), (b"sounds//"+base64.b64encode((url).encode())+b".wav").decode())
    # Save to transcriptions folder
    with open((b"transcriptions//"+base64.b64encode((url).encode())+b".txt").decode(), 'w') as f:
        f.write(transcribed)
        

@app.route('/', methods=['GET', 'POST'])
def index():
    data = request.form['curr_url']
    resp = Response("OK", status=200, mimetype='text/plain')
    print(data)
    if ONLY_RECORD_INSTAGRAM and not 'instagram.com' in data: return resp
    if not data in URLS:
        add_url(data, LOG_FILE)
        URLS.append(data)
        t = threading.Thread(target=download_from_url, args=(data,))
        t.start()
        t.join()
    return resp


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)