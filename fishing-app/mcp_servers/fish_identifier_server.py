"""MCP Server for Fish Identifier skill"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from mcp_servers import MCPServerBase
from skills.fish_identifier.service import FishIdentifierService


class FishIdentifierMCPServer(MCPServerBase):
    """MCP server exposing fish identification tools"""
    
    def __init__(self):
        super().__init__("fish-identifier", "1.0.0")
        self.service = FishIdentifierService()
    
    def setup_tools(self):
        """Register all fish identifier tools"""
        
        # Tool 1: identify_fish (from file path)
        self.register_tool(
            name="identify_fish",
            description="Identify fish species from an image file. Returns species name, confidence score, and fishing tips.",
            input_schema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the fish image file"
                    }
                },
                "required": ["image_path"]
            },
            handler=self._handle_identify_file
        )
        
        # Tool 2: identify_fish_base64 (from base64 data)
        self.register_tool(
            name="identify_fish_base64",
            description="Identify fish species from base64-encoded image data.",
            input_schema={
                "type": "object",
                "properties": {
                    "image_base64": {
                        "type": "string",
                        "description": "Base64-encoded image data"
                    }
                },
                "required": ["image_base64"]
            },
            handler=self._handle_identify_base64
        )
        
        # Tool 3: get_fish_tips
        self.register_tool(
            name="get_fish_tips",
            description="Get fishing tips and techniques for a specific fish species.",
            input_schema={
                "type": "object",
                "properties": {
                    "fish_name": {
                        "type": "string",
                        "description": "Fish species name (Chinese or English)"
                    }
                },
                "required": ["fish_name"]
            },
            handler=self._handle_get_tips
        )
    
    def _handle_identify_file(self, image_path: str):
        """Handle identify_fish tool"""
        return self.service.recognize(image_path=image_path)
    
    def _handle_identify_base64(self, image_base64: str):
        """Handle identify_fish_base64 tool"""
        return self.service.recognize(image_base64=image_base64)
    
    def _handle_get_tips(self, fish_name: str):
        """Handle get_fish_tips tool"""
        return self.service.get_tips(fish_name)


if __name__ == "__main__":
    server = FishIdentifierMCPServer()
    server.run_stdio()
