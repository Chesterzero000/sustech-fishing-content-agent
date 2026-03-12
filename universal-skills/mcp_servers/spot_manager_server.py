"""MCP Server for Spot Manager skill"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from mcp_servers import MCPServerBase
from skills.spot_manager.service import SpotManagerService


class SpotManagerMCPServer(MCPServerBase):
    """MCP server exposing spot manager tools"""
    
    def __init__(self):
        super().__init__("spot-manager", "1.0.0")
        self.service = SpotManagerService()
    
    def setup_tools(self):
        """Register all spot manager tools"""
        
        # Tool 1: get_nearby_spots
        self.register_tool(
            name="get_nearby_spots",
            description="Find fishing spots near a location. Returns spots within specified radius sorted by distance.",
            input_schema={
                "type": "object",
                "properties": {
                    "latitude": {
                        "type": "number",
                        "description": "GPS latitude"
                    },
                    "longitude": {
                        "type": "number",
                        "description": "GPS longitude"
                    },
                    "radius": {
                        "type": "number",
                        "default": 10.0,
                        "description": "Search radius in kilometers"
                    },
                    "fish_species": {
                        "type": "string",
                        "description": "Optional filter by fish species"
                    }
                },
                "required": ["latitude", "longitude"]
            },
            handler=self._handle_nearby
        )
        
        # Tool 2: search_spots
        self.register_tool(
            name="search_spots",
            description="Search fishing spots by fish species or other criteria.",
            input_schema={
                "type": "object",
                "properties": {
                    "fish_species": {
                        "type": "string",
                        "description": "Fish species to search for"
                    },
                    "city": {
                        "type": "string",
                        "description": "Optional city filter"
                    }
                },
                "required": ["fish_species"]
            },
            handler=self._handle_search
        )
        
        # Tool 3: get_spot_details
        self.register_tool(
            name="get_spot_details",
            description="Get detailed information about a specific fishing spot.",
            input_schema={
                "type": "object",
                "properties": {
                    "spot_id": {
                        "type": "integer",
                        "description": "Spot ID"
                    }
                },
                "required": ["spot_id"]
            },
            handler=self._handle_details
        )
        
        # Tool 4: list_spots
        self.register_tool(
            name="list_spots",
            description="List all fishing spots with pagination.",
            input_schema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "default": 20,
                        "description": "Number of spots to return"
                    },
                    "offset": {
                        "type": "integer",
                        "default": 0,
                        "description": "Offset for pagination"
                    }
                },
                "required": []
            },
            handler=self._handle_list
        )
    
    def _handle_nearby(self, latitude: float, longitude: float, radius: float = 10.0, fish_species: str = None):
        """Handle get_nearby_spots tool"""
        return self.service.search_nearby(
            latitude=latitude,
            longitude=longitude,
            radius=radius,
            fish_species=fish_species
        )
    
    def _handle_search(self, fish_species: str, city: str = None):
        """Handle search_spots tool"""
        return self.service.search_by_fish(fish_species=fish_species, city=city)
    
    def _handle_details(self, spot_id: int):
        """Handle get_spot_details tool"""
        return self.service.get_spot_details(spot_id)
    
    def _handle_list(self, limit: int = 20, offset: int = 0):
        """Handle list_spots tool"""
        return self.service.list_spots(limit=limit, offset=offset)


if __name__ == "__main__":
    server = SpotManagerMCPServer()
    server.run_stdio()
