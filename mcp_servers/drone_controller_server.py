"""MCP Server for drone-controller skill.

This server registers all available tools from the drone-controller skill
so external MCP clients can invoke them. It relies on the base MCPServerBase
class provided by the project (shared.mcp_server_base) and the service layer
exposed by skills.drone-controller.service.DroneControllerService.
"""

from shared.mcp_server_base import MCPServerBase
from skills.drone-controller.service import DroneControllerService


class DroneControllerServer(MCPServerBase):
    def __init__(self, host: str = "0.0.0.0", port: int = 8000):
        super().__init__(host=host, port=port)
        self.service = DroneControllerService()
        # Register all service methods as MCP tools
        # The actual MCP framework may expect a specific registration API;
        # here we provide a representative registration that many setups use.
        if hasattr(self, "register_tool"):
            self.register_tool("drone.get_telemetry", self.service.get_telemetry)
            self.register_tool("drone.get_trajectory", self.service.get_trajectory)
            self.register_tool("drone.get_status", self.service.get_status)
            self.register_tool("drone.send_command", self.service.send_command)


if __name__ == "__main__":
    server = DroneControllerServer()
    if hasattr(server, "start"):
        server.start()
    elif hasattr(server, "run"):  # fallback for different MCP servers
        server.run()
    else:
        # Basic placeholder to indicate the server object is ready.
        print("DroneController MCP server initialized. Implement start/run according to your MCP framework.")
