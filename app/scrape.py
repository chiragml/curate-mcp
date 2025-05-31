"""
Job-related tools for LinkedIn MCP server.

This module provides tools for scraping LinkedIn job postings and searches.
"""

from typing import Any, Dict, List

from linkedin_scraper import Job, actions
from mcp.server.fastmcp import FastMCP
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import logging
from drivers.chrome import get_or_create_driver, close_driver
from config import get_config, conf_logger
import time

def scrape_posting(mcp: FastMCP, logger: logging.Logger) -> None:
    """
    Scrape a job posting from LinkedIn.

    --------------------------
    Parameters:
    mcp: FastMCP
        The MCP server instance to use for scraping.
    --------------------------
    """
    global conf_logger
    conf_logger = logger
    @mcp.tool()
    def scrape_job_posting_linkedIn(url: str) -> Dict[str, Any]:
        """
        Scrape job details from a LinkedIn job posting.
        """
        driver = None
        try:
            driver = get_or_create_driver()
            config = get_config()
            
            logger.info(f"Starting LinkedIn job scraping for: {url}")
            
            # Attempt login with timeout protection
            try:
                # Set a timeout for the entire login process
                driver.set_page_load_timeout(30)
                login_with_retry(driver, config.linkedIn.login_email, config.linkedIn.login_password)
                
            except ValueError as ve:
                # Specific error messages (verification, CAPTCHA, etc.)
                # error_msg = str(ve)
                # logger.error(f"Login failed with known issue: {error_msg}")
                # time.sleep(5)  # Allow time for user to manually resolve issues
                
                # Return error without crashing
                return {
                    "status": "error",
                    "message": "Please login to LinkedIn manually in a regular browser first to verify your account."
                }
                
            except Exception as e:
                # Generic login failure
                logger.error(f"Login failed: {e}")
                return {
                    "error": f"Failed to log in to LinkedIn: {str(e)}",
                    "status": "login_failed"
                }
            
            # Proceed with scraping
            try:
                logger.info(f"Scraping job: {url}")
                
                # Add timeout for job scraping too
                driver.set_page_load_timeout(20)
                
                job = Job(url, driver=driver, close_on_complete=False)
                result = job.to_dict()
                
                logger.info("Job scraping successful")
                return result
                
            except Exception as e:
                logger.error(f"Error scraping job: {e}")
                return {
                    "error": f"Failed to scrape job posting: {str(e)}",
                    "status": "scraping_failed"
                }
                
        except Exception as e:
            logger.error(f"Unexpected error in scrape_job_posting_linkedIn: {e}")
            return {
                "error": f"Unexpected error: {str(e)}",
                "status": "unexpected_error"
            }
        finally:
            # Don't close the driver here if you want to reuse it
            pass

    def login_with_retry(driver, email: str, password: str, max_attempts: int = 3) -> None:
        """
        Attempt to log in to LinkedIn with retries and verification detection.
        """
        for attempt in range(max_attempts):
            try:
                logger.info(f"Login attempt {attempt + 1}...")
                
                # Navigate to LinkedIn
                driver.get("https://www.linkedin.com/login")
                time.sleep(3)
                
                wait = WebDriverWait(driver, 30)
                
                # Find and fill email field
                email_field = wait.until(
                    EC.presence_of_element_located((By.ID, "username"))
                )
                email_field.clear()
                email_field.send_keys(email)
                time.sleep(1)
                
                # Find and fill password field
                password_field = wait.until(
                    EC.presence_of_element_located((By.ID, "password"))
                )
                password_field.clear()
                password_field.send_keys(password)
                time.sleep(1)
                
                # Click login button
                login_button = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
                )
                login_button.click()
                
                # Wait for page to load after login
                time.sleep(5)
                
                # Check what page we're on
                current_url = driver.current_url
                page_source = driver.page_source.lower()
                
                # Check for verification requirement
                if any(indicator in page_source for indicator in [
                    "verify your identity",
                    "verification code",
                    "suspicious activity",
                    "verify your account",
                    "confirm it's you",
                    "security verification",
                    "let's do a quick security check"
                ]):
                    logger.warning("LinkedIn is requesting verification")
                    raise ValueError("LinkedIn requires email/phone verification. Please login manually once to establish trust.")
                
                # Check for CAPTCHA
                if "captcha" in page_source or "security check" in page_source:
                    logger.warning("CAPTCHA detected")
                    raise ValueError("LinkedIn is showing a CAPTCHA. Please login manually to bypass.")
                
                # Check if we're on the feed
                if "feed" in current_url or "in/" in current_url:
                    logger.info("Login successful!")
                    return True
                
                # Try to detect feed element with shorter timeout
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test-id='feed']"))
                    )
                    logger.info("Login successful!")
                    return True
                except:
                    # Feed not found, but let's check if we're logged in anyway
                    if "linkedin.com/in/" in current_url or "linkedin.com/feed" in current_url:
                        logger.info("Login appears successful")
                        return True
                    else:
                        logger.warning(f"Unexpected page after login: {current_url}")
                        raise ValueError(f"Login failed - unexpected page: {current_url}")
                    
            except ValueError as ve:
                # Re-raise ValueError to exit early
                raise ve
                
            except Exception as e:
                logger.error(f"Login attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_attempts - 1:
                    logger.info("Retrying...")
                    time.sleep(5)
                else:
                    raise ValueError(f"Failed to log in after {max_attempts} attempts: {str(e)}")
        
        return False