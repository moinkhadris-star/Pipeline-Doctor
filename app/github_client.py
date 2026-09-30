from github import Github
from dotenv import load_dotenv
import os

load_dotenv()

class GitHubClient:
    def __init__(self):
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise ValueError("GITHUB_TOKEN not found in .env file")
        self.client = Github(token)
    
    def get_latest_failed_run(self, repo_name: str):
        """Get the most recent failed pipeline run"""
        try:
            repo = self.client.get_repo(repo_name)
            
            # Get all workflow runs
            runs = repo.get_workflow_runs()
            
            # Find latest failed run
            for run in runs:
                if run.conclusion == "failure":
                    return run
            
            return None
        
        except Exception as e:
            raise Exception(f"Could not fetch runs for {repo_name}: {str(e)}")
    
    def get_run_by_id(self, repo_name: str, run_id: int):
        """Get a specific pipeline run by ID"""
        try:
            repo = self.client.get_repo(repo_name)
            return repo.get_workflow_run(run_id)
        except Exception as e:
            raise Exception(f"Could not fetch run {run_id}: {str(e)}")
    
    def get_run_logs_summary(self, run) -> dict:
        """Extract useful info from a pipeline run"""
        try:
            # Get failed jobs
            jobs = run.jobs()
            failed_jobs = []
            
            for job in jobs:
                if job.conclusion == "failure":
                    failed_steps = []
                    
                    for step in job.steps:
                        if step.conclusion == "failure":
                            failed_steps.append({
                                "step_name": step.name,
                                "number": step.number
                            })
                    
                    failed_jobs.append({
                        "job_name": job.name,
                        "failed_steps": failed_steps,
                        "html_url": job.html_url
                    })
            
            return {
                "run_id": run.id,
                "run_name": run.name,
                "status": run.status,
                "conclusion": run.conclusion,
                "branch": run.head_branch,
                "commit_message": run.head_commit.message,
                "created_at": str(run.created_at),
                "html_url": run.html_url,
                "failed_jobs": failed_jobs,
                "total_jobs": run.jobs().totalCount
            }
        
        except Exception as e:
            raise Exception(f"Could not extract log summary: {str(e)}")
    
    def test_connection(self):
        """Test GitHub API connection works"""
        try:
            user = self.client.get_user()
            return f"Connected as: {user.login}"
        except Exception as e:
            return f"Connection failed: {str(e)}"