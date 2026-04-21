from mcp.server.fastmcp import FastMCP

from .dwd import register_tools as _register_dwd_tools
from .stations import register_tools as _register_station_tools


def register_dwd_tools(mcp: FastMCP) -> None:
    _register_dwd_tools(mcp)
    _register_station_tools(mcp)
