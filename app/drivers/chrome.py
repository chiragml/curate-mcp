# import undetected_chromedriver as uc
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.common.exceptions import WebDriverException
# from typing import Dict
# import random
# import time

# # Automatically downloads and manages ChromeDriver
# service = Service(ChromeDriverManager().install())
# # driver = webdriver.Chrome(service=service)

# # Configure Chrome options for stealth mode


# active_drivers: Dict[str, webdriver.Chrome] = {}



# def get_or_create_driver(session_id: str = "default", headless: bool = False) -> webdriver.Chrome:
#     """
#     Get or create a Chrome WebDriver instance with stealth mode enabled.

#     Parameters:
#     session_id (str): Identifier for the browser session. Defaults to "default".

#     Returns:
#     webdriver.Chrome: Configured Chrome WebDriver instance.
#     """
#     global active_drivers

#     if session_id in active_drivers:
#         return active_drivers[session_id]
#     chrome_options = Options()
#     # Essential stealth arguments
#     chrome_options.add_argument('--disable-blink-features=AutomationControlled')
#     chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     chrome_options.add_experimental_option('useAutomationExtension', False)
#     # Additional stealth configurations
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     chrome_options.add_argument('--disable-web-security')
#     chrome_options.add_argument('--disable-features=VizDisplayCompositor')
#     chrome_options.add_argument('--disable-logging')
#     chrome_options.add_argument('--log-level=3')
#     chrome_options.add_argument('--silent')

#     # Additional GPU-related disables
#     chrome_options.add_argument('--disable-accelerated-2d-canvas')
#     chrome_options.add_argument('--disable-accelerated-jpeg-decoding')
#     chrome_options.add_argument('--disable-accelerated-mjpeg-decode')
#     chrome_options.add_argument('--disable-accelerated-video-decode')
#     chrome_options.add_argument('--disable-gpu-sandbox')
#     chrome_options.add_argument(" --enable-unsafe-swiftshader")
#     # Randomized window size
#     chrome_options.add_argument('--window-size=1920,1080')
#     chrome_options.add_argument('--start-maximized')

#     # Set a realistic user agent
#     # User agent rotation
#     user_agents = [
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
#     ]
#     chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')
#     if headless:
#         chrome_options.add_argument('--headless')

#     try:
#     # Create a new Chrome driver with the specified options
#         driver = webdriver.Chrome(service=service, options=chrome_options)
#     except Exception as e:
#         raise WebDriverException(e)
#     # Store the driver in the active drivers dictionary
#     driver.set_page_load_timeout(60)
#     active_drivers[session_id] = driver

#     # Allow some time for the driver to initialize
#     time.sleep(2)
#     return driver  

# def close_driver(session_id: str = "default") -> None:
#     """
#     Close the Chrome WebDriver instance for the given session ID.

#     Parameters:
#     session_id (str): Identifier for the browser session. Defaults to "default".
#     """
#     global active_drivers

#     if session_id in active_drivers:
#         driver = active_drivers[session_id]
#         driver.quit()
#         del active_drivers[session_id]
#     else:
#         print(f"No active driver found for session ID: {session_id}")


import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from typing import Dict, Union
import random
import time

# Support both driver types
active_drivers: Dict[str, Union[webdriver.Chrome, uc.Chrome]] = {}

def get_or_create_driver(
    session_id: str = "default", 
    headless: bool = False,
    use_undetected: bool = True  # New parameter
) -> Union[webdriver.Chrome, uc.Chrome]:
    """
    Get or create a Chrome WebDriver instance.
    
    Parameters:
    session_id (str): Identifier for the browser session
    headless (bool): Whether to run in headless mode
    use_undetected (bool): Whether to use undetected-chromedriver
    """
    global active_drivers

    if session_id in active_drivers:
        return active_drivers[session_id]
    
    if use_undetected:
        # Use undetected-chromedriver
        chrome_options = uc.ChromeOptions()
        
        # Basic options
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--start-maximized')
        
        if headless:
            chrome_options.add_argument('--headless')
        
        driver = uc.Chrome(options=chrome_options, version_main=None)
        
    else:
        # Use regular selenium
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        # Additional stealth configurations
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--silent')

        # Additional GPU-related disables
        chrome_options.add_argument('--disable-accelerated-2d-canvas')
        chrome_options.add_argument('--disable-accelerated-jpeg-decoding')
        chrome_options.add_argument('--disable-accelerated-mjpeg-decode')
        chrome_options.add_argument('--disable-accelerated-video-decode')
        chrome_options.add_argument('--disable-gpu-sandbox')
        chrome_options.add_argument(" --enable-unsafe-swiftshader")
        # Randomized window size
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--start-maximized')
        
        if headless:
            chrome_options.add_argument('--headless')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.set_page_load_timeout(60)
    active_drivers[session_id] = driver
    time.sleep(2)
    
    return driver

def close_driver(session_id: str = "default") -> None:
    """
    Close the Chrome WebDriver instance for the given session ID.

    Parameters:
    session_id (str): Identifier for the browser session. Defaults to "default".
    """
    global active_drivers

    if session_id in active_drivers:
        driver = active_drivers[session_id]
        driver.quit()
        del active_drivers[session_id]
    else:
        print(f"No active driver found for session ID: {session_id}")










