"""OpenClaw Configuration Loader"""
import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path


class ConfigLoader:
    """Load and manage OpenClaw configuration"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize config loader
        
        Args:
            config_path: Path to openclaw.yaml, defaults to project root
        """
        if config_path is None:
            # Default to openclaw.yaml in project root
            project_root = Path(__file__).parent.parent
            config_path = project_root / "openclaw.yaml"
        
        self.config_path = Path(config_path)
        self._config: Optional[Dict[str, Any]] = None
        
    def load(self) -> Dict[str, Any]:
        """Load configuration from YAML file
        
        Returns:
            Configuration dictionary
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Expand environment variables
        config = self._expand_env_vars(config)
        
        self._config = config
        return config
    
    def _expand_env_vars(self, obj: Any) -> Any:
        """Recursively expand environment variables in config
        
        Args:
            obj: Configuration object (dict, list, str, etc.)
            
        Returns:
            Object with environment variables expanded
        """
        if isinstance(obj, dict):
            return {k: self._expand_env_vars(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._expand_env_vars(item) for item in obj]
        elif isinstance(obj, str):
            # Expand ${VAR} or ${VAR:-default}
            if obj.startswith('${') and obj.endswith('}'):
                var_expr = obj[2:-1]
                
                # Handle default value: ${VAR:-default}
                if ':-' in var_expr:
                    var_name, default = var_expr.split(':-', 1)
                    return os.getenv(var_name, default)
                else:
                    return os.getenv(var_expr, obj)
            return obj
        else:
            return obj
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'api.base_url')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        if self._config is None:
            self.load()
        
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration
        
        Returns:
            Complete configuration dictionary
        """
        if self._config is None:
            self.load()
        
        return self._config
    
    def get_skills(self) -> list:
        """Get enabled skills configuration
        
        Returns:
            List of enabled skill configurations
        """
        skills = self.get('skills', [])
        return [s for s in skills if s.get('enabled', True)]
    
    def get_skill(self, name: str) -> Optional[Dict[str, Any]]:
        """Get specific skill configuration
        
        Args:
            name: Skill name
            
        Returns:
            Skill configuration or None if not found
        """
        skills = self.get_skills()
        for skill in skills:
            if skill.get('name') == name:
                return skill
        return None
    
    def get_cron_jobs(self) -> list:
        """Get enabled cron jobs
        
        Returns:
            List of enabled cron job configurations
        """
        jobs = self.get('cron_jobs', [])
        return [j for j in jobs if j.get('enabled', True)]
    
    def get_monitoring_alerts(self) -> list:
        """Get monitoring alert configurations
        
        Returns:
            List of alert configurations
        """
        return self.get('monitoring.alerts', [])


# Global config instance
_config_instance: Optional[ConfigLoader] = None


def get_config() -> ConfigLoader:
    """Get global config instance
    
    Returns:
        ConfigLoader instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigLoader()
        _config_instance.load()
    return _config_instance


def reload_config():
    """Reload configuration from file"""
    global _config_instance
    if _config_instance is not None:
        _config_instance.load()
