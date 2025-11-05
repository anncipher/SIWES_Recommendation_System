# SIWES_Recommendation_System


The SIWES (Student Industrial Work Experience Scheme) Recommendation System is a web-based application that helps students automatically find internship opportunities that best match their skills, field of study, and preferred location.

The system uses a text-based similarity model (TF-IDF + Cosine Similarity) to recommend companies offering internship roles most relevant to each student’s profile.

---

🧩 **Features**

🧠 **AI-powered recommendations:** Matches students to internships using skill and field similarity.

🌍 **Location-based filtering:** Suggests internships within a student’s preferred area.

⚡ **Fast and simple interface:** Built with HTML, CSS, and JavaScript for smooth interaction.

☁️ **Fully deployed system:** Flask backend on Render and frontend on Vercel.

---

🛠️ **Tech Stack**

**Backend**

**Python (Flask)** – Web framework for building the REST API.

**Pandas** – For data manipulation and CSV handling.

**Scikit-learn** – For text vectorization (TfidfVectorizer) and similarity computation (cosine_similarity).

**Flask-CORS** – Enables frontend-backend communication across different domains.

**Frontend**

**HTML5, CSS3, JavaScript** – User interface and API interaction.

**Fetch API** – Sends POST requests to the Flask endpoint and displays results dynamically.

**Deployment**

**Render** – Hosts and serves the Flask API.

---

⚙️ **How It Works**

1. Students enter their Field of Study, Skills, and Preferred Location on the web page.

2. The frontend sends these inputs to the Flask API hosted on Render.

3. The API processes the request by comparing the user input with internship listings using TF-IDF vectorization and cosine similarity.

4. The top matching internships are returned and displayed on the interface.

---

🧪 **Libraries Used**

flask

flask-cors

pandas

scikit-learn

---

🚀 **Deployment**

**Backend (Flask)** – Deployed on Render

**Integration:** The frontend connects to the backend through an API endpoint such as

https://skillsinnov8.onrender.com/recommend

---

📊 **Outcome**

Fully functional web app that generates personalized internship recommendations.

Simplified the internship search process for students.

Demonstrates integration of machine learning, API development, and web deployment.

---

🖼️ **Interface Preview**

<img width="1361" height="679" alt="SIWES Recommender" src="https://github.com/user-attachments/assets/ec9d7756-b942-4084-b403-069bf1abe083" />
<img width="1363" height="681" alt="SIWES Recommender2" src="https://github.com/user-attachments/assets/22a765ad-5f20-42bf-901a-f451c341dadb" />



🌐 Project Live: https://skills-innov8.vercel.app


## 💡 Future Improvements
---
- Add user authentication and personalized dashboards  
- Integrate a database (e.g., PostgreSQL) for dynamic internship listings  
- Deploy an ML model trained on real-time student–employer data 
