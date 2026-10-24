
# Ask & Act Mini Agent

Ask & Act Mini Agent is a small full-stack project I built to explore how an AI assistant can respond to questions and use tools. It has a React frontend and a FastAPI backend.

## What it can do

- Answer questions through an AI model using OpenRouter
- Calculate basic arithmetic
- Get weather information using Open-Meteo
- Search a local knowledge file
- Show which tool was used in a response

## Built with

- **Frontend:** React, Vite, JavaScript, CSS
- **Backend:** Python, FastAPI
- **AI:** OpenRouter
- **Weather data:** Open-Meteo

## Project folders

```text
ask-and-act-mini-agent/
├── backend/
│   ├── agent.py
│   ├── app.py
│   ├── tools.py
│   ├── knowledge.json
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
└── .gitignore
```

## Run locally

### 1. Get the project

```bash
git clone https://github.com/ridhkaa16/ask-and-act-mini-agent.git
cd ask-and-act-mini-agent
```

### 2. Start the backend

In PowerShell:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `backend/.env` file based on `.env.example` and add your own OpenRouter API key. Keep this key private and don't commit the `.env` file.

Then start FastAPI:

```powershell
uvicorn app:app --reload
```

The backend runs at `http://127.0.0.1:8000`.

### 3. Start the frontend

Open a second terminal at the project root:

```powershell
cd frontend
npm install
npm run dev
```

Open the local address Vite displays. It is usually `http://localhost:5173`.

Keep both the backend and frontend running while testing the app.

## Example

Try asking:

> What is 25 multiplied by 16?

The agent can use its calculator tool to return the answer.

## Author

Ridhika Ranjith

[GitHub profile](https://github.com/ridhkaa16)
