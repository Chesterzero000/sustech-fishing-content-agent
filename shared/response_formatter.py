"""Unified response formatting for CLI and MCP outputs"""
from typing import Any, Dict, Optional
from datetime import datetime
import json


class ResponseFormatter:
    """Formats responses consistently across all skills
    
    Provides standardized success/error responses for both
    CLI (Markdown) and MCP (JSON) interfaces.
    """
    
    @staticmethod
    def success(data: Any, message: str = "Success") -> Dict[str, Any]:
        """Format successful response
        
        Args:
            data: Response data (any JSON-serializable type)
            message: Success message
            
        Returns:
            Standardized success response dict
        """
        return {
            "success": True,
            "message": message,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def error(error: str, code: str = "ERROR", details: Optional[Dict] = None) -> Dict[str, Any]:
        """Format error response
        
        Args:
            error: Error message
            code: Error code (e.g., "VALIDATION_ERROR", "API_ERROR")
            details: Optional additional error details
            
        Returns:
            Standardized error response dict
        """
        response = {
            "success": False,
            "error": error,
            "code": code,
            "timestamp": datetime.now().isoformat()
        }
        if details:
            response["details"] = details
        return response
    
    @staticmethod
    def to_json(data: Dict[str, Any], pretty: bool = False) -> str:
        """Convert response to JSON string
        
        Args:
            data: Response dictionary
            pretty: If True, format with indentation
            
        Returns:
            JSON string (UTF-8, no ASCII escaping for Chinese)
        """
        if pretty:
            return json.dumps(data, ensure_ascii=False, indent=2)
        return json.dumps(data, ensure_ascii=False)
    
    @staticmethod
    def to_markdown(data: Dict[str, Any]) -> str:
        """Convert response to Markdown format (for CLI display)
        
        Args:
            data: Response dictionary
            
        Returns:
            Markdown-formatted string
        """
        if not data.get("success"):
            error_msg = data.get('error', 'Unknown error')
            code = data.get('code', 'ERROR')
            result = f"❌ **Error** ({code}): {error_msg}"
            
            if "details" in data:
                result += f"\n\n**Details:**\n```json\n{json.dumps(data['details'], ensure_ascii=False, indent=2)}\n```"
            
            return result
        
        lines = ["✅ **Success**"]
        
        if "message" in data and data["message"] != "Success":
            lines.append(f"\n{data['message']}")
        
        if "data" in data:
            lines.append("\n### Data:")
            data_content = data['data']
            
            # Format based on data type
            if isinstance(data_content, (dict, list)):
                lines.append(f"```json\n{json.dumps(data_content, ensure_ascii=False, indent=2)}\n```")
            else:
                lines.append(f"\n{data_content}")
        
        return "\n".join(lines)
    
    @staticmethod
    def format_list(items: list, title: str = "Results") -> str:
        """Format a list of items as Markdown
        
        Args:
            items: List of items to format
            title: Title for the list
            
        Returns:
            Markdown-formatted list
        """
        if not items:
            return f"### {title}\n\nNo items found."
        
        lines = [f"### {title} ({len(items)} items)\n"]
        
        for i, item in enumerate(items, 1):
            if isinstance(item, dict):
                # Format dict items with key-value pairs
                item_str = ", ".join(f"{k}: {v}" for k, v in item.items())
                lines.append(f"{i}. {item_str}")
            else:
                lines.append(f"{i}. {item}")
        
        return "\n".join(lines)
