#Implement all this concept by machine learning with flask

from flask import Flask, escape, request, render_template, redirect, url_for, send_from_directory
from scripts.ready_input_function import get_page_clean_text
from scripts.ready_input_function import get_raw_clean_text
from scripts.sentiment_analyses import get_topic
from scripts.sentiment_analyses import get_sentiment
from scripts.news_translation import get_translation

from tensorflow import keras
import tensorflow_hub as hub
import tensorflow_text as text
import tensorflow as tf
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import pytesseract
from PIL import Image

from werkzeug.utils import secure_filename
import os


# UTILITY FUNCCTIONS AND MODELS 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#vector = pickle.load(open("vectorizer.pkl", 'rb'))
model = keras.models.load_model('model_v1.h5',custom_objects={'KerasLayer': hub.KerasLayer})
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"



# SETINGS 
UPLOAD_FOLDER = r'static\uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


#  FLASK APP STARTS HERE 
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def main():
    return render_template("index.html")

# @app.route('/home', methods=['GET', 'POST'])
# def selection():
#     return render_template("home.html")
@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/choose_format', methods=['GET', 'POST'])
def test():
    if request.method == "POST":
        news_format = request.form['news_format']
        if news_format=='url':
            return redirect('/url')
        elif news_format=='text':
            return redirect('/text')
        else:
            return redirect('/image')
    else:
        return render_template("choose_format.html")



# text route is this one 
@app.route('/url', methods=['GET', 'POST'])
def prediction_url():
    if request.method == "POST":
        print("I'm here!!")
        lang = request.form['language']
        if lang=='eng':
            print(lang)
            news = str(request.form['news'])
            news_to_predict=get_page_clean_text(news)
            predict = model.predict(pd.DataFrame([news_to_predict]))
            print(lang)
            print(news_to_predict)
            print(predict)
            if predict>=0.5:
                confidence=(predict[0][0]*100-50)*2
                return render_template("prediction.html", prediction_text_part1="Prediction|| ",prediction_text_part2= "Fake News", prediction_text_part3=f" with a confidence level of  {round(confidence,0)} %" , prediction_text1=f"{get_topic(news_to_predict)}", prediction_text2=f"{get_sentiment(news_to_predict)}")
            else:
                confidence=(50-predict[0][0]*100)*2
                return render_template("prediction.html", prediction_text_part1="Prediction|| ",prediction_text_part2= "Reliable News", prediction_text_part3=f" with a confidence level of  {round(confidence,0)} %" , prediction_text1=f"{get_topic(news_to_predict)}", prediction_text2=f"{get_sentiment(news_to_predict)}")
        elif lang=='por':
            print(lang)
            pt_news = str(request.form['news'])
            pt_news=get_page_clean_text(pt_news)
            news_to_predict=get_translation(pt_news)
            predict = model.predict(pd.DataFrame([news_to_predict]))
            print(lang)
            print(news_to_predict)
            print(predict)
            if predict>=0.5:
                confidence=(predict[0][0]*100-50)*2
                return render_template("prediction.html", prediction_text_part1="Prediction|| ",prediction_text_part2= "Fake News", prediction_text_part3=f" with a confidence level of  {round(confidence,0)} %" , prediction_text1=f"{get_topic(news_to_predict)}", prediction_text2=f"{get_sentiment(news_to_predict)}")
            else:
                confidence=(50-predict[0][0]*100)*2
                return render_template("prediction.html", prediction_text_part1="Prediction|| ",prediction_text_part2= "Reliable News", prediction_text_part3=f" with a confidence level of  {round(confidence,0)} %" , prediction_text1=f"{get_topic(news_to_predict)}", prediction_text2=f"{get_sentiment(news_to_predict)}")


    else:
        return render_template("prediction.html")

