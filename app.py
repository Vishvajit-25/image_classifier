from flask import Flask, render_template, request
from script import check
from flask import Flask, request
import time 

class flag:
    def __init__(self):
        self.stop_flag=False

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/echo', methods=['POST','GET'])
def echo():
    text = request.form['text']
    result=check(text,30)
    if result==1:
        text="ISO CERTIFIED"
    elif result==0:
        text="NON ISO CERTIFIED"
    else:
        text="TIMEOUT"
    return render_template('echo.html', text=text)

if __name__ == '__main__':
    app.run(debug=True)

