"""MCP Server for Fishing Coach skill"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from mcp_servers import MCPServerBase
from skills.fishing_coach.service import FishingCoachService


class FishingCoachMCPServer(MCPServerBase):
    """MCP server exposing fishing coach tools"""
    
    def __init__(self):
        super().__init__("fishing-coach", "1.0.0")
        self.service = FishingCoachService()
    
    def setup_tools(self):
        """Register all fishing coach tools"""
        
        # Tool 1: coach_ask
        self.register_tool(
            name="coach_ask",
            description="Ask the AI fishing coach a question. Provides intelligent answers using RAG and knowledge graph.",
            input_schema={
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The fishing question to ask"
                    },
                    "user_id": {
                        "type": "string",
                        "description": "Optional user ID for personalization"
                    },
                    "latitude": {
                        "type": "number",
                        "description": "Optional user latitude for location-based advice"
                    },
                    "longitude": {
                        "type": "number",
                        "description": "Optional user longitude for location-based advice"
                    },
                    "voice_style": {
                        "type": "string",
                        "enum": ["default", "friendly", "professional", "humorous", "patient"],
                        "description": "Voice style for the response"
                    }
                },
                "required": ["question"]
            },
            handler=self._handle_ask
        )
        
        # Tool 2: coach_chat
        self.register_tool(
            name="coach_chat",
            description="Multi-turn chat with the fishing coach. Maintains conversation context and user memory.",
            input_schema={
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The question or message"
                    },
                    "user_id": {
                        "type": "string",
                        "description": "User ID (required for chat)"
                    },
                    "voice_style": {
                        "type": "string",
                        "enum": ["default", "friendly", "professional", "humorous", "patient"],
                        "description": "Voice style"
                    }
                },
                "required": ["question", "user_id"]
            },
            handler=self._handle_chat
        )
        
        # Tool 3: get_user_memory
        self.register_tool(
            name="get_user_memory",
            description="Get user's fishing memory, preferences, and history.",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User ID"
                    }
                },
                "required": ["user_id"]
            },
            handler=self._handle_get_memory
        )
    
    def _handle_ask(self, question: str, user_id: str = None, 
                    latitude: float = None, longitude: float = None,
                    voice_style: str = None):
        """Handle coach_ask tool"""
        return self.service.ask(
            question=question,
            user_id=user_id,
            latitude=latitude,
            longitude=longitude,
            voice_style=voice_style
        )
    
    def _handle_chat(self, question: str, user_id: str, voice_style: str = None):
        """Handle coach_chat tool"""
        return self.service.chat(
            question=question,
            user_id=user_id,
            voice_style=voice_style
        )
    
    def _handle_get_memory(self, user_id: str):
        """Handle get_user_memory tool"""
        return self.service.get_user_memory(user_id)


if __name__ == "__main__":
    server = FishingCoachMCPServer()
    server.run_stdio()
