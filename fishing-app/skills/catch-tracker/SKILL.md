---
name: catch-tracker
description: "Catch record logging and statistics. Use when: (1) user logs a new catch, (2) needs catch history, (3) wants fishing statistics, (4) manages catch records. Tracks fish species, weight, location, and photos."
metadata:
  {
    "openclaw": {
      "emoji": "📊",
      "requires": {
        "bins": []
      },
      "os": ["linux", "darwin", "win32"]
    }
  }
---

# Catch Tracker

Fishing catch record management with statistics and analytics.

## Features

- **Log Catches**: Record fish species, weight, location, photos
- **Catch History**: View personal catch records with pagination
- **Statistics**: Analyze catch data (total catches, species distribution, weight trends)
- **CRUD Operations**: Create, read, update, delete catch records
- **Photo Support**: Upload and manage catch photos

## When to Use

- User catches a fish and wants to log it
- User asks "Show my catch history"
- User wants fishing statistics
- User needs to manage catch records

## Examples

### CLI Usage

```bash
# Log a new catch
fishing-cli catch log --user user123 --fish "鲫鱼" --weight 0.5 --spot 42

# View catch history
fishing-cli catch list --user user123 --limit 10

# Get statistics
fishing-cli catch stats --user user123

# Delete a catch
fishing-cli catch delete --id 456
```

### MCP Tool Usage

```json
{
  "tool": "log_catch",
  "arguments": {
    "user_id": "user123",
    "fish_species": "鲫鱼",
    "weight": 0.5,
    "spot_id": 42,
    "image_path": "/path/to/photo.jpg"
  }
}
```

## Data Model

```json
{
  "id": 1,
  "user_id": "user123",
  "fish_species": "鲫鱼",
  "weight": 0.5,
  "length": 15.0,
  "spot_id": 42,
  "spot_name": "洪湖公园",
  "latitude": 22.5523,
  "longitude": 114.1234,
  "image_url": "https://...",
  "notes": "早晨7点钓获",
  "created_at": "2026-03-10T08:00:00"
}
```

## Statistics Features

### Catch Summary
- Total catches
- Total weight
- Species count
- Favorite spot

### Species Distribution
- Catches by species
- Weight by species
- Average weight per species

### Time Analysis
- Catches by month
- Catches by season
- Best fishing times

## Response Format

```json
{
  "success": true,
  "data": {
    "catch_id": 123,
    "fish_species": "鲫鱼",
    "weight": 0.5,
    "spot_name": "洪湖公园",
    "created_at": "2026-03-10T08:00:00"
  }
}
```

## Integration

This skill wraps:
- `backend_routes.py` - Catch record endpoints
- SQLite/MySQL database - Catch data storage
- Image upload handling