@app.route('/text', methods=['GET', 'POST'])
def prediction_text():
    if request.method == "POST":
        print("I'm here!!")
        lang = request.form['language']
        if lang=='eng':
            print(lang)
            news = str(request.form['news'])
            news_to_predict=get_raw_clean_text(news)
            predict = model.predict(pd.DataFrame([news_to_predict]))
            print(lang)
            print(news_to_predict)
            print(predict)
            if predict>=0.5:
                confidence=(predict[0][0]*100-50)*2
                return render_template("prediction.html", prediction_text_part1="Prediction|| ",prediction_text_part2= "Fake News", prediction_text_part3=f" with a confidence level of  {round(confidence,0)} %" , prediction_text1=f"{get_topic(news_to_predict)}", prediction_text2=f"{get_sentiment(news_to_predict)}")
            else:
                confidence=(50-predict[0][0]*100)*2
                return render_template("prediction.html", prediction_text_part1="Prediction|| ",prediction_text_part2= "Reliable News", prediction_text_part3=f" with a confidence level of  {round(confidence,0)} %" , prediction_text1=f"{get_topic(news_to_predict)}", prediction_text2=f"{get_sentiment(news_to_predict)}")
        elif lang=='por':
            print(lang)
            pt_news = str(request.form['news'])
            pt_news=get_raw_clean_text(pt_news)
            news_to_predict=get_translation(pt_news)
            predict = model.predict(pd.DataFrame([news_to_predict]))
            print(lang)
            print(news_to_predict)
            print(predict)
            if predict>=0.5:
                confidence=(predict[0][0]*100-50)*2
                return render_template("prediction.html", prediction_text_part1="Prediction|| ",prediction_text_part2= "Fake News", prediction_text_part3=f" with a confidence level of  {round(confidence,0)} %" , prediction_text1=f"{get_topic(news_to_predict)}", prediction_text2=f"{get_sentiment(news_to_predict)}")
            else:
                confidence=(50-predict[0][0]*100)*2
                return render_template("prediction.html", prediction_text_part1="Prediction|| ",prediction_text_part2= "Reliable News", prediction_text_part3=f" with a confidence level of  {round(confidence,0)} %" , prediction_text1=f"{get_topic(news_to_predict)}", prediction_text2=f"{get_sentiment(news_to_predict)}")


    else:
        return render_template("prediction.html")



@app.route('/image', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        global lang
        lang = request.form['language']
        # if user does not select file, browser also
        # submit an empty part without filename
        print(file)
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            predict, news_to_predict = uploaded_file(filename)

            if predict>=0.5:
                confidence=(predict[0][0]*100-50)*2
                return render_template("image.html", prediction_text_part1="Prediction|| ",prediction_text_part2= "Fake News", prediction_text_part3=f" with a confidence level of  {round(confidence,0)} %" , prediction_text1=f"{get_topic(news_to_predict)}", prediction_text2=f"{get_sentiment(news_to_predict)}")
            else:
                confidence=(50-predict[0][0]*100)*2
                return render_template("image.html", prediction_text_part1="Prediction|| ",prediction_text_part2= "Reliable News", prediction_text_part3=f" with a confidence level of  {round(confidence,0)} %" , prediction_text1=f"{get_topic(news_to_predict)}", prediction_text2=f"{get_sentiment(news_to_predict)}")
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
    else:
        return render_template('image.html')

# @app.route('/uploads/<filename>')
def uploaded_file(filename):
    print('HELLO')
    global lang
    img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    text = pytesseract.image_to_string(img,lang=lang)
    #lang = request.form['language']
    print(text)
    print('language', lang)
    if lang=='eng':
        print(lang)
        news = text
        news_to_predict=get_raw_clean_text(news)
        predict = model.predict(pd.DataFrame([news_to_predict]))
        print(lang)
        print(predict)
        return predict, news_to_predict
        
    elif lang=='por':
        print(lang)
        pt_news = text
        pt_news=get_raw_clean_text(pt_news)
        news_to_predict=get_translation(pt_news)
        predict = model.predict(pd.DataFrame([news_to_predict]))
        print(lang)
        print(news_to_predict)
        print(predict)
        return predict, news_to_predict





if __name__ == '__main__':
    # Setup Tesseract executable path
    app.run(host= '0.0.0.0', port=5000)




