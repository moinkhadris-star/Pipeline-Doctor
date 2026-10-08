import google.generativeai as genai
from dotenv import load_dotenv
from app.github_client import GitHubClient
import os
import json
import asyncio

load_dotenv()

class PipelineDoctorAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        genai.configure(api_key=api_key)
        self.llm = genai.GenerativeModel("gemini-3.5-flash")
        self.github = GitHubClient()
    
    def _build_prompt(self, run_summary: dict) -> str:
        return f"""
You are Pipeline Doctor, an expert DevOps AI agent.
Analyse this CI/CD pipeline failure and diagnose it.

PIPELINE DETAILS:
Pipeline: {run_summary['run_name']}
Branch: {run_summary['branch']}
Commit: {run_summary['commit_message']}
Failed at: {run_summary['created_at']}

FAILED JOBS:
{json.dumps(run_summary['failed_jobs'], indent=2)}

Respond with ONLY this JSON, no other text:
{{
    "diagnosis": "What went wrong in 2-3 sentences.",
    "suggestion": "1. Step one. 2. Step two. 3. Step three.",
    "confidence": "high/medium/low",
    "category": "dependency/configuration/test/build/other"
}}
"""

    def _call_gemini(self, prompt: str) -> str:
        response = self.llm.generate_content(prompt)
        return response.text.strip()

    async def diagnose(self, repo_name: str, run_id: int = None) -> dict:
        
        print(f"Fetching pipeline data for {repo_name}...")
        
        if run_id:
            run = self.github.get_run_by_id(repo_name, run_id)
        else:
            run = self.github.get_latest_failed_run(repo_name)
        
        if not run:
            return {
                "repo": repo_name,
                "status": "no_failures",
                "pipeline_name": "",
                "branch": "",
                "failed_at": "",
                "pipeline_url": "",
                "diagnosis": "No failed pipeline runs found.",
                "suggestion": "All recent pipelines passed successfully!",
                "confidence": "high"
            }
        
        print("Extracting failure details...")
        run_summary = self.github.get_run_logs_summary(run)
        
        print("AI agent analysing failure...")
        prompt = self._build_prompt(run_summary)

        loop = asyncio.get_running_loop()
        ai_response = await loop.run_in_executor(
            None,
            self._call_gemini,
            prompt
        )
        
        # Clean markdown if present
        if "```" in ai_response:
            parts = ai_response.split("```")
            if len(parts) >= 2:
                ai_response = parts[1]
                if ai_response.startswith("json"):
                    ai_response = ai_response[4:]
        
        ai_response = ai_response.strip()
        
        try:
            diagnosis_data = json.loads(ai_response)
        except json.JSONDecodeError:
            diagnosis_data = {
                "diagnosis": ai_response,
                "suggestion": "Check pipeline logs manually.",
                "confidence": "low",
                "category": "other"
            }
        
        print("Diagnosis complete!")
        return {
            "repo": repo_name,
            "status": run_summary['conclusion'],
            "pipeline_name": run_summary['run_name'],
            "branch": run_summary['branch'],
            "failed_at": run_summary['created_at'],
            "pipeline_url": run_summary['html_url'],
            "diagnosis": diagnosis_data.get("diagnosis", "Unable to diagnose"),
            "suggestion": diagnosis_data.get("suggestion", "Check logs manually"),
            "confidence": diagnosis_data.get("confidence", "low")
        }