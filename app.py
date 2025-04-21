from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Home route (optional if serving frontend)
@app.route('/')
def home():
    return render_template('index.html')

# Load internships data once
internships = pd.read_csv('internships.csv')

# Clean and preprocess internship data
internships.fillna('', inplace=True)
internships['Required_Skills'] = internships['Required_Skills'].str.lower().str.strip()
internships['Required_Field'] = internships['Required_Field'].str.lower().str.strip()
internships['Location'] = internships['Location'].str.lower().str.strip()

# Combine internship details into a single text field
internships['combined_text'] = internships['Required_Skills'] + " " + internships['Required_Field'] + " " + internships['Location']

# Initialize and fit vectorizer on internships
vectorizer = TfidfVectorizer()
internship_tfidf = vectorizer.fit_transform(internships['combined_text'])

# Function to recommend internships
def recommend_internships(skills, field, location, top_n=3):
    input_text = f"{skills.lower().strip()} {field.lower().strip()} {location.lower().strip()}"
    input_tfidf = vectorizer.transform([input_text])

    # Compute cosine similarity
    similarities = cosine_similarity(input_tfidf, internship_tfidf)[0]
    top_indices = similarities.argsort()[-top_n:][::-1]

    # Return top N company names
    recommendations = internships.iloc[top_indices]['Company'].tolist()
    return recommendations

# Recommendation API endpoint
@app.route('/recommend', methods=['POST'])
def get_recommendations():
    data = request.get_json()

    skills = data.get('skills', '')
    field = data.get('field_of_study', '')
    location = data.get('preferred_location', '')

    if not (skills and field and location):
        return jsonify({'error': 'All fields are required'}), 400

    recommendations = recommend_internships(skills, field, location)
    return jsonify({'recommended_companies': recommendations})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
