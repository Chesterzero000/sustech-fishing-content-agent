---
name: fish-identifier
description: "Fish species recognition from images using AI vision. Use when: (1) user uploads fish photo, (2) needs to identify caught fish, (3) wants fishing tips for specific species. Supports 3000+ fish species via Fishial API."
metadata:
  {
    "openclaw": {
      "emoji": "🐟",
      "requires": {
        "bins": []
      },
      "os": ["linux", "darwin", "win32"]
    }
  }
---

# Fish Identifier

AI-powered fish species identification using computer vision and knowledge graph integration.

## Features

- **Image Recognition**: Identify fish species from photos using Doubao Vision + Fishial API
- **3000+ Species**: Support for global fish species database
- **Fishing Tips**: Get fishing techniques for identified species
- **Knowledge Graph**: Integration with fish knowledge graph for detailed information
- **Confidence Scores**: Provides confidence levels for identifications

## When to Use

- User uploads a photo of a caught fish
- User asks "What fish is this?"
- User needs fishing tips for a specific species
- User wants to learn about fish characteristics

## Examples

### CLI Usage

```bash
# Recognize fish from image
fishing-cli fish recognize ./my_catch.jpg

# Get fishing tips for a species
fishing-cli fish tips "鲫鱼"

# Recognize with JSON output
fishing-cli fish recognize ./photo.jpg --format json
```

### MCP Tool Usage

```json
{
  "tool": "identify_fish",
  "arguments": {
    "image_path": "/path/to/fish.jpg"
  }
}
```

Or with base64:

```json
{
  "tool": "identify_fish_base64",
  "arguments": {
    "image_base64": "iVBORw0KGgoAAAANS..."
  }
}
```

## Recognition Process

1. **Image Upload**: User provides fish photo
2. **Vision Analysis**: Doubao Vision model analyzes image
3. **Fishial API**: Cross-reference with Fishial.ai database (3000+ species)
4. **Knowledge Graph**: Retrieve fishing techniques from Neo4j
5. **Response**: Return species name, confidence, and fishing tips

## Supported Species

- **Freshwater**: 鲫鱼, 鲤鱼, 草鱼, 青鱼, 黑鱼, 鲈鱼, etc.
- **Saltwater**: 带鱼, 石斑鱼, 鲳鱼, 大黄鱼, etc.
- **Global**: 3000+ species via Fishial API

## Response Format

```json
{
  "success": true,
  "data": {
    "species": "鲫鱼",
    "confidence": 0.95,
    "scientific_name": "Carassius auratus",
    "fishing_tips": {
      "bait": "蚯蚓、红虫、商品饵",
      "technique": "台钓、传统钓",
      "season": "春秋最佳"
    }
  }
}
```

## Integration

This skill wraps:
- `fusion_fish_recognition.py` - Multi-model fusion recognition
- `doubao_fish_recognition.py` - Doubao Vision API
- Fishial API - Global fish database
- Neo4j knowledge graph - Fishing techniques
