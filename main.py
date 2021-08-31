from flask import Flask, render_template, request, redirect, url_for
from get_tweets import get_related_tweets
from transformers import pipeline
import plotly.graph_objects as go
import plotly
import json

# Import text classification transformer model
model = pipeline('sentiment-analysis')

# Get tweets and predict their sentiment
def request_results(name):
    tweets = get_related_tweets(name)
    tweets['prediction'] = tweets['tweet_text'].apply(lambda x: model(x)[0]['label'])
    return tweets



app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/', methods=['POST', 'GET'])
def get_data():
    if request.method == 'POST':
        req = request.form['search']
        return redirect(url_for('success', req=req))


@app.route('/success/<req>')
def success(req):
    df_1 = request_results(req)
    fig_1 = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=['Text', 'Prediction'],
                    fill_color='#99202e',
                    align='left',
                    font=dict(color='white')
                ),
                cells=dict(
                    values=[df_1.tweet_text, df_1.prediction],
                    fill_color='#e05a69',
                    align='left',
                    font=dict(color='white')
                )
            )
    ])

    df_2 = df_1.prediction.value_counts()
    fig_2 = go.Figure(
        data=[
            go.Pie(
                labels=df_2.index.tolist(),
                values=df_2.values
            )
        ])
    fig_2.update_traces(
        marker=dict(
            colors=['royalblue', 'darkblue']
        ))

    tableJSON = json.dumps(fig_1, cls=plotly.utils.PlotlyJSONEncoder)
    pieJSON = json.dumps(fig_2, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('home.html', tableJSON = tableJSON, pieJSON=pieJSON)



if __name__ == '__main__' :
    app.run(debug=True)