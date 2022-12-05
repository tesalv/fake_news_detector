#Implement all this concept by machine learning with flask

from flask import Flask, escape, request, render_template
from scripts.ready_input_function import get_page_clean_text
from scripts.sentiment_analyses import get_topic
from scripts.sentiment_analyses import get_sentiment

from tensorflow import keras
import tensorflow_hub as hub
import tensorflow_text as text
import tensorflow as tf
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#vector = pickle.load(open("vectorizer.pkl", 'rb'))
model = keras.models.load_model('model_v1.h5',custom_objects={'KerasLayer': hub.KerasLayer})

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == "POST":
        news = str(request.form['news'])
        news_to_predict=get_page_clean_text(news)

        predict = model.predict(pd.DataFrame([news_to_predict]))
        print(predict)
        if predict>=0.5:
            #print(f"This news are predicted to be Fake with a confidence level of {round(predict*100)}% ")
            #return render_template("prediction.html", prediction_text=f"This news are predicted to be Fake with a confidence level of {(predict[0][0]*100,0)} % \n \n {get_topic(news_to_predict)}  \n \n {get_sentiment(news_to_predict)} ")
            return render_template("prediction-Copy.html", prediction_text=f"This news are predicted to be Fake with a confidence level of {(round(predict[0][0]*100-50),0)} %" , prediction_text1=f"{get_topic(news_to_predict)}", prediction_text2=f"{get_sentiment(news_to_predict)}")
        else:
            #print(f"This news are predicted to be True with a confidence level of {1 - round(predict*100)}% ")
            #return render_template("prediction.html", prediction_text=f"This news are predicted to be True with a confidence level of {(predict[0][0]*100,0)} % \n \n {get_topic(news_to_predict)} \n \n {get_sentiment(news_to_predict)}")
            return render_template("prediction-Copy.html", prediction_text=f"This news are predicted to be True with a confidence level of {(round(predict[0][0]*100),0)} %",prediction_text1=f"{get_topic(news_to_predict)}", prediction_text2=f"{get_sentiment(news_to_predict)}")
        #return render_template("prediction.html", prediction_text="News headline is -> {}".format(predict))


    else:
        return render_template("prediction-Copy.html")


if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=6006)
