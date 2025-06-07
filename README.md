# restaurant-app
# 🍽️ ChefMate: Restaurant Clustering & Cooking Guide Application

**ChefMate** is an intelligent Streamlit-based web application that clusters and recommends restaurants based on user preferences and provides a conversational cooking guide chatbot to assist with recipe preparation.

---

## 📌 Project Overview

ChefMate combines machine learning, cloud computing, and interactive user interfaces to offer:

- Personalized restaurant recommendations based on cuisine, dish type, or location.
- A cooking assistant chatbot for step-by-step recipe guidance.
- Dynamic map visualizations and restaurant metrics.
- Scalable cloud deployment using AWS services.

---

## 🚀 Key Features

- 🔍 **Smart Restaurant Recommendations** using clustering algorithms.
- 🗺️ **Interactive Maps & Ratings** for visual insights.
- 🤖 **AI Chatbot** to guide users in preparing recipes.
- ☁️ **Cloud Integration** using AWS S3, RDS, and EC2.
- 🎛️ **User-friendly Interface** built with Streamlit.

---

## 🧠 Skills Gained

- Streamlit application development
- Machine learning model training (clustering)
- AWS RDS, EC2 integration
- Data preprocessing and cleaning
- End-to-end ML model integration
- Chatbot development with NLP
- Cloud deployment 

---

## 🧾 Problem Statement

> Build an intelligent application that clusters and recommends restaurants based on user input (cuisine/dishes) and integrates a chef-like chatbot to guide users in preparing recipes.

---

## 🏢 Business Use Cases

- 📍 Location-based and cuisine-based restaurant recommendations.
- 📊 Visual analytics and metrics for restaurant data.
- 👨‍🍳 Recipe preparation assistance via chatbot.
- 📦 Potential integration with food delivery platforms.

---

## 🛠️ Technology Stack

| Domain | Tools |
|--------|-------|
| Frontend | Streamlit |
| Backend | Python, Scikit-learn |
| ML Model | Clustering (e.g., KMeans) |
| Cloud | AWS S3, RDS, EC2 |
| Chatbot | NLP-based conversational logic |
| Database | PostgreSQL / MySQL on AWS RDS |
| Version Control | Git, GitHub |

---

## 🗂️ Dataset

- **Source:** Zomato JSON Dataset
- **Key Fields:**  
  - `Restaurant ID`, `Name`, `Location`, `Cuisines`, `Ratings`,  
  - `Average Cost for Two`, `Price Range`,  
  - `Features` (Table booking, Online delivery),  
  - `Longitude`, `Latitude`

### 🔧 Preprocessing Includes:
- Handling missing/inconsistent data
- Normalizing cost and rating fields
- Converting JSON to SQL schema
- Extracting relevant features for clustering

---

## 🔄 Project Pipeline

1. **Data Collection:**  
   Upload raw JSON data to AWS S3.

2. **Data Preprocessing:**  
   Pull from S3 → Clean → Structure into SQL → Push to RDS.

3. **Model Training:**  
   Pull from RDS → Train clustering model → Save model.

4. **Application Development (Streamlit):**  
   - Restaurant recommendations via clustering
   - Visualizations with maps and ratings
   - Chatbot for recipe assistance

5. **Deployment:**  
   Host app and model on AWS EC2.

---

## 📊 Evaluation Metrics

| Aspect | Metric |
|--------|--------|
| 🔍 Recommendation Accuracy | User feedback |
| 🤖 Chatbot Effectiveness | Resolution of queries |
| ⚡ App Responsiveness | Latency & speed |
| 📈 User Engagement | Session time, interactions |

---

## 📦 Deliverables

- Source code (Streamlit app, ML model, chatbot logic)
- Preprocessed dataset (SQL format)
- Trained clustering model (Pickle/Joblib)
- AWS deployment scripts
- Project documentation & pipeline explanation

---

