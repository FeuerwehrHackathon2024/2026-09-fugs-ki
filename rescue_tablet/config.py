"""
Configuration for Rescue Tablet API integration.
"""

import os

from rescue_tablet.tools.env import get_api_config
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    # Host und Port des RescueTablet-Servers
    rescue_tablet_host: str

    # Security-Header (Name und Wert aus den RescueTablet-Einstellungen)
    rescue_tablet_security_header_name: str = "RT-Security-Token"
    rescue_tablet_security_header_value: str

    # Statischer Bearer-Token
    rescue_tablet_bearer_token: str

    # SSL-Zertifikat prüfen (false bei selbst-signierten Zertifikaten)
    rescue_tablet_verify_ssl: bool = False

    # User-Agent Header
    rescue_tablet_user_agent: str = "insomnia/12.5.0"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

API_CONFIG = get_api_config()

def get_config(environment="development"):
    """Retrieve the configuration for the specified environment."""
    return API_CONFIG.get(environment, {})