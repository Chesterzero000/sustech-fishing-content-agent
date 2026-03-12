---
name: spot-manager
description: "Fishing spot search and management. Use when: (1) user needs nearby fishing spots, (2) wants spot details, (3) searches by fish species, (4) manages favorite spots. Database of 99 Shenzhen fishing spots with GPS coordinates."
metadata:
  {
    "openclaw": {
      "emoji": "📍",
      "requires": {
        "bins": []
      },
      "os": ["linux", "darwin", "win32"]
    }
  }
---

# Spot Manager

Fishing spot search and management with location-based recommendations.

## Features

- **Nearby Search**: Find fishing spots within radius
- **Fish Species Filter**: Search spots by target fish
- **Spot Details**: Get comprehensive spot information
- **Favorites**: Manage user's favorite spots
- **99 Shenzhen Spots**: Pre-loaded database with GPS coordinates

## When to Use

- User asks "Where can I fish nearby?"
- User wants spots for specific fish species
- User needs spot details (address, fish types, fees)
- User wants to save favorite spots

## Examples

### CLI Usage

```bash
# Find nearby spots
fishing-cli spots nearby --lat 22.5 --lon 114.0 --radius 10

# Search by fish species
fishing-cli spots search --fish "鲫鱼" --city "深圳"

# Get spot details
fishing-cli spots details --id 123

# List all spots
fishing-cli spots list --limit 20
```

### MCP Tool Usage

```json
{
  "tool": "get_nearby_spots",
  "arguments": {
    "latitude": 22.5,
    "longitude": 114.0,
    "radius": 10
  }
}
```

Search by fish:

```json
{
  "tool": "search_spots",
  "arguments": {
    "fish_species": "鲫鱼",
    "city": "深圳"
  }
}
```

## Spot Database

**99 Shenzhen Fishing Spots** including:
- 洪湖公园 (Honghu Park)
- 深圳湾公园 (Shenzhen Bay Park)
- 西丽水库 (Xili Reservoir)
- 梅林水库 (Meilin Reservoir)
- And 95 more...

Each spot includes:
- GPS coordinates (latitude, longitude)
- Address
- Fish species available
- Water type (lake, river, reservoir, sea)
- Difficulty level
- Fee information
- Rating

## Search Features

### Nearby Search
- Radius-based (default: 10km)
- Sorted by distance
- Returns GPS coordinates

### Fish Species Filter
- Search by target fish
- Multiple species support
- Returns matching spots

### Advanced Filters
- Water type (freshwater/saltwater)
- Difficulty level (easy/medium/hard)
- Fee range (free/paid)
- Rating threshold

## Response Format

```json
{
  "success": true,
  "data": {
    "count": 5,
    "spots": [
      {
        "id": 1,
        "name": "洪湖公园",
        "latitude": 22.5523,
        "longitude": 114.1234,
        "address": "深圳市罗湖区洪湖路",
        "fish_species": ["鲫鱼", "鲤鱼", "草鱼"],
        "water_type": "lake",
        "difficulty": "easy",
        "fee": "free",
        "rating": 4.5,
        "distance": 2.3
      }
    ]
  }
}
```

## Integration

This skill wraps:
- `fishing_spots_db.py` - SQLite database with 99 spots
- GPS distance calculation
- Spot filtering and sorting
