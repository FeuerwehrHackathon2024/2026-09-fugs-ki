from mcp.server.fastmcp import FastMCP

from tools.missions.actions import register_action_tools
from tools.missions.resources import register_resource_tools
from tools.missions.groups import register_group_tools

def register_tools(mcp: FastMCP) -> None:
    register_action_tools(mcp)
    register_resource_tools(mcp)
    register_group_tools(mcp)