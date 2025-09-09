import nltk
from flask import Flask, render_template, request
import pandas as pd
import sklearn
import itertools
import numpy as np
import seaborn as sb
import re
import nltk
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from matplotlib import pyplot as plt
from sklearn.linear_model import PassiveAggressiveClassifier
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from dotenv import load_dotenv
import os 

load_dotenv()

WEB3FORM_KEY = os.getenv("WEB3FORM_KEY")

# These downloads are only needed once. After the first run, you can comment them out to speed up startup.
nltk.download('stopwords')
#nltk.download('punkt')
#nltk.download('wordnet')

app = Flask(__name__, template_folder='./templates', static_folder='./static')

# --- Load ML Model and Preprocessing Objects ---
try:
    loaded_model = pickle.load(open("model.pkl", 'rb'))
    vector = pickle.load(open("vector.pkl", 'rb'))
except FileNotFoundError:
    print("Error: model.pkl or vector.pkl not found. Make sure they are in the root directory.")
    # You might want to exit or handle this more gracefully
    exit()

lemmatizer = WordNetLemmatizer()
stpwrds = set(stopwords.words('english'))

# --- ML Prediction Function ---
def fake_news_det(news):
    review = news
    review = re.sub(r'[^a-zA-Z\s]', '', review)
    review = review.lower()
    review = nltk.word_tokenize(review)
    
    corpus = []
    for y in review:
        if y not in stpwrds:
            corpus.append(lemmatizer.lemmatize(y))
            
    input_data = [' '.join(corpus)]
    vectorized_input_data = vector.transform(input_data)
    prediction = loaded_model.predict(vectorized_input_data)
    return prediction

# --- Page Routes ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        message = request.form['news']
        if not message.strip():
            # Handle empty input
            return render_template("prediction.html", prediction_text="Please enter a news article or headline.")

        pred = fake_news_det(message)
        
        if pred[0] == 1:
            result = "Prediction: This looks like FAKE news. 📰"
        else:
            result = "Prediction: This looks like REAL news. 📰"
            
        return render_template("prediction.html", prediction_text=result)
    else:
        # For GET request, just show the page
        return render_template('prediction.html')

# --- NEW ROUTE for the 'How It Works' page ---
@app.route('/working')
def working():
    return render_template('working.html')

# --- NEW ROUTE for the 'About' page ---
# (You will need to create about.html)
@app.route('/about')
def about():
    return render_template('about.html')

# --- NEW ROUTE for the 'Contact' page ---
# (You will need to create contact.html)
@app.route('/contact')
def contact():
    return render_template('contact.html', web3form_key=WEB3FORM_KEY)

if __name__ == '__main__':
    app.run(debug=True)