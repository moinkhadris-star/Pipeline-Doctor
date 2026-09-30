from openai import OpenAI
from dotenv import load_dotenv
from app.github_client import GitHubClient
import os
import json

load_dotenv()

class PipelineDoctorAgent:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in .env file")
        
        self.llm = OpenAI(api_key=api_key)
        self.github = GitHubClient()
    
    def _build_prompt(self, run_summary: dict) -> str:
        """Build the prompt for the AI agent"""
        return f"""
You are Pipeline Doctor, an expert DevOps AI agent.
Your job is to analyse CI/CD pipeline failures and 
provide clear, actionable diagnosis.

PIPELINE FAILURE DETAILS:
========================
Repository Run: {run_summary['run_name']}
Branch: {run_summary['branch']}
Commit Message: {run_summary['commit_message']}
Failed at: {run_summary['created_at']}

FAILED JOBS:
{json.dumps(run_summary['failed_jobs'], indent=2)}

YOUR TASK:
Analyse this pipeline failure and respond with ONLY 
a valid JSON object in this exact format:

{{
    "diagnosis": "Clear explanation of what went wrong in 2-3 sentences. Be specific about the failure.",
    "suggestion": "Specific steps to fix this. Number each step. Be practical and actionable.",
    "confidence": "high/medium/low",
    "category": "dependency/configuration/test/build/deployment/permission/timeout/other"
}}

Be specific, practical and concise.
Respond with ONLY the JSON. No other text.
"""
    
    async def diagnose(self, repo_name: str, run_id: int = None) -> dict:
        """Main method - diagnose a pipeline failure"""
        
        # Step 1: Get the pipeline run
        print(f"🔍 Fetching pipeline data for {repo_name}...")
        
        if run_id:
            run = self.github.get_run_by_id(repo_name, run_id)
        else:
            run = self.github.get_latest_failed_run(repo_name)
        
        if not run:
            return {
                "repo": repo_name,
                "status": "no_failures",
                "diagnosis": "No failed pipeline runs found.",
                "suggestion": "All recent pipelines passed successfully!",
                "confidence": "high"
            }
        
        # Step 2: Extract log summary
        print("📋 Extracting failure details...")
        run_summary = self.github.get_run_logs_summary(run)
        
        # Step 3: Send to AI for diagnosis
        print("🤖 AI agent analysing failure...")
        prompt = self._build_prompt(run_summary)
        
        response = self.llm.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are Pipeline Doctor, an expert DevOps AI agent. Always respond with valid JSON only."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        # Step 4: Parse AI response
        ai_response = response.choices[0].message.content.strip()
        
        try:
            diagnosis_data = json.loads(ai_response)
        except json.JSONDecodeError:
            diagnosis_data = {
                "diagnosis": ai_response,
                "suggestion": "Please check the pipeline logs manually.",
                "confidence": "low",
                "category": "other"
            }
        
        # Step 5: Return complete result
        print("✅ Diagnosis complete!")
        return {
            "repo": repo_name,
            "status": run_summary['conclusion'],
            "diagnosis": diagnosis_data.get("diagnosis", "Unable to diagnose"),
            "suggestion": diagnosis_data.get("suggestion", "Check logs manually"),
            "confidence": diagnosis_data.get("confidence", "low")
        }