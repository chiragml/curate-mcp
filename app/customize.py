import pyoverleaf
from drivers.chrome import get_or_create_driver, close_driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from mcp.server.fastmcp import FastMCP
from config import get_config
import logging
import time

def customize(mcp: FastMCP, logger: logging.Logger) -> None:
    """Customize the MCP server with Overleaf integration."""
    api = None
    
    def __create_pyoverleaf_api__() -> None:
        """Create pyoverleaf API instance using your driver"""
        nonlocal api
        if api is not None:
            return api
        driver = get_or_create_driver("overleaf_auth" , headless=False, use_undetected=True)
        overleaf_config = get_config().overleaf
        email = overleaf_config.email
        password = overleaf_config.password
        logger.info(f"Using Overleaf credentials: {email} {password}")
        try:
            # Login
            driver.get("https://www.overleaf.com/login")
            wait = WebDriverWait(driver, 20)
            
            # Fill credentials
            wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(email)
            driver.find_element(By.NAME, "password").send_keys(password)
            driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
            
            # Wait for login
            wait.until(EC.url_contains("/project"))
            
            # Get session cookie
            cookies = driver.get_cookies()
            session_cookie = next(
                (c['value'] for c in cookies if c['name'] == 'overleaf_session2'), 
                None
            )
            
            # Create pyoverleaf API with the cookie
            api = pyoverleaf.Api()
            api.session.cookies.set('overleaf_session2', session_cookie)
            
            
        except Exception as e:
            close_driver("overleaf_auth")
            raise e

    # Usage

    """
    TODO: The dirver is able to log in but is able to log in but there seems to be an issue with fetching the projects. something to do with session.
    Figure out what that is and fixing it should be easy enough.
    """

    @mcp.tool()
    def get_overleaf_projects():
        __create_pyoverleaf_api__()
        time.sleep(2)
        """Get all projects from Overleaf"""
        try:
            projects = api.projects.list()
            return [project.to_dict() for project in projects]
        except Exception as e:
            print(f"Error fetching projects: {e}")
            return []