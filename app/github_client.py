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
        try:
            repo = self.client.get_repo(repo_name)
            runs = repo.get_workflow_runs(status="failure")
            for run in runs:
                return run  # Return first one immediately
            return None
        except Exception as e:
            raise Exception(f"Could not fetch runs for {repo_name}: {str(e)}")
    
    def get_run_by_id(self, repo_name: str, run_id: int):
        try:
            repo = self.client.get_repo(repo_name)
            return repo.get_workflow_run(run_id)
        except Exception as e:
            raise Exception(f"Could not fetch run {run_id}: {str(e)}")
    
    def get_run_logs_summary(self, run) -> dict:
        try:
            # Only fetch jobs ONCE and store it
            jobs_list = list(run.jobs())
            failed_jobs = []
            
            for job in jobs_list:
                if job.conclusion == "failure":
                    failed_jobs.append({
                        "job_name": job.name,
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
                "total_jobs": len(jobs_list)
            }
        
        except Exception as e:
            raise Exception(f"Could not extract log summary: {str(e)}")

    def test_connection(self):
        try:
            user = self.client.get_user()
            return f"Connected as: {user.login}"
        except Exception as e:
            return f"Connection failed: {str(e)}"