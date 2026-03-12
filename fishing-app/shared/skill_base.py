"""Base class for all OpenClaw skills"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime


class SkillBase(ABC):
    """Base class that all skills inherit from"""
    
    def __init__(self, skill_name: str, version: str = "1.0.0"):
        self.skill_name = skill_name
        self.version = version
        self.initialized_at = datetime.now()
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the skill's main functionality
        
        Args:
            **kwargs: Skill-specific parameters
            
        Returns:
            Dict containing execution results
        """
        pass
    
    def get_metadata(self) -> Dict[str, Any]:
        """Return skill metadata
        
        Returns:
            Dict with skill name, version, and initialization time
        """
        return {
            "name": self.skill_name,
            "version": self.version,
            "initialized_at": self.initialized_at.isoformat()
        }
    
    def validate_params(self, required_params: list, provided_params: dict) -> None:
        """Validate required parameters are provided
        
        Args:
            required_params: List of required parameter names
            provided_params: Dict of provided parameters
            
        Raises:
            ValueError: If any required parameters are missing
        """
        missing = [p for p in required_params if p not in provided_params]
        if missing:
            raise ValueError(f"Missing required parameters: {', '.join(missing)}")
