"""Centralized configuration management for all skills"""
import os
from typing import Any, Optional
from dotenv import load_dotenv


class ConfigManager:
    """Manages configuration for OpenClaw skills
    
    Singleton pattern ensures consistent config across all skills.
    Loads from config.env and .env files.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        # Load environment variables from both config files
        load_dotenv('config.env')
        load_dotenv('.env')
        
        self._config = {}
        self._load_config()
        self._initialized = True
    
    def _load_config(self):
        """Load configuration from environment variables"""
        # Database configs
        self._config['neo4j_uri'] = os.getenv('NEO4J_URI', 'bolt://192.168.1.79:7687')
        self._config['neo4j_user'] = os.getenv('NEO4J_USER', 'neo4j')
        self._config['neo4j_password'] = os.getenv('NEO4J_PASSWORD', 'fishing_hero_2025')
        
        # AI model configs
        self._config['embed_model'] = os.getenv('EMBED_MODEL', 'shibing624/text2vec-base-chinese')
        self._config['hf_endpoint'] = os.getenv('HF_ENDPOINT', 'https://hf-mirror.com')
        
        # API keys
        self._config['google_ai_api_key'] = os.getenv('GOOGLE_AI_API_KEY', '')
        self._config['polo_api_key'] = os.getenv('POLO_API_KEY', '')
        
        # WeChat config
        self._config['wx_appid'] = os.getenv('WX_APPID', 'wxcea48780209aa522')
        self._config['wx_appsecret'] = os.getenv('WX_APPSECRET', '')
        
        # Timezone
        self._config['timezone'] = os.getenv('TZ', 'Asia/Shanghai')
        
        # Transformers config
        self._config['transformers_offline'] = os.getenv('TRANSFORMERS_OFFLINE', '0')
        self._config['hf_hub_download_timeout'] = os.getenv('HF_HUB_DOWNLOAD_TIMEOUT', '300')
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value (runtime only, not persisted)
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self._config[key] = value
    
    def get_all(self) -> dict:
        """Get all configuration as a dictionary
        
        Returns:
            Copy of all configuration values
        """
        return self._config.copy()
    
    def has(self, key: str) -> bool:
        """Check if configuration key exists
        
        Args:
            key: Configuration key
            
        Returns:
            True if key exists, False otherwise
        """
        return key in self._config


# Singleton instance for easy import
config = ConfigManager()
