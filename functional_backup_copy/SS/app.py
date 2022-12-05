#Implement all this concept by machine learning with flask

from flask import Flask, escape, request, render_template, redirect, url_for, send_from_directory
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

@app.route('/home', methods=['GET', 'POST'])
def selection():
    return render_template("home.html")

# text route is this one 
@app.route('/text', methods=['GET', 'POST'])
def prediction():
    if request.method == "POST":

        lang = request.form['language']

        news = str(request.form['news'])
        news_to_predict=get_page_clean_text(news)
        predict = model.predict(pd.DataFrame([news_to_predict]))
        print(predict)
        if predict>=0.5:
            confidence=(predict[0][0]*100-50)*2
            return render_template("prediction.html", prediction_text=f"This news are predicted to be Fake with a confidence level of {round(confidence,0)} %" , prediction_text1=f"{get_topic(news_to_predict)}", prediction_text2=f"{get_sentiment(news_to_predict)}")
        else:
            confidence=(50-predict[0][0]*100)*2
            return render_template("prediction.html", prediction_text=f"This news are predicted to be True with a confidence level of {round(confidence,0)} %",prediction_text1=f"{get_topic(news_to_predict)}", prediction_text2=f"{get_sentiment(news_to_predict)}")

    else:
        return render_template("prediction.html")



@app.route('/image', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        print(file)
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    else:
        return render_template('image.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    print('HELLO')
    img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    text = pytesseract.image_to_string(img)
    return render_template('image.html', text=text)


if __name__ == '__main__':
    # Setup Tesseract executable path
    app.run(host= '0.0.0.0', port=4342)




# def dropdown_input():
#     input_form = [' ','url', 'text', 'image']
#     lang_choice = [' ', 'eng', 'por']
#     return render_template('prediction.html', input_form=input_form,lang_choice=lang_choice)

# def all_functions():
   
#     input_form = [' ','url', 'text', 'image']
#     lang_choice = [' ', 'eng', 'por']
#         #return render_template('prediction.html', input_form=input_form,lang_choice=lang_choice)
#     # else:
#     #     input_form = [' ', 'url', 'text', 'image']
#     #     lang_choice = [' ' ,'eng', 'por']
#     #     return render_template('prediction.html', input_form=input_form,lang_choice=lang_choice)

#     if input_form=='url':
#         news = str(request.form['news'])
#         news_to_predict=get_page_clean_text(news)

#         predict = model.predict(pd.DataFrame([news_to_predict]))
#         print(predict)
#         if predict>=0.5:
#             return render_template("prediction.html", prediction_text=f"This news are predicted to be Fake with a confidence level of {(round(predict[0][0]*100-50),0)} %" , prediction_text1=f"{get_topic(news_to_predict)}", prediction_text2=f"{get_sentiment(news_to_predict)}",input_form=input_form,lang_choice=lang_choice)
#         else:
#             return render_template("prediction.html", prediction_text=f"This news are predicted to be True with a confidence level of {(round(predict[0][0]*100),0)} %",prediction_text1=f"{get_topic(news_to_predict)}", prediction_text2=f"{get_sentiment(news_to_predict)}",input_form=input_form,lang_choice=lang_choice)
    
#     elif input_form=='text':
#         news = str(request.form['news'])
#         predict = model.predict(pd.DataFrame([news]))
#         print(predict)
#         if predict>=0.5:
#             return render_template("prediction.html", prediction_text=f"This news are predicted to be Fake with a confidence level of {(round(predict[0][0]*100-50),0)} %" , prediction_text1=f"{get_topic(news_to_predict)}", prediction_text2=f"{get_sentiment(news_to_predict)}",input_form=input_form,lang_choice=lang_choice)
#         else:
#             return render_template("prediction.html", prediction_text=f"This news are predicted to be True with a confidence level of {(round(predict[0][0]*100),0)} %",prediction_text1=f"{get_topic(news_to_predict)}", prediction_text2=f"{get_sentiment(news_to_predict)}",input_form=input_form,lang_choice=lang_choice)

#     elif input_form=='image':
#         image = request.files['ocrImage']
#         text = ''
#         filename = secure_filename(image.filename)
#         print(filename)
#         image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         text = pytesseract.image_to_string(img)
#         f = open(os.path.join(app.config['UPLOAD_FOLDER'], filename)+'.txt','w')
#         f.write(text)
#         f.close()
#         return render_template('prediction.html',text=text)
#     # else:
#     #     input_form = ['url', 'text', 'image']
#     #     lang_choice = ['eng', 'por']
#     #     return render_template("prediction.html",input_form=input_form,lang_choice=lang_choice)









# def submitImage():
#     image = request.files['ocrImage']
#     text = ''
#     filename = secure_filename(image.filename)
#     print(filename)
#     image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#     img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#     text = pytesseract.image_to_string(img)
#     f = open(os.path.join(app.config['UPLOAD_FOLDER'], filename)+'.txt','w')
#     f.write(text)
#     f.close()

#     return render_template('prediction.html',text=text)


