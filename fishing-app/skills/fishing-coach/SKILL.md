---
name: fishing-coach
description: "AI fishing coach with RAG and knowledge graph. Use when: (1) user asks fishing questions, (2) needs fishing advice, (3) wants to learn fishing techniques. Provides personalized coaching based on user level and location."
metadata:
  {
    "openclaw": {
      "emoji": "🎓",
      "requires": {
        "env": ["NEO4J_URI", "NEO4J_USER", "NEO4J_PASSWORD"]
      },
      "primaryEnv": "NEO4J_URI",
      "os": ["linux", "darwin", "win32"]
    }
  }
---

# Fishing Coach

AI-powered fishing coach that provides personalized advice using RAG (Retrieval-Augmented Generation) and knowledge graph.

## Features

- **Intelligent Q&A**: Answer fishing-related questions with context-aware responses
- **Knowledge Graph**: Access to 100+ fish species database with fishing techniques
- **RAG System**: Retrieve relevant information from fishing knowledge base
- **User Memory**: Remember user preferences and fishing history
- **Voice Styles**: Multiple personality styles (friendly, professional, humorous)
- **Reasoning**: Chain-of-Thought and ReAct reasoning for complex questions

## When to Use

- User asks "How to catch [fish species]?"
- User needs fishing spot recommendations
- User wants to learn fishing techniques
- User asks about fish behavior or habits
- User needs equipment recommendations

## Examples

### CLI Usage

```bash
# Ask a question
fishing-cli coach ask "鲫鱼怎么钓?"

# Chat with user context
fishing-cli coach chat --user-id user123 --question "今天天气适合钓鱼吗?"

# Get user memory
fishing-cli coach memory --user-id user123

# Chat with voice style
fishing-cli coach ask "草鱼用什么饵料?" --voice-style friendly
```

### MCP Tool Usage

```json
{
  "tool": "coach_ask",
  "arguments": {
    "question": "鲫鱼怎么钓?",
    "user_id": "user123",
    "latitude": 22.5,
    "longitude": 114.0
  }
}
```

## Configuration

Required environment variables:
- `NEO4J_URI`: Neo4j database URI (default: bolt://192.168.1.79:7687)
- `NEO4J_USER`: Neo4j username (default: neo4j)
- `NEO4J_PASSWORD`: Neo4j password

Optional:
- `EMBED_MODEL`: Embedding model for RAG (default: shibing624/text2vec-base-chinese)

## Voice Styles

- `default`: Balanced and informative
- `friendly`: Warm and encouraging
- `professional`: Technical and precise
- `humorous`: Fun and engaging
- `patient`: Detailed and educational

## Integration

This skill wraps the `AdvancedFishingAgentV4` from `advanced_agent_v4_reasoning.py`, providing:
- Intent classification
- Knowledge graph queries
- RAG-based information retrieval
- User memory management
- Multi-turn conversation support
