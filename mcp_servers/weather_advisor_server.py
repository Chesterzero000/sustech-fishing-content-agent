"""MCP Server for Weather Advisor skill"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from mcp_servers import MCPServerBase
from skills.weather_advisor.service import WeatherAdvisorService


class WeatherAdvisorMCPServer(MCPServerBase):
    """MCP server exposing weather advisor tools"""
    
    def __init__(self):
        super().__init__("weather-advisor", "1.0.0")
        self.service = WeatherAdvisorService()
    
    def setup_tools(self):
        """Register all weather advisor tools"""
        
        # Tool 1: get_weather
        self.register_tool(
            name="get_weather",
            description="Get current weather conditions and fishing suitability index.",
            input_schema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name (Chinese, e.g., 深圳)"
                    },
                    "latitude": {
                        "type": "number",
                        "description": "GPS latitude"
                    },
                    "longitude": {
                        "type": "number",
                        "description": "GPS longitude"
                    }
                },
                "oneOf": [
                    {"required": ["city"]},
                    {"required": ["latitude", "longitude"]}
                ]
            },
            handler=self._handle_get_weather
        )
        
        # Tool 2: get_forecast
        self.register_tool(
            name="get_forecast",
            description="Get weather forecast for multiple days (1-7 days).",
            input_schema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name"
                    },
                    "latitude": {
                        "type": "number",
                        "description": "GPS latitude"
                    },
                    "longitude": {
                        "type": "number",
                        "description": "GPS longitude"
                    },
                    "days": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 7,
                        "default": 7,
                        "description": "Number of forecast days"
                    }
                },
                "oneOf": [
                    {"required": ["city"]},
                    {"required": ["latitude", "longitude"]}
                ]
            },
            handler=self._handle_get_forecast
        )
        
        # Tool 3: calculate_fishing_index
        self.register_tool(
            name="calculate_fishing_index",
            description="Calculate fishing suitability index (0-100) based on weather conditions.",
            input_schema={
                "type": "object",
                "properties": {
                    "weather_data": {
                        "type": "object",
                        "description": "Weather data object with temperature, pressure, wind_speed, etc."
                    }
                },
                "required": ["weather_data"]
            },
            handler=self._handle_calculate_index
        )
    
    def _handle_get_weather(self, city: str = None, latitude: float = None, longitude: float = None):
        """Handle get_weather tool"""
        return self.service.get_current(city=city, latitude=latitude, longitude=longitude)
    
    def _handle_get_forecast(self, city: str = None, latitude: float = None, longitude: float = None, days: int = 7):
        """Handle get_forecast tool"""
        return self.service.get_forecast(city=city, latitude=latitude, longitude=longitude, days=days)
    
    def _handle_calculate_index(self, weather_data: dict):
        """Handle calculate_fishing_index tool"""
        return self.service.calculate_fishing_index(weather_data)


if __name__ == "__main__":
    server = WeatherAdvisorMCPServer()
    server.run_stdio()
