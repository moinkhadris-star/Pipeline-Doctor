from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from app.agent import PipelineDoctorAgent
import uvicorn

app = FastAPI(
    title="Pipeline Doctor",
    description="AI agent that diagnoses CI/CD pipeline failures",
    version="1.0.0"
)

# Request model
class DiagnoseRequest(BaseModel):
    repo_name: str      # e.g. "username/repo-name"
    run_id: int = None  # optional specific run, latest if None

# Response model
class DiagnoseResponse(BaseModel):
    repo: str
    status: str
    pipeline_name: str = ""
    branch: str = ""
    failed_at: str = ""
    pipeline_url: str = ""
    diagnosis: str
    suggestion: str
    confidence: str

@app.get("/", response_class=HTMLResponse)
async def home():
    with open("app/templates/index.html", encoding="utf-8") as f:
        return f.read()

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "Pipeline Doctor"}

@app.post("/diagnose", response_model=DiagnoseResponse)
async def diagnose(request: DiagnoseRequest):
    try:
        agent = PipelineDoctorAgent()
        result = await agent.diagnose(request.repo_name, request.run_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)