## VeriScanX - Fake News Detection (Flask + scikit-learn)

VeriScanX is a Flask web application that detects fake news using a trained PassiveAggressiveClassifier with TF‑IDF features. It provides a clean UI with Tailwind CSS and multiple pages: Home, Prediction, How It Works, About, and Contact.

### Features
- Fake news classifier (PassiveAggressiveClassifier) with TF‑IDF vectorizer
- Prediction page to analyze headlines/articles
- Informational pages: How It Works, About, Contact
- Environment-based Web3Forms key (no hardcoded secrets)

### Project Structure
```
app.py
train_model.py
model.pkl
vector.pkl
news.csv
templates/
  index.html
  prediction.html
  working.html
  about.html
  contact.html
static/
  logo.svg
  illustration.png
dataset/
  train.csv
  test.csv
  submit.csv
requirements.txt
```

### Requirements
- Python 3.8+
- See `requirements.txt`

Install dependencies:
```bash
pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file in the project root (this file is git-ignored) and set:
```bash
WEB3FORM_KEY=your_real_web3forms_key
```
This key is injected into the Contact page via Flask. In production, configure this as a platform environment variable instead of a `.env` file.

### Running the App (Development)
```bash
python app.py
```
The app starts with `debug=True` by default. Open `http://127.0.0.1:5000`.

Routes:
- `/` Home
- `/predict` Prediction (GET/POST)
- `/working` How It Works
- `/about` About
- `/contact` Contact

### Training or Updating the Model
If you want to retrain the model using your own dataset, place a CSV named `news.csv` in the project root with columns:
- `text`: the article/headline text
- `label`: `FAKE` or `REAL` (case-insensitive)

Then run:
```bash
python train_model.py
```
This will:
- Validate the dataset
- Train a new TF‑IDF + PassiveAggressiveClassifier model
- Print accuracy
- Save `model.pkl` and `vector.pkl`

The application loads these files at startup.

### Notes on NLTK
The application uses NLTK for tokenization, lemmatization, and stopwords. The first run may require downloading resources (already present in code but commented out). If you see missing resource errors, uncomment in `app.py` near the top:
```python
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')
```

### Styling / UI
The UI uses Tailwind CSS via CDN and the Poppins font. The home page layout is structured to fit the viewport height. If you see overflow on some devices, slightly reduce top/bottom paddings on header or hero.

### Deployment
General guidance:
- Configure `WEB3FORM_KEY` as an environment variable in your hosting platform
- Use a production WSGI server (e.g., gunicorn) and set `debug=False`
- Ensure `model.pkl` and `vector.pkl` are deployed with the app

Example (Linux):
```bash
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:8000 app:app
```

### License
This project includes a `LICENSE` file in the repo root.

### Acknowledgements
- scikit-learn, NLTK
- Tailwind CSS
- Web3Forms for contact form handling


