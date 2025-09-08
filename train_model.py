import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score

# --- Step 1: Load and Prepare the Data ---
try:
    df = pd.read_csv('news.csv')
except FileNotFoundError:
    print("Error: news.csv not found. Make sure it's in the same directory.")
    exit()

# Drop any rows with missing values
df.dropna(inplace=True)

# Ensure the required columns exist
if 'text' not in df.columns or 'label' not in df.columns:
    print("Error: The CSV must have 'text' and 'label' columns.")
    exit()

# Convert text labels ('FAKE', 'REAL') to numbers (1, 0)
if df['label'].dtype == 'object':
    df['label'] = df['label'].apply(lambda x: 1 if x.strip().upper() == 'FAKE' else 0)

# Check if we have more than one class to predict
if len(df['label'].unique()) < 2:
    print("\n--- CRITICAL ERROR ---")
    print("Your dataset contains only one class of news.")
    print("The model needs examples of BOTH 'REAL' and 'FAKE' news to learn.")
    print("Please use a dataset with a mix of both labels.")
    exit() # Stop the script

# Separate the features (x) and the target (y)
x = df['text']
y = df['label']


# --- Step 2: Split Data and Vectorize Text ---
# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)

# Initialize a TfidfVectorizer to convert text into numerical data
# This is a standard approach for text classification
vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
tfidf_train = vectorizer.fit_transform(x_train)
tfidf_test = vectorizer.transform(x_test)


# --- Step 3: Train the Model ---
# Initialize a new PassiveAggressiveClassifier
# This is the corrected step: we create a new model instead of loading an old one.
model = PassiveAggressiveClassifier(max_iter=100) # Increased max_iter for better training
model.fit(tfidf_train, y_train)


# --- Step 4: Evaluate the Model ---
# Make predictions on the test set
y_pred = model.predict(tfidf_test)
score = accuracy_score(y_test, y_pred)
print(f'Model Accuracy: {round(score*100,2)}%')


# --- Step 5: Save the Trained Model and Vectorizer ---
# Save the newly trained model to model.pkl
with open('model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

# Save the vectorizer to vector.pkl
with open('vector.pkl', 'wb') as vector_file:
    pickle.dump(vectorizer, vector_file)

print("\nModel retrained and saved successfully!")
print("Files 'model.pkl' and 'vector.pkl' have been updated.")

