chat_history = []
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from database import db
from models import ChatHistory
import os
import pickle
import faiss
import numpy as np

from openai import OpenAI
from langchain_huggingface import HuggingFaceEmbeddings

# =========================
# LOAD ENV VARIABLES
# =========================

load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

# =========================
# OPENAI CLIENT FOR NVIDIA
# =========================

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY
)

# =========================
# FLASK APP
# =========================

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# =========================
# LOAD FAISS
# =========================

index = faiss.read_index("faiss_index/index.faiss")

with open("faiss_index/index.pkl", "rb") as f:
    documents = pickle.load(f)

# =========================
# EMBEDDING MODEL
# =========================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():
    return render_template("index.html")

# =========================
# ADMIN DASHBOARD
# =========================

@app.route("/admin")
def admin():

    chats = ChatHistory.query.order_by(
        ChatHistory.timestamp.desc()
    ).all()

    return render_template(
        "admin.html",
        chats=chats
    )
# =========================
# CHAT API
# =========================

@app.route("/chat", methods=["POST"])
def chat():

    try:

        user_message = request.json.get("message")

        chat_history.append({
            "role": "user",
            "message": user_message
        })

        # Convert question to embedding
        query_embedding = embedding_model.embed_query(user_message)

        # Search FAISS
        D, I = index.search(
            np.array([query_embedding]).astype("float32"),
            5
        )

        print("\n===================")
        print("USER:", user_message)
        print("===================")
        print("Distances:", D)

        retrieved_docs = []

        for idx in I[0]:

            if idx < len(documents):

                doc = documents[idx]

                if hasattr(doc, "page_content"):
                    content = doc.page_content
                else:
                    content = str(doc)

                print(content)
                print("-------------------")

                retrieved_docs.append(content)

        # If nothing relevant found
        if not retrieved_docs:
            print("\nRETURNING TO FRONTEND:")
            print(answer)
            print("-----------------------")
            return jsonify({
                "answer": "Sorry, I could not find that information in the BalleBaaz Arena knowledge base."
            })

        # Build context
        context = "\n\n".join(retrieved_docs)

        # Prompt
        prompt = f"""
You are BalleBaaz Arena AI Assistant.

STRICT RULES:

1. Answer ONLY using the provided context.
2. Never use your own knowledge.
3. Never guess.
4. Never assume.
5. If the answer is not explicitly present in the context, reply exactly:

Sorry, I could not find that information in the BalleBaaz Arena knowledge base.

CONTEXT:
{context}

QUESTION:
{user_message}
"""

        # NVIDIA RESPONSE
        completion = client.chat.completions.create(
            model="meta/llama-3.1-8b-instruct",
            messages=[
                {
                    "role": "system",
                    "content": """
You answer ONLY from the retrieved context.
Do not make assumptions.
Do not invent information.
If the answer is not present in the context, say:
Sorry, I could not find that information in the BalleBaaz Arena knowledge base.
"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.0,
            max_tokens=150
        )

        answer = completion.choices[0].message.content

        # Save chat history
        new_chat = ChatHistory(
            user_message=user_message,
            bot_response=answer
        )

        db.session.add(new_chat)
        db.session.commit()

        return jsonify({
            "answer": answer
        })

    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "answer": "Server error occurred."
        })

# =========================
# RUN APP
# =========================

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)