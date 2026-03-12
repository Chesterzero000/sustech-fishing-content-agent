"""Weather Advisor Service - Wraps volc_tools weather functionality"""
from typing import Dict, Any, Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from shared import SkillBase, ResponseFormatter
from volc_tools import VolcWeatherTool


class WeatherAdvisorService(SkillBase):
    """Weather and fishing conditions advisor
    
    Wraps VolcWeatherTool to provide:
    - Current weather conditions
    - Weather forecasts
    - Fishing suitability index
    """
    
    def __init__(self):
        super().__init__("weather-advisor", "1.0.0")
        self.weather_tool = VolcWeatherTool()
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute weather query
        
        Args:
            city: City name (Chinese)
            latitude: GPS latitude
            longitude: GPS longitude
            days: Forecast days (default: 1)
            
        Returns:
            Weather data and fishing index
        """
        city = kwargs.get('city')
        latitude = kwargs.get('latitude')
        longitude = kwargs.get('longitude')
        
        if not city and not (latitude and longitude):
            return ResponseFormatter.error("Missing required parameter: city or (latitude, longitude)")
        
        try:
            # Get location string
            if city:
                location = city
            else:
                location = f"{latitude},{longitude}"
            
            # Get weather data
            weather_data = self.weather_tool.get_weather(location)
            
            # Calculate fishing index
            fishing_index = self._calculate_fishing_index(weather_data)
            
            return ResponseFormatter.success(
                data={
                    "weather": weather_data,
                    "fishing_index": fishing_index,
                    "recommendation": self._get_recommendation(fishing_index)
                },
                message="Weather data retrieved"
            )
        
        except Exception as e:
            return ResponseFormatter.error(
                error=str(e),
                code="WEATHER_ERROR"
            )
    
    def get_current(self, city: str = None, latitude: float = None, longitude: float = None) -> Dict[str, Any]:
        """Get current weather (convenience method)
        
        Args:
            city: City name
            latitude: GPS latitude
            longitude: GPS longitude
            
        Returns:
            Current weather and fishing index
        """
        return self.execute(city=city, latitude=latitude, longitude=longitude)
    
    def get_forecast(self, city: str = None, latitude: float = None, longitude: float = None, days: int = 7) -> Dict[str, Any]:
        """Get weather forecast
        
        Args:
            city: City name
            latitude: GPS latitude
            longitude: GPS longitude
            days: Number of forecast days (1-7)
            
        Returns:
            Weather forecast
        """
        try:
            location = city if city else f"{latitude},{longitude}"
            forecast_data = self.weather_tool.get_forecast(location, days=days)
            
            return ResponseFormatter.success(
                data=forecast_data,
                message=f"{days}-day weather forecast"
            )
        
        except Exception as e:
            return ResponseFormatter.error(
                error=str(e),
                code="FORECAST_ERROR"
            )
    
    def calculate_fishing_index(self, weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate fishing suitability index
        
        Args:
            weather_data: Weather data dictionary
            
        Returns:
            Fishing index (0-100) and recommendation
        """
        try:
            index = self._calculate_fishing_index(weather_data)
            
            return ResponseFormatter.success(
                data={
                    "fishing_index": index,
                    "recommendation": self._get_recommendation(index)
                },
                message="Fishing index calculated"
            )
        
        except Exception as e:
            return ResponseFormatter.error(
                error=str(e),
                code="INDEX_ERROR"
            )
    
    def _calculate_fishing_index(self, weather_data: Dict[str, Any]) -> int:
        """Calculate fishing index based on weather conditions
        
        Args:
            weather_data: Weather data
            
        Returns:
            Fishing index (0-100)
        """
        index = 50  # Base score
        
        # Temperature factor (optimal: 15-25°C)
        temp = weather_data.get('temperature', 20)
        if 15 <= temp <= 25:
            index += 20
        elif 10 <= temp < 15 or 25 < temp <= 30:
            index += 10
        else:
            index -= 10
        
        # Pressure factor (stable is good)
        pressure = weather_data.get('pressure', 1013)
        if 1010 <= pressure <= 1020:
            index += 15
        elif 1000 <= pressure < 1010 or 1020 < pressure <= 1030:
            index += 5
        
        # Wind factor (light breeze best)
        wind_speed = weather_data.get('wind_speed', 0)
        if wind_speed < 5:
            index += 15
        elif wind_speed < 10:
            index += 5
        else:
            index -= 10
        
        # Precipitation factor
        precip = weather_data.get('precipitation', 0)
        if precip == 0:
            index += 10
        elif precip < 5:
            index += 5
        else:
            index -= 15
        
        # Clamp to 0-100
        return max(0, min(100, index))
    
    def _get_recommendation(self, index: int) -> str:
        """Get fishing recommendation based on index
        
        Args:
            index: Fishing index (0-100)
            
        Returns:
            Recommendation text
        """
        if index >= 80:
            return "今天是钓鱼的绝佳天气！鱼儿活跃，快去钓鱼吧！"
        elif index >= 60:
            return "今天天气不错，适合钓鱼。"
        elif index >= 40:
            return "天气一般，可以尝试钓鱼，但效果可能不太理想。"
        elif index >= 20:
            return "天气条件不太好，不太适合钓鱼。"
        else:
            return "天气很差，不建议钓鱼。"
