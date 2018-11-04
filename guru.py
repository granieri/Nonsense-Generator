import flask
from poet import Poet
app = flask.Flask(__name__)

stuff = ''

@app.route('/')
def main_page():
    with open('index.html') as f:
        page = f.read()
        return page

@app.route('/guruify', methods=['POST'])
def guruify():
    target = flask.request.form['data']
    print(target)
    p = Poet()
    target = "https://en.wikipedia.org/wiki/" + target.replace(' ','_')
    p.target(target)
    try:
        poem = p.getpoem()
    except:
        poem = "No wisdom about this"
    ps = poem.split()
    commonbaddies = [
    'and',
    'of',
    'the',
    'as',
    'for'
    'a',
    'to',
    'like',
    'in'
    ]
    for word in ps[::-1]:
        if word in commonbaddies:
            ps = ps[:-1]
        else:
            break
    q = len(ps) // 4
    poem = ' '.join(ps[:q]) + '|' + ' '.join(ps[q:q*2]) + '|' + ' '.join(ps[q*2:q*3]) + '|' + ' '.join(ps[q*3:])
    return poem

# @app.route('/guruify', methods = ['POST'])
# def guruify():
#     target = flask.request.form['target']
#     print("WATERMELONS !!!!!", target)
#     stuff = target
#     print(stuff)
#     return flask.redirect('/')

if __name__ == "__main__":
    app.run()
