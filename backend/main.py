# backend/main.py
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np 
from rapidfuzz import process, fuzz

# ==============================
# CONFIGURATION
# ==============================
DB_PATH = os.path.join(os.path.dirname(__file__), "faq.db")
SIMILARITY_THRESHOLD = 0.5   # Lowered for better matching
FUZZY_THRESHOLD = 50         # Fuzzy match threshold
TOP_K = 3                     # Number of top results to retrieve

app = FastAPI(title="Customer Care FAQ Chatbot")

# ==============================
# Pydantic Models
# ==============================
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    suggestion: str = None

# ==============================
# Load Embedding Model
# ==============================
print("Loading embedding model...")
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# ==============================
# Database Functions
# ==============================
def get_all_faqs_from_db():
    """Fetch all FAQs from the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT question, answer FROM faq")
    faqs = cur.fetchall()
    conn.close()
    return [{"question": row["question"], "answer": row["answer"]} for row in faqs]

def save_chat_history(user_msg, bot_msg):
    """Save conversation history to database."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO chat_history (user_msg, bot_msg) VALUES (?, ?)", (user_msg, bot_msg))
    conn.commit()
    conn.close()

# ==============================
# Build FAISS Vector Store
# ==============================
def build_vectorstore():
    """Create FAISS index from FAQ questions."""
    faqs = get_all_faqs_from_db()

    if not faqs:
        print("ERROR: No FAQs found in database!")
        return None, []

    questions = [faq["question"] for faq in faqs]
    print("FAQs Loaded:", questions)

    embeddings = embedding_model.encode(questions, convert_to_numpy=True)
    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])  # L2 distance
    index.add(embeddings)

    print("FAISS index built successfully. Total vectors:", index.ntotal)
    return index, faqs

vectorstore, faq_data = build_vectorstore()
faq_questions = [f["question"] for f in faq_data]

# ==============================
# Utility - FAISS Search
# ==============================
def similarity_search_with_score(query, k=TOP_K):
    """Search FAISS for closest matches to the query."""
    query_vector = embedding_model.encode([query], convert_to_numpy=True).astype("float32")
    distances, indices = vectorstore.search(query_vector, k)

    results = []
    for idx, distance in zip(indices[0], distances[0]):
        if idx != -1:
            results.append((faq_data[idx], float(distance)))
    return results

# ==============================
# FastAPI Route - Query
# ==============================
@app.post("/query", response_model=QueryResponse)
def query_faq(req: QueryRequest):
    q = req.question.strip()
    print("\nUser Query:", q)

    # ==============================
    # 1. Check if vectorstore is ready
    # ==============================
    if vectorstore is None or vectorstore.ntotal == 0:
        return QueryResponse(answer="Sorry, the knowledge base is empty. Please add FAQs first.")

    # ==============================
    # 2. Semantic Search (FAISS)
    # ==============================
    docs_and_scores = similarity_search_with_score(q, k=TOP_K)
    print("FAISS Results:", docs_and_scores)

    if docs_and_scores:
        # L2 distance is inverted for similarity (smaller = better)
        best_match, best_score = docs_and_scores[0]
        similarity = 1 / (1 + best_score)  # Convert distance to similarity score
        print(f"Best Match: {best_match['question']} | Score: {similarity}")

        if similarity >= SIMILARITY_THRESHOLD:
            save_chat_history(q, best_match["answer"])
            return QueryResponse(answer=best_match["answer"])

    # ==============================
    # 3. Fuzzy Matching Fallback
    # ==============================
    # 3. Fuzzy Matching Fallback
    print("Running fuzzy matching...")
    fuzzy_match = process.extractOne(q, faq_questions, scorer=fuzz.token_sort_ratio)
    print("Fuzzy Match Result:", fuzzy_match)

    if fuzzy_match and fuzzy_match[1] >= FUZZY_THRESHOLD:
        matched = next(f for f in faq_data if f["question"] == fuzzy_match[0])
        print("Fuzzy Match Accepted:", matched)
        save_chat_history(q, matched["answer"])
        return QueryResponse(answer=matched["answer"])

    #print("Running fuzzy matching...")
    #fuzzy_match = process.extractOne(q, faq_questions, scorer=fuzz.token_sort_ratio)
    #print("Fuzzy Match:", fuzzy_match)

    #if fuzzy_match and fuzzy_match[1] >= FUZZY_THRESHOLD:
        #matched = next(f for f in faq_data if f["question"] == fuzzy_match[0])
        #save_chat_history(q, matched["answer"])
        #return QueryResponse(answer=matched["answer"])

    # ==============================
    # 4. Fallback Response with Suggestions
    # ==============================
    suggestions = [doc["question"] for doc, _ in docs_and_scores] if docs_and_scores else []
    print("No strong match found. Suggestions:", suggestions)
    save_chat_history(q, "Sorry, I couldn't find an exact match.")
    return QueryResponse(answer="Sorry, I can only answer questions related to our store policies, orders, and products.",
                         suggestion=suggestions[0] if suggestions else None)
