import math
from flask import Flask, render_template, url_for, request
import VSM

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])

def index():
  search_result = False

  if request.method == 'POST':
    form = request.form
    search_result = VSM.caller(form['keyword'])

  return render_template('index.html', search_result=search_result)

if __name__ == "__main__":
  app.run(debug=True)