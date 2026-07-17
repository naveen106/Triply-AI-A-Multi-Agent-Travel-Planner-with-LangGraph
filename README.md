# ✈️ Triply AI — A Multi-Agent Travel Planner with LangGraph

An open-source AI travel planner that turns a natural-language trip request into a practical travel plan with flight suggestions, hotel ideas, and a day-by-day itinerary. The project uses a multi-agent workflow built with LangGraph, LangChain, and FastAPI.

## Why this project?

Planning a trip usually means jumping between multiple websites, tools, and spreadsheets. This project brings that flow into one experience by combining:

- a flight-search agent,
- a hotel-research agent,
- an itinerary-planning agent, and
- a final response agent,

all coordinated through a LangGraph workflow.

## Features

- ✈️ Flight research using AviationStack
- 🏨 Hotel suggestions using Tavily search
- 🧠 Multi-agent orchestration with LangGraph
- 📝 Structured travel itinerary generation
- 🌐 FastAPI backend with a simple web interface
- 💾 Conversation state persistence using PostgreSQL
- ⚡ LLM-powered responses with Groq

## Tech Stack

- Python 3.10+
- FastAPI
- Jinja2 + HTML/CSS/JavaScript frontend
- LangGraph
- LangChain
- Groq LLMs
- PostgreSQL
- Tavily API
- AviationStack API

## Project Structure

```text
.
├── app.py                # FastAPI app entry point
├── backend.py            # LangGraph travel workflow
├── requirements.txt      # Python dependencies
├── static/               # Static frontend assets
├── templates/            # HTML templates
└── tools/                # Flight and web search integrations
```

## Prerequisites

Before running the project locally, make sure you have:

- Python 3.12 or newer recommended (latest stable version if possible)
- uv installed (recommended for dependency management)
- PostgreSQL running and accessible
- API keys for:
  - Groq
  - Tavily
  - AviationStack


## Beginner-Friendly Setup Guide

Follow these steps if you are new to Python or web apps.

### 1) Install Python

You need Python installed before using this project. You can download from internet externally or like here from command line

#### Windows (Command Prompt or PowerShell)
```powershell
winget install -e --id Python.Python.3.12
```

If you want the latest available version, you can try:

```powershell
winget upgrade --id Python.Python.3.12
```

After installation, verify:

```bash
python --version
```

### 2) Install uv

uv is the easiest way to manage dependencies for this project.

#### Windows (PowerShell)
```
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

If that does not work, use:

```powershell
py -m pip install --user uv
```

Verify installation:

```bash
uv --version
```

### 3) Create the environment and install dependencies

```bash
uv venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

To add/install dependencies, you can add by giving dependency name or using requirments.txt file which will download all the listed dependencies in that file.
```bash
uv add <package name here>
```

```bash
uv add -r requirements.txt
```


### 4)Clone the project

Open a terminal and run:

```bash
git clone <your-repository-url>
cd Triply-AI
```

If you already downloaded the project folder, go into it:

```bash
cd path/to/your/project-folder
```

### 5) Create your .env file

Create a file named `.env` in the project root and add the required values:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/travel_db
GROQ_API_KEY=your_groq_api_key
AVIATIONSTACK_API_KEY=your_aviationstack_api_key
TAVILY_API_KEY=your_tavily_api_key
DEFAULT_ORIGIN_IATA=IN
```

> If you do not have the API keys yet, you will need to sign up for the services and paste the keys into the file.

### 6) Run the web app

Start the app with:

```bash
uv run python app.py
```

Or with Uvicorn:

```bash
uv run uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 7) Open the app in your browser

After the server starts, open:

```text
http://localhost:8000/
```

If the page opens, the app is running successfully.

### 8) Test the API

You can also test the backend directly:

```bash
curl -X POST http://localhost:8000/api/travel \
  -H "Content-Type: application/json" \
  -d '{"message":"Plan a 3-day trip to Tokyo with a budget of $1200"}'
```

## API Endpoints

- GET /health - Health check
- POST /api/travel - Submit a travel request

Example request:

```bash
curl -X POST http://localhost:8000/api/travel \
  -H "Content-Type: application/json" \
  -d '{"message":"Plan a 3-day trip to Tokyo with a budget of $1200"}'
```

## How the Workflow Works

1. The user submits a travel request.
2. The flight agent gathers flight-related information.
3. The hotel agent searches for accommodation suggestions.
4. The itinerary agent creates a practical travel plan.
5. The final agent formats the result into a polished response.

## Contributing

Contributions are welcome. If you want to improve the app, add new travel features, or fix issues:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Open a pull request

## Acknowledgments

This project is built with the help of modern LLM tooling and travel APIs, and it is intended as a practical example of combining LangGraph agents with real-world applications.