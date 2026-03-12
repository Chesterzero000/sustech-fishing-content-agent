---
name: weather-advisor
description: "Weather forecasts and fishing conditions advisor. Use when: (1) user asks about weather, (2) needs fishing suitability index, (3) wants to plan fishing trips. Provides real-time weather and 7-day forecasts via QWeather API."
metadata:
  {
    "openclaw": {
      "emoji": "🌤️",
      "requires": {
        "env": []
      },
      "os": ["linux", "darwin", "win32"]
    }
  }
---

# Weather Advisor

Real-time weather forecasts and fishing condition analysis powered by QWeather API.

## Features

- **Current Weather**: Real-time weather conditions
- **7-Day Forecast**: Extended weather predictions
- **Fishing Index**: Calculate fishing suitability based on weather
- **Location-Based**: Support city names or GPS coordinates
- **Multi-Factor Analysis**: Temperature, pressure, wind, precipitation

## When to Use

- User asks "What's the weather today?"
- User wants to know if it's good for fishing
- User needs weather forecast for trip planning
- User asks about fishing conditions

## Examples

### CLI Usage

```bash
# Get current weather
fishing-cli weather current --city "深圳"

# Get 7-day forecast
fishing-cli weather forecast --city "深圳" --days 7

# Calculate fishing index
fishing-cli weather fishing-index --lat 22.5 --lon 114.0

# Weather with JSON output
fishing-cli weather current --city "深圳" --format json
```

### MCP Tool Usage

```json
{
  "tool": "get_weather",
  "arguments": {
    "city": "深圳"
  }
}
```

Or with coordinates:

```json
{
  "tool": "get_weather",
  "arguments": {
    "latitude": 22.5,
    "longitude": 114.0
  }
}
```

## Fishing Index Calculation

The fishing index (0-100) considers:

- **Temperature**: Optimal range 15-25°C
- **Air Pressure**: Stable pressure is best
- **Wind Speed**: Light breeze ideal (< 5 m/s)
- **Precipitation**: Light rain OK, heavy rain bad
- **Time of Day**: Dawn and dusk best

### Index Interpretation

- **80-100**: Excellent fishing conditions
- **60-79**: Good conditions
- **40-59**: Fair conditions
- **20-39**: Poor conditions
- **0-19**: Very poor conditions

## Weather Data

Powered by QWeather (和风天气) API:
- Real-time updates
- Accurate forecasts
- Global coverage
- Fishing-specific indices

## Response Format

```json
{
  "success": true,
  "data": {
    "current": {
      "temperature": 22,
      "feels_like": 20,
      "humidity": 65,
      "pressure": 1013,
      "wind_speed": 3.5,
      "condition": "晴"
    },
    "fishing_index": 85,
    "recommendation": "今天是钓鱼的好天气！"
  }
}
```

## Integration

This skill wraps:
- `volc_tools.py` - VolcWeatherTool for QWeather API
- `weather_service.py` - Weather data processing
- `weather_fishing_service.py` - Fishing condition analysis
