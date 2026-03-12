"""Fishing Coach Service - Wraps AdvancedFishingAgentV4"""
from typing import Dict, Any, Optional
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from shared import SkillBase, ResponseFormatter
from advanced_agent_v4_reasoning import AdvancedFishingAgentV4


class FishingCoachService(SkillBase):
    """Fishing coach service providing AI-powered fishing advice
    
    Wraps the AdvancedFishingAgentV4 to provide:
    - Intelligent Q&A with RAG
    - Knowledge graph integration
    - User memory and personalization
    - Multi-turn conversations
    """
    
    def __init__(self, voice_style: str = None):
        super().__init__("fishing-coach", "1.0.0")
        self.agent = AdvancedFishingAgentV4(
            voice_style=voice_style,
            enable_reasoning=True
        )
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute fishing coach query
        
        Args:
            question: User question
            user_id: Optional user ID for personalization
            latitude: Optional user latitude
            longitude: Optional user longitude
            voice_style: Optional voice style override
            
        Returns:
            Response with answer and metadata
        """
        question = kwargs.get('question')
        if not question:
            return ResponseFormatter.error("Missing required parameter: question")
        
        try:
            # Call agent
            response = self.agent.chat(
                question=question,
                user_id=kwargs.get('user_id'),
                latitude=kwargs.get('latitude'),
                longitude=kwargs.get('longitude'),
                voice_style=kwargs.get('voice_style')
            )
            
            return ResponseFormatter.success(
                data=response,
                message="Fishing coach response generated"
            )
        
        except Exception as e:
            return ResponseFormatter.error(
                error=str(e),
                code="AGENT_ERROR"
            )
    
    def ask(self, question: str, **kwargs) -> Dict[str, Any]:
        """Ask a single question (convenience method)
        
        Args:
            question: User question
            **kwargs: Additional parameters (user_id, latitude, longitude, etc.)
            
        Returns:
            Response dictionary
        """
        return self.execute(question=question, **kwargs)
    
    def chat(self, question: str, user_id: str, **kwargs) -> Dict[str, Any]:
        """Multi-turn chat with user context
        
        Args:
            question: User question
            user_id: User ID for memory
            **kwargs: Additional parameters
            
        Returns:
            Response dictionary
        """
        return self.execute(question=question, user_id=user_id, **kwargs)
    
    def get_user_memory(self, user_id: str) -> Dict[str, Any]:
        """Get user memory and preferences
        
        Args:
            user_id: User ID
            
        Returns:
            User memory data
        """
        try:
            from user_memory import get_memory_manager
            memory_manager = get_memory_manager()
            memory = memory_manager.get_user_memory(user_id)
            
            return ResponseFormatter.success(
                data={
                    "user_id": user_id,
                    "level": memory.level.value if memory else "beginner",
                    "preferences": memory.preferences if memory else {},
                    "fishing_history": memory.fishing_history if memory else []
                },
                message="User memory retrieved"
            )
        
        except Exception as e:
            return ResponseFormatter.error(
                error=str(e),
                code="MEMORY_ERROR"
            )
