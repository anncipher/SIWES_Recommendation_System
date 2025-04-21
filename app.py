# Import necessary libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load datasets
students = pd.read_csv('students.csv')  
internships = pd.read_csv('internships.csv')  

# Preprocess the data
students['Skills'] = students['Skills'].str.lower().str.strip()
students['Field_of_Study'] = students['Field_of_Study'].str.lower().str.strip()
students['Preferred_Location'] = students['Preferred_Location'].str.lower().str.strip()

internships['Required_Skills'] = internships['Required_Skills'].str.lower().str.strip()
internships['Required_Field'] = internships['Required_Field'].str.lower().str.strip()
internships['Location'] = internships['Location'].str.lower().str.strip()

# Combine relevant text for vectorization
students['combined_text'] = students['Skills'] + " " + students['Field_of_Study'] + " " + students['Preferred_Location']
internships['combined_text'] = internships['Required_Skills'] + " " + internships['Required_Field'] + " " + internships['Location']

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Fit and transform the combined text
student_tfidf = vectorizer.fit_transform(students['combined_text'])
internship_tfidf = vectorizer.transform(internships['combined_text'])

# Compute cosine similarity matrix
similarity_matrix = cosine_similarity(student_tfidf, internship_tfidf)

# Function to recommend internships

def recommend_internships(student_skills, student_field, student_location, top_n=3):
    input_text = student_skills.lower().strip() + " " + student_field.lower().strip() + " " + student_location.lower().strip()
    student_tfidf_input = vectorizer.transform([input_text])
    similarity_matrix = cosine_similarity(student_tfidf_input, internship_tfidf)
    sim_scores = list(enumerate(similarity_matrix[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Return full internship details for top matches
    top_matches = []
    for i, score in sim_scores[:top_n]:
        match = internships.iloc[i].to_dict()
        match['match_score'] = round(float(score), 2)
        top_matches.append(match)
    return top_matches

# API endpoint for recommendations
@app.route('/recommend', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    student_skills = data.get('skills', '')
    student_field = data.get('field_of_study', '')
    student_location = data.get('preferred_location', '')

    recommendations = recommend_internships(student_skills, student_field, student_location)
    return jsonify({'recommended_companies': recommendations})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
