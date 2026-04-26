"""
Environment configuration tools for Rescue Tablet.
"""

import os

def get_api_config():
    """Retrieve API configuration from environment variables."""
    return {
        "production": {
            "base_url": os.getenv("RESCUE_TABLET_PROD_URL", "https://missions-api.rescuetablet.com/"),
            "api_key": os.getenv("RESCUE_TABLET_PROD_KEY", ""),
        },
        "development": {
            "base_url": os.getenv("RESCUE_TABLET_DEV_URL", "https://missions-api-dev.rescuetablet.com/"),
            "api_key": os.getenv("RESCUE_TABLET_DEV_KEY", ""),
        },
    }