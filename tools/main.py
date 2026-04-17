from mcp.server.fastmcp import FastMCP

from generic import register_generic_tools


mcp = FastMCP("Tools", json_response=True)


@mcp.tool("hello")
def hallo() -> str:
    return "Hello from tools!"


@mcp.tool("add")
def add(a: int, b: int) -> int:
    return a + b


register_generic_tools(mcp)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
