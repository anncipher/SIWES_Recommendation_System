# Import necessary libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable frontend to connect

# Load datasets (you can adjust these to read from a database or another source)
students = pd.read_csv('C:\\Users\\HP\\OneDrive\\Desktop\\siwes_api\\students.csv')  
internships = pd.read_csv('C:\\Users\\HP\\OneDrive\\Desktop\\siwes_api\\internships.csv')  

# Clean and preprocess the data (ensure the relevant columns exist in your dataset)
students['Skills'] = students['Skills'].str.lower().str.strip()
students['Field_of_Study'] = students['Field_of_Study'].str.lower().str.strip()
students['Preferred_Location'] = students['Preferred_Location'].str.lower().str.strip()

internships['Required_Skills'] = internships['Required_Skills'].str.lower().str.strip()
internships['Required_Field'] = internships['Required_Field'].str.lower().str.strip()
internships['Location'] = internships['Location'].str.lower().str.strip()

# Combine skills, field of study, and preferred location into a single text column for each student and internship
students['combined_text'] = students['Skills'] + " " + students['Field_of_Study'] + " " + students['Preferred_Location']
internships['combined_text'] = internships['Required_Skills'] + " " + internships['Required_Field'] + " " + internships['Location']

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Fit and transform the combined text for both students and internships
student_tfidf = vectorizer.fit_transform(students['combined_text'])
internship_tfidf = vectorizer.transform(internships['combined_text'])

# Compute cosine similarity between each student and each internship
similarity_matrix = cosine_similarity(student_tfidf, internship_tfidf)

# Function to recommend internships based on a student's skills, field, and location
def recommend_internships(student_skills, student_field, student_location, top_n=3):
    # Combine input skills, field, and location into a single string
    input_text = student_skills + " " + student_field + " " + student_location
    
    # Vectorize the input data
    student_tfidf_input = vectorizer.transform([input_text])
    
    # Compute cosine similarity
    similarity_matrix = cosine_similarity(student_tfidf_input, internship_tfidf)
    
    # Get top N internships based on similarity
    sim_scores = list(enumerate(similarity_matrix[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_matches = [internships.iloc[i[0]]['Company'] for i in sim_scores[:top_n]]
    
    return top_matches

# Define an API endpoint for receiving the student's data and returning recommendations
@app.route('/recommend', methods=['POST'])
def get_recommendations():
    # Extract data from the request
    data = request.get_json()
    
    student_skills = data.get('skills', '')
    student_field = data.get('field_of_study', '')
    student_location = data.get('preferred_location', '')
    
    # Get recommendations
    top_recommendations = recommend_internships(student_skills, student_field, student_location)
    
    return jsonify({'recommended_companies': top_recommendations})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

app = Flask(__name__)
CORS(app)  # Enable frontend to connect