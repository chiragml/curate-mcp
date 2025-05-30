from mcp.server.fastmcp import FastMCP
from drivers.chrome import active_drivers, close_driver
from typing import Any, Dict, List
from scrape import scrape_posting
from config import reset_config
import dotenv
import logging
import time
import sys
# Configure logging to stderr
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)


LOGGER = None

def set_logger(logger: logging.Logger) -> None:
    global LOGGER
    LOGGER = logger

set_logger(logging.getLogger(__name__))

def get_logger() -> logging.Logger:
    """
    Get a logger instance for the application.

    If no logger is provided, a new logger is created with the name 'curate-mcp'.
    """
    
    return LOGGER



app = FastMCP("curate-mcp")

OVERLEAFCRED = None

scrape_posting(app, get_logger())

@app.tool()
async def close_session() -> Dict[str, Any]:
    """Close the current browser session and clean up resources."""
    session_id = "default"  # Using the same default session

    if session_id in active_drivers:
       reset_config()  # Reset configuration to default
       time.sleep(1)  # Allow time for reset
       close_driver(session_id)
    else:
        return {
            "status": "warning",
            "message": "No active browser session to close",
        }


@app.tool()
def customize(content: str, login_cred = OVERLEAFCRED) -> str:
    '''
    Tool call for customizing a resume based on scraped data.
    --------------------------
    Parameters:
    content: str
        The scraped job post content to customize the resume with.
    login_cred: str
        The credentials for Overleaf to customize the resume
    
    --------------------------
    Returns:
    str
        The customized resume content.
    --------------------------
    '''
    # Tool call for customizing resume based on scraped data
    raise NotImplementedError("Customization functionality is not implemented yet.")

@app.prompt()
def __validate__(resume: str, job: dict) -> str:
    """
    Make sure that the resume is properly tailored to the job post.

    --------------------------
    Parameters:
    resume: str
        The resume to be validated.
    job_post: str
        The job post to validate against.
    --------------------------
    Returns:
    str
        How much more does the resume needs to be customized.
    """
    res = f"Review my attached resume and suggest targeted improvements for the {job.job_description} at {job.company}.\n" +\
            "Highlight specific sections that need changes and provide detailed suggestions.\n" +\
            "Focus on tailoring the resume to the job description and company culture.\n" +\
            "Ensure the resume aligns with the job requirements and showcases relevant skills.\n" +\
            "Provide actionable feedback to enhance the resume's effectiveness for <|Project|> and <|Experience|> sections.\n" 
    
    return res    