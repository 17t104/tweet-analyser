from flask import *
from flask import jsonify
from flask_cors import CORS
from sentiment import call_predict_function
import requests

app=Flask(__name__)
CORS(app)
jinja_options = app.jinja_options.copy()

jinja_options.update(dict(
    block_start_string='<%',
    block_end_string='%>',
    variable_start_string='%%',
    variable_end_string='%%',
    comment_start_string='<#',
    comment_end_string='#>'
))
result_dict=dict()
app.jinja_options = jinja_options

@app.route('/')
def home():
    return render_template('tweet.html')
@app.errorhandler(404) 
def not_found(e):
    return render_template("error.html") 
@app.route('/about')
def about():
    return render_template("about.html")
@app.route('/result',methods=['GET','POST'])
def check_tweet():
    if request.method=='POST':
        tweet=request.form['tweet']
        result=call_predict_function(tweet)
        datas=dict()
        datas={'tweet':tweet,'label':result["label"],'score':result["score"]}
        return render_template('new.html',data=json.dumps(datas))
        
    else:    
        return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
