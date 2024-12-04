import os
from typing import Dict, Any
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

class Config:
    """Simplified configuration management"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    
    # System Configuration
    DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    WORK_DIR = os.getenv("WORK_DIR", "./coding")
    
    @classmethod
    def get_openai_config(cls) -> Dict[str, Any]:
        """Get OpenAI configuration"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
            
        return {
            "temperature": cls.OPENAI_TEMPERATURE,
            "config_list": [{
                "model": cls.OPENAI_MODEL,
                "api_key": cls.OPENAI_API_KEY,
            }]
        }
    
    @classmethod
    def get_logging_config(cls) -> Dict[str, Any]:
        """Get logging configuration"""
        return {
            "level": getattr(logging, cls.LOG_LEVEL.upper()),
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    
    @classmethod
    def initialize(cls) -> None:
        """Initialize and validate configuration"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        if cls.DEBUG_MODE:
            print("\n=== Configuration ===")
            print(f"Model: {cls.OPENAI_MODEL}")
            print(f"Temperature: {cls.OPENAI_TEMPERATURE}")
            print(f"Work Directory: {cls.WORK_DIR}")
            print("===================\n")

# Initialize configuration
Config.initialize() 