from flask import Flask, render_template, request, jsonify
import json, re
import collections, random
from datetime import datetime

app = Flask(__name__)

class Data:
    def __init__(self, jobid, title, category, deadline, desc):
        self.title = title
        self.title = title
        self.category = category
        self.deadline = deadline
        self.desc = desc
        self.year = [datetime.strptime(a, '%B %d, %Y').year for a in deadline]


def readjson(filename):
    d = []
    with open(filename) as f:
        for line in f:
            d.append(json.loads(line))
    jobid = [a['jobid'] for a in d]
    title = [a['title'] for a in d]
    category = [a['category'] for a in d]
    deadline = [a['deadline'] for a in d]
    desc = [a['description'] for a in d]
    return Data(jobid, title, category, deadline, desc)

data = readjson('all.json')

@app.route('/')
def index():
    return render_template('index.html',)

r = lambda: random.randint(0, 255)
getRandomColor = lambda : '#%02X%02X%02X' % (r(),r(),r())

@app.route('/search')
def search():
# random.choice(('dust', 'MHD', 'princeton'))
    keyword = request.args.get('keyword', '')
    if keyword:
        result = []
        for i, desc in enumerate(data.desc):
            m = re.search(r'(%s)' % (keyword), desc, re.IGNORECASE)
            if m is not None:
                result.append((data.year[i], data.title[i]))
        years = [row[0] for row in result]
        yearCount = collections.Counter(years)
        color = getRandomColor()
        d = json.dumps(dict(
            labels=list(yearCount.keys()),
            datasets=[dict(
                label=keyword,
                strokeColor=color,
                pointColor=color,
                pointStrokeColor="#fff",
                pointHighlightFill="#fff",
                pointHighlightStroke=color,
                data=list(yearCount.values()),
                listing=result)]
            ))
        return d


if __name__ == '__main__':
    app.debug = True
    app.run()
