"""Base MCP server implementation for OpenClaw skills

This module provides a base class for creating MCP (Model Context Protocol) servers
that expose skill functionality as tools. Works with stdio transport.

If mcp SDK is not installed, provides a minimal stdio-based implementation.
"""
import sys
import json
import logging
from typing import Dict, Any, List, Optional, Callable
from abc import ABC, abstractmethod

# Try to import MCP SDK, fall back to minimal implementation if not available
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    MCP_SDK_AVAILABLE = True
except ImportError:
    MCP_SDK_AVAILABLE = False
    logging.warning("MCP SDK not installed. Using minimal stdio implementation.")


class MCPServerBase(ABC):
    """Base class for MCP servers
    
    Provides common functionality for all skill MCP servers:
    - Tool registration
    - Request handling
    - Error handling
    - Stdio transport
    """
    
    def __init__(self, name: str, version: str = "1.0.0"):
        """Initialize MCP server
        
        Args:
            name: Server name (e.g., "fishing-coach")
            version: Server version
        """
        self.name = name
        self.version = version
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.tool_handlers: Dict[str, Callable] = {}
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            stream=sys.stderr  # Log to stderr, keep stdout for MCP protocol
        )
        self.logger = logging.getLogger(name)
    
    def register_tool(
        self,
        name: str,
        description: str,
        input_schema: Dict[str, Any],
        handler: Callable
    ):
        """Register a tool with the MCP server
        
        Args:
            name: Tool name (e.g., "coach_ask")
            description: Tool description for AI
            input_schema: JSON Schema for tool parameters
            handler: Function to call when tool is invoked
        """
        self.tools[name] = {
            "name": name,
            "description": description,
            "inputSchema": input_schema
        }
        self.tool_handlers[name] = handler
        self.logger.info(f"Registered tool: {name}")
    
    @abstractmethod
    def setup_tools(self):
        """Setup all tools for this server
        
        Subclasses must implement this to register their tools.
        """
        pass
    
    def handle_list_tools(self) -> Dict[str, Any]:
        """Handle tools/list request
        
        Returns:
            Dict with list of available tools
        """
        return {
            "tools": list(self.tools.values())
        }
    
    def handle_call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/call request
        
        Args:
            tool_name: Name of tool to call
            arguments: Tool arguments
            
        Returns:
            Tool execution result
        """
        if tool_name not in self.tool_handlers:
            return {
                "content": [{
                    "type": "text",
                    "text": f"Error: Unknown tool '{tool_name}'"
                }],
                "isError": True
            }
        
        try:
            handler = self.tool_handlers[tool_name]
            result = handler(**arguments)
            
            # Format result as MCP content
            return {
                "content": [{
                    "type": "text",
                    "text": json.dumps(result, ensure_ascii=False)
                }]
            }
        except Exception as e:
            self.logger.error(f"Tool execution error: {e}", exc_info=True)
            return {
                "content": [{
                    "type": "text",
                    "text": f"Error executing tool: {str(e)}"
                }],
                "isError": True
            }
    
    def run_stdio(self):
        """Run server with stdio transport
        
        Reads JSON-RPC requests from stdin, writes responses to stdout.
        """
        self.logger.info(f"Starting MCP server: {self.name} v{self.version}")
        self.setup_tools()
        self.logger.info(f"Registered {len(self.tools)} tools")
        
        if MCP_SDK_AVAILABLE:
            self._run_with_sdk()
        else:
            self._run_minimal_stdio()
    
    def _run_with_sdk(self):
        """Run using official MCP SDK"""
        # This will be implemented when SDK is available
        self.logger.info("Running with MCP SDK")
        # TODO: Implement SDK-based server
        pass
    
    def _run_minimal_stdio(self):
        """Run using minimal stdio implementation
        
        Implements basic JSON-RPC 2.0 protocol over stdio.
        """
        self.logger.info("Running with minimal stdio implementation")
        
        while True:
            try:
                # Read request from stdin
                line = sys.stdin.readline()
                if not line:
                    break
                
                request = json.loads(line)
                self.logger.debug(f"Received request: {request}")
                
                # Handle request
                response = self._handle_request(request)
                
                # Write response to stdout
                sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
                sys.stdout.flush()
                
            except json.JSONDecodeError as e:
                self.logger.error(f"Invalid JSON: {e}")
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": "Parse error"
                    }
                }
                sys.stdout.write(json.dumps(error_response) + "\n")
                sys.stdout.flush()
            
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}", exc_info=True)
    
    def _handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle JSON-RPC request
        
        Args:
            request: JSON-RPC request
            
        Returns:
            JSON-RPC response
        """
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        try:
            if method == "tools/list":
                result = self.handle_list_tools()
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                result = self.handle_call_tool(tool_name, arguments)
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
        
        except Exception as e:
            self.logger.error(f"Request handling error: {e}", exc_info=True)
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
