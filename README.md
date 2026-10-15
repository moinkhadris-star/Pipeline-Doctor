# Pipeline Doctor 🏥

> AI agent that automatically diagnoses CI/CD pipeline failures using GitHub API and Google Gemini AI.

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://docker.com)
[![AWS](https://img.shields.io/badge/AWS-EC2-orange)](https://aws.amazon.com)
[![Gemini](https://img.shields.io/badge/Gemini-AI-purple)](https://ai.google.dev)

---

## What is Pipeline Doctor?

Every DevOps engineer has been frustrated by cryptic CI/CD pipeline failures.
Pipeline Doctor solves this by automatically connecting to your GitHub repository,
finding the latest pipeline failure, and using AI to diagnose exactly what went
wrong and how to fix it.

**No more manually reading through hundreds of log lines.**

---

## Try It Live

Live demo: `http://16.171.135.155:8000`

## How to Use

### Diagnose Latest Failure (automatic)
1. Enter GitHub repo name: `username/repo-name`
2. Leave Run ID blank
3. Click "Diagnose Pipeline"
4. App automatically finds the most recent failure

### Diagnose a Specific Run
1. Go to GitHub Actions on any repo
2. Click any failed pipeline run
3. Copy the Run ID from the URL:
   `github.com/user/repo/actions/runs/12345678`
                                          
4. Enter repo name AND Run ID in Pipeline Doctor
5. Click "Diagnose Pipeline"
---
Use these pre-built demo pipelines to test:

| Demo | Repo | Run ID | Failure Type |
|------|------|--------|--------------|
| Missing package | moinkhadris-star/github-actions-learning |38734044392| Dependency error |
| Syntax error | moinkhadris-star/github-actions-learning |38734247389| Python syntax |
| Failed tests | moinkhadris-star/github-actions-learning |38734488293| Test failure |

Steps:
1. Open the live demo link above
2. Copy a repo name from the table
3. Copy the Run ID
4. Paste both into Pipeline Doctor
5. Click Diagnose Pipeline
6. See AI diagnosis in seconds

---

## How It Works

1. User enters GitHub repo name
2. App connects to GitHub API
3. Finds latest failed pipeline run
4. Extracts job and step failure details
5. Gemini AI analyses the failure
6. Returns diagnosis and numbered fix steps
7. Displayed in clean web UI


---

## Features

- Connect to any public GitHub repository
- Automatically finds the latest failed pipeline run
- Diagnose a specific run using Run ID
- AI-powered diagnosis using Google Gemini
- Shows pipeline name, branch, and exact failure time
- Direct link to the failed run on GitHub
- Numbered fix steps with confidence level
- Clean dark-themed web interface
- Fully containerised with Docker
- Deployed on AWS EC2

---

## Tech Stack

| Category | Technology |
|----------|-----------|
| Backend | Python, FastAPI |
| AI | Google Gemini API |
| GitHub Integration | PyGithub |
| Frontend | HTML, CSS, JavaScript |
| Containerisation | Docker |
| Cloud | AWS EC2 |
| CI/CD | GitHub Actions |
| Environment | python-dotenv |

---

## Project Structure

```
pipeline-doctor/
├── app/
│   ├── __init__.py
│   ├── main.py              
│   ├── agent.py             
│   ├── github_client.py     
│   └── templates/
│       └── index.html       
├── tests/
│   └── test_agent.py        
├── .github/
│   └── workflows/
│       └── deploy.yml       
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```


---

## Local Setup

### Prerequisites

- Python 3.11+
- Docker Desktop
- GitHub Personal Access Token
- Google Gemini API Key (free at aistudio.google.com)

### 1. Clone the repository

```bash
git clone https://github.com/moinkhadris-star/pipeline-doctor.git
cd pipeline-doctor
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` with your keys:

GEMINI_API_KEY=your-gemini-api-key-here
GITHUB_TOKEN=your-github-personal-access-token-here

### 3. Run with Docker (recommended)

```bash
docker-compose up --build
```

### 4. Run without Docker

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### 5. Open the app
http://localhost:8000


---

## How to Use

**Basic usage - diagnose latest failure:**
1. Enter your GitHub repository name (format: `username/repo-name`)
2. Leave Run ID blank
3. Click "Diagnose Pipeline"
4. App finds the latest failed run automatically

**Diagnose a specific run:**
1. Go to GitHub Actions tab on your repo
2. Click a failed run
3. Copy the Run ID from the URL: `github.com/user/repo/actions/runs/12345678`
4. Enter repo name and Run ID in Pipeline Doctor
5. Click "Diagnose Pipeline"

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web UI |
| GET | `/health` | Health check |
| POST | `/diagnose` | Diagnose a pipeline failure |


---

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes |
| `GITHUB_TOKEN` | GitHub Personal Access Token | Yes |

---

## Docker

### Build image

```bash
docker build -t pipeline-doctor:latest .
```

### Run container

```bash
docker run -d \
  --name pipeline-doctor \
  -p 8000:8000 \
  -e GEMINI_API_KEY=your-key \
  -e GITHUB_TOKEN=your-token \
  pipeline-doctor:latest
```

### Using Docker Compose

```bash
docker-compose up -d --build
```

---

## CI/CD Pipeline

This project uses GitHub Actions for automated testing and deployment.

Pipeline stages:
1. Run unit tests
2. Security scan with Trivy
3. Build Docker image
4. Push to Docker Hub
5. Deploy to AWS EC2

---


## Future Improvements

- Add support for private repositories
- Real-time log streaming from GitHub API
- Multiple pipeline comparison
- Slack/Discord notifications
- Historical diagnosis dashboard
- Support for GitLab and Bitbucket pipelines
- Export diagnosis report as PDF

---

## Author

**Moin Khadri Syed** - MSc Software Engineering Student, UK

- GitHub: [moinkhadris-star](https://github.com/moinkhadris-star)
- LinkedIn: [Moin Khadri Syed](https://www.linkedin.com/in/moin-khadri-syed/)
---
