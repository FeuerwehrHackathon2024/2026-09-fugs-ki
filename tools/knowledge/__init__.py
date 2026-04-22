from mcp.server.fastmcp import FastMCP

from .rag import register_tools as register_rag_tools


def register_knowledge_tools(mcp: FastMCP) -> None:
    register_rag_tools(mcp)
