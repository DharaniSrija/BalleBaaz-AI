# 🏏 Ballebaaz Arena AI Chatbot

A Flask + LangChain + FAISS + NVIDIA-powered cricket AI assistant.

## Project Structure
```
BallebaazArena/
├── app.py                  ← Flask backend (unchanged)
├── create_embeddings.py    ← Build FAISS index from ChatBot.json
├── requirements.txt        ← Python dependencies
├── .env                    ← NVIDIA API key
├── faiss_index/
│   ├── index.faiss
│   └── index.pkl
├── templates/
│   └── index.html          ← ✅ Themed UI
└── static/
    ├── style.css           ← ✅ Cricket equipment palette
    ├── script.js           ← ✅ Improved JS
    └── cricket-equipment.avif
```

## Setup & Run
```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your NVIDIA key to .env
# NVIDIA_API_KEY=your_key_here

# 4. Run
python app.py
# Open http://127.0.0.1:5000
```

## Theme Colors (from cricket-equipment.avif)
| Name          | Hex       | Used for               |
|---------------|-----------|------------------------|
| Pitch Teal    | #3da8a8   | Borders, accents, dots |
| Sage Green    | #5dbf9a   | Status dot, highlights |
| Cream/Ivory   | #dde8c8   | Header text            |
| Amber/Gold    | #d4a83a   | Send button, badge     |
| Forest Green  | #005040   | Header bg, bot avatar  |
| Night Navy    | #08142e   | Page background        |
