from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Home route (optional if serving frontend)
@app.route('/')
def home():
    return render_template('index.html')


# Load and preprocess internships data
internships = pd.read_csv('internships.csv')
internships.fillna('', inplace=True)

# Normalize fields
internships['Required_Skills'] = internships['Required_Skills'].str.lower().str.strip()
internships['Required_Field'] = internships['Required_Field'].str.lower().str.strip()
internships['Location'] = internships['Location'].str.lower().str.strip()

# Combine features for vectorization
internships['combined_text'] = (
    internships['Required_Skills'] + ' ' +
    internships['Required_Field'] + ' ' +
    internships['Location']
)

# Vectorize the internship data
vectorizer = TfidfVectorizer()
internship_tfidf = vectorizer.fit_transform(internships['combined_text'])


# Matching Function
def recommend_internships(skills, field, location, top_n=3):
    user_input = f"{skills.lower().strip()} {field.lower().strip()} {location.lower().strip()}"
    input_vector = vectorizer.transform([user_input])
    similarity_scores = cosine_similarity(input_vector, internship_tfidf)[0]
    top_indices = similarity_scores.argsort()[-top_n:][::-1]

    recommended = []
    for idx in top_indices:
        recommended.append({
            'Company': internships.iloc[idx]['Company'],
            'Role': internships.iloc[idx]['Role'],
            'Location': internships.iloc[idx]['Location'].capitalize()
        })

    return recommended


# API Route
@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    skills = data.get('skills', '')
    field = data.get('field_of_study', '')
    location = data.get('preferred_location', '')

    if not (skills and field and location):
        return jsonify({'error': 'All fields are required'}), 400

    matches = recommend_internships(skills, field, location)
    return jsonify({'recommended_companies': matches})


# Entry point
import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

