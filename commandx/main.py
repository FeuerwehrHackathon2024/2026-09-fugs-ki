from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse
from tools import register_tools

mcp = FastMCP("CommandX", json_response=True)
register_tools(mcp)

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    return JSONResponse({"status": "ok"}, status_code=200)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")

