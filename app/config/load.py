from .schema import LinkedInConfig, AppConfig
from typing import Optional
# import dotenv
import os
import logging
from os.path import join, dirname

# dotEnv_dir = join(dirname(__file__), '..', '..', '.env')

conf_logger: logging.Logger = logging.getLogger(__name__)
# conf_logger.info(f"---------------------------- Here -----------------------------{dotEnv_dir}")
# print(f"---------------------------- Here -----------------------------{dotEnv_dir}")
def load_credentials_from_env(config: AppConfig) -> AppConfig:
    # dotenv.load_dotenv(dotEnv_dir)

    config.linkedIn.login_email = os.environ.get("LINKEDIN_ID")
    config.linkedIn.login_password = os.environ.get("LINKEDIN_PASSWORD")
    return config

def load_overleaf_credsentials_from_env(config: AppConfig) -> AppConfig:
    """Load Overleaf credentials from environment variables."""
    config.overleaf.email = os.environ.get("OVERLEAF_EMAIL")
    config.overleaf.password = os.environ.get("OVERLEAF_PASSWORD")
    
    if not config.overleaf.email or not config.overleaf.password:
        conf_logger.warning("Overleaf credentials are not set in the environment variables.")
    
    return config
