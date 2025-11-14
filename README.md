
# 🤖 Customer Support FAQ Chatbot (FastAPI + Streamlit + FAISS)

This project is a **locally running customer support chatbot** that answers FAQs using **semantic search**.
It uses **FastAPI** as the backend, **Streamlit** as the frontend, and **FAISS** for vector similarity search.

---

## 🚀 Project Overview

The chatbot retrieves the most relevant FAQ from a local SQLite database using **embeddings** and **vector search**.
It works **without any external API**, making it lightweight and cost-free.

### ✔ What the Chatbot Can Do

* Accept customer questions
* Convert the question into an embedding
* Search the FAQ database using FAISS
* Return the closest matching answer
* Display questions & answers instantly in a clean UI

---

## 🧠 Tech Stack

### **Backend**

* FastAPI
* SQLite
* FAISS (Vector Indexing)
* SentenceTransformers (Embedding Model)
* Uvicorn

### **Frontend**

* Streamlit

### **Environment**

* Python 3.12
* Virtual Environment (`venv`)

---

## 📂 Project Structure

```
customer_chatbot_db/
│
├── backend/
│   ├── main.py
│   ├── db_setup.py
│   ├── faq.db
│   ├── models/
│   └── utils/
│
├── frontend/
│   ├── app.py
│
└── README.md
```

---

## ▶️ How to Run the Project

### **1️⃣ Activate Virtual Environment**

```
cd customer_chatbot_db
venv\Scripts\activate
```

### **2️⃣ Run Backend**

```
cd backend
python db_setup.py
uvicorn main:app --reload
```

Backend runs at:
👉 `http://127.0.0.1:8000`

---

### **3️⃣ Run Frontend**

Open a second terminal:

```
cd customer_chatbot_db
venv\Scripts\activate
cd frontend
streamlit run app.py
```

Frontend runs at:
👉 `http://localhost:8501`

---

## 🗄️ Database

 project uses an SQLite database `faq.db` with predefined FAQs:

| Question                       | Answer |
| ------------------------------ | ------ |
| What products do you sell?     | ...    |
| Where are your stores located? | ...    |
| What is your return policy?    | ...    |
| How can I contact support?     | ...    |

FAISS is used to generate embeddings and retrieve the most similar FAQ.

---

## 🧪 How It Works Internally

1. **User asks a question**
2. Backend generates a **question embedding**
3. FAISS retrieves the vector with highest similarity
4. Returns the best matching answer
5. Streamlit displays it in the UI

---

## 🎥 Demo Video

Watch the working demo of the chatbot below:

👉 **[Click here to watch the project demo](https://drive.google.com/file/d/1vohA3BWVKh4Kt6gndCRgm5_cEwGerSwg/view?usp=sharing)**

---

## 🌟 Features

* Fast inference
* No external API required
* Easy deployment
* Clean UI
* Very fast vector search

---

## 📌 Future Improvements

* Add full-fledged RAG with documents
* Add chat history
* Add admin panel to add/remove FAQs
* Deploy on Render / Railway

---

## 🧑‍💻 Author

**Aishwarya Yadav Gotte**
AI/ML Enthusiast | Python Developer | LLMs | FastAPI | Vector Databases

