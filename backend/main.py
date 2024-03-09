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


@app.route('/', methods=['GET', 'POST'])
def index():
    data = request.form['curr_url']
    resp = Response("OK", status=200, mimetype='text/plain')
    print(data)
    if ONLY_RECORD_INSTAGRAM and not 'instagram.com' in data: return resp
    if not data in URLS:
        add_url(data, LOG_FILE)
        URLS.append(data)
    return resp


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)