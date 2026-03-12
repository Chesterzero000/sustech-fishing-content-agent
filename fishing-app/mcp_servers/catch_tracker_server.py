"""MCP Server for Catch Tracker Skill"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from mcp_servers.base import MCPServerBase
from skills.catch_tracker.service import CatchTrackerService


class CatchTrackerMCPServer(MCPServerBase):
    """MCP Server for catch record management"""
    
    def __init__(self):
        super().__init__(
            name="catch-tracker",
            version="1.0.0",
            description="Catch record management - log catches, view history, get statistics"
        )
        self.service = CatchTrackerService()
    
    def register_tools(self):
        """Register MCP tools"""
        
        @self.tool(
            name="log_catch",
            description="Log a new catch record with fish species, weight, and optional details",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User ID"
                    },
                    "fish_species": {
                        "type": "string",
                        "description": "Fish species name (e.g., '鲫鱼', '鲈鱼')"
                    },
                    "weight": {
                        "type": "number",
                        "description": "Fish weight in kg"
                    },
                    "length": {
                        "type": "number",
                        "description": "Fish length in cm (optional)"
                    },
                    "spot_id": {
                        "type": "integer",
                        "description": "Fishing spot ID (optional)"
                    },
                    "image_path": {
                        "type": "string",
                        "description": "Path to catch photo (optional)"
                    },
                    "notes": {
                        "type": "string",
                        "description": "Additional notes (optional)"
                    },
                    "latitude": {
                        "type": "number",
                        "description": "GPS latitude (optional)"
                    },
                    "longitude": {
                        "type": "number",
                        "description": "GPS longitude (optional)"
                    }
                },
                "required": ["user_id", "fish_species", "weight"]
            }
        )
        def log_catch_tool(user_id: str, fish_species: str, weight: float, **kwargs):
            """Log a new catch"""
            return self.service.log_catch(
                user_id=user_id,
                fish_species=fish_species,
                weight=weight,
                **kwargs
            )
        
        @self.tool(
            name="get_catches",
            description="Get catch history for a user with pagination",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User ID"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of records to return (default: 20)",
                        "default": 20
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Offset for pagination (default: 0)",
                        "default": 0
                    }
                },
                "required": ["user_id"]
            }
        )
        def get_catches_tool(user_id: str, limit: int = 20, offset: int = 0):
            """Get catch history"""
            return self.service.get_catches(
                user_id=user_id,
                limit=limit,
                offset=offset
            )
        
        @self.tool(
            name="get_catch_statistics",
            description="Get catch statistics for a user including total catches, weight, species distribution",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User ID"
                    }
                },
                "required": ["user_id"]
            }
        )
        def get_statistics_tool(user_id: str):
            """Get catch statistics"""
            return self.service.get_statistics(user_id=user_id)
        
        @self.tool(
            name="delete_catch",
            description="Delete a catch record by ID with optional ownership verification",
            input_schema={
                "type": "object",
                "properties": {
                    "catch_id": {
                        "type": "integer",
                        "description": "Catch record ID"
                    },
                    "user_id": {
                        "type": "string",
                        "description": "User ID for ownership verification (optional)"
                    }
                },
                "required": ["catch_id"]
            }
        )
        def delete_catch_tool(catch_id: int, user_id: str = None):
            """Delete a catch record"""
            return self.service.delete_catch(
                catch_id=catch_id,
                user_id=user_id
            )


if __name__ == "__main__":
    server = CatchTrackerMCPServer()
    server.run()
