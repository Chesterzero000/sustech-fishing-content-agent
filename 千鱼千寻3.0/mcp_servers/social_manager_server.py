"""MCP server for the social-manager skill.

Registers all available tools (service functions) using MCPServerBase.
"""
from __future__ import annotations

try:
    # Real project import path (if available)
    from mcp_server_base import MCPServerBase
except Exception:
    # Lightweight fallback so repository remains usable in isolation
    class MCPServerBase:  # type: ignore
        def __init__(self, *args, **kwargs):
            self._registry = {}

        def register(self, name: str, func):
            self._registry[name] = func

        def run(self):
            # Placeholder for real MCP server loop
            print("MCP server running with registered tools:")
            for k in sorted(self._registry.keys()):
                print(f" - {k}")


from skills.social-manager.service import (
    create_post,
    get_posts,
    delete_post,
    add_comment,
    get_comments,
    like_post,
    unlike_post,
)


class SocialManagerServer(MCPServerBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Register all service tools
        self.register("social.create_post", create_post)
        self.register("social.get_posts", get_posts)
        self.register("social.delete_post", delete_post)
        self.register("social.add_comment", add_comment)
        self.register("social.get_comments", get_comments)
        self.register("social.like_post", like_post)
        self.register("social.unlike_post", unlike_post)


def main():
    server = SocialManagerServer()
    server.run()


if __name__ == "__main__":  # pragma: no cover
    main()
