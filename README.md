# AI-assignment
web apliation multiple choice question test for autism






# README.md

## Autism Screening Questionnaire Web App

This repository builds a local web application that asks 20 multiple‑choice questions (generic placeholders) on a single scrollable page and then shows a probability of autism based on the selected answers.

### Stack
- **FastAPI** – Backend exposing a `/predict` endpoint.
- **PyTorch** – Tiny placeholder model that maps the 20 answers to a probability.
- **Streamlit** – Frontend UI that displays all questions, collects answers, calls the API, and shows the result.

### Project Structure
```
AI Assignment (or your chosen folder)
│
├─ backend/
│   ├─ main.py            # FastAPI app
│   ├─ model.py           # Placeholder PyTorch model
│   └─ requirements.txt   # Backend dependencies
│
├─ frontend/
│   ├─ app.py             # Streamlit UI
│   └─ requirements.txt   # Frontend dependencies
│
├─ questions.json         # 20 placeholder questions
├─ README.md              # This file
└─ .gitignore            # Optional
```

### Prerequisites
- Python 3.10+ (tested on 3.11)
- `pip` available in your environment

### Install Dependencies
Open two terminal windows (or use a terminal multiplexer).

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload   # starts the FastAPI server on http://127.0.0.1:8000
```

#### Frontend
```bash
cd ../frontend
pip install -r requirements.txt
streamlit run app.py        # opens the UI at http://localhost:8501
```

### Using the App
1. Open the Streamlit URL shown in the terminal (typically `http://localhost:8501`).
2. Answer all 20 questions by selecting one of the four options for each.
3. Click **Submit** – the app will call the FastAPI backend and display:
   - The probability (as a percentage and a progress bar).
   - A short textual interpretation (Low / Moderate / High likelihood).

### Extending / Retraining
The current model is a random‑weight linear layer, only to demonstrate the flow. To improve accuracy:
1. Replace `backend/model.py` with a trained PyTorch model (e.g., a small MLP).
2. Update the `predict` method to load saved weights.
3. Adjust the scoring logic in `frontend/app.py` if you change the answer encoding.

### Notes
- All questions appear on the same scrollable page (Streamlit handles scrolling automatically).
- No Flask is used.
- The app runs locally; you can later containerise it with Docker if desired.

---
*Happy testing!*
