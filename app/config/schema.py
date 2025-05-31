from dataclasses import dataclass, field
from typing import Optional, List, Literal

@dataclass
class ChromeConfig:
    """Configuration for Chrome driver."""

    headless: bool = True
    chromedriver_path: Optional[str] = None
    browser_args: List[str] = field(default_factory=list)
    non_interactive: bool = False

@dataclass
class LinkedInConfig:
    """Configuration for LinkedIn scraping."""
    
    login_email: Optional[str] = None
    login_password: Optional[str] = None
    scrape_delay: int = 2  # Delay in seconds between actions

@dataclass
class OverleafConfig:
    """Configuration for Overleaf API."""
    
    email: Optional[str] = None
    password: Optional[str] = None

@dataclass
class AppConfig:
    "Main configuration class for the application."
    # chrome: ChromeConfig = field(default_factory=ChromeConfig)
    linkedIn: LinkedInConfig = field(default_factory=LinkedInConfig)
    overleaf: OverleafConfig = field(default_factory=OverleafConfig)

