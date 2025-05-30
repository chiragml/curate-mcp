'''
Getting and resetting the configuration for the application.
'''
from typing import Optional
from .load import load_credentials_from_env
from .schema import AppConfig
import logging

conf_logger: logging.Logger = logging.getLogger(__name__)

_config: Optional[AppConfig] = None

def get_config() -> AppConfig:
    """
    Get the current application configuration.

    Returns:
        AppConfig: The current application configuration.
    """
    
    global _config
    if _config is None:
        _config = AppConfig()
        _config = load_credentials_from_env(_config)
        
        if _config.linkedIn.login_email is None or _config.linkedIn.login_password is None:
            raise ValueError("LinkedIn credentials are not set. Please set LINKEDIN_ID and LINKEDIN_PASSWORD in your environment variables.")
    return _config

def reset_config() -> None:
    """
    Reset the application configuration to its default state.
    """
    global _config
    _config = None
    get_config()  # Reinitialize to load environment variables again   
