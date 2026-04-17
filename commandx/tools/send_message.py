from mcp.server.fastmcp import FastMCP
from client import CIMgateClient
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("commandx")

client = CIMgateClient()

def send_message(mission_id: str, message: str) -> list[dict]:
    log.info("TOOL  send_message")
    return client.post(("message" + mission_id + "/message"), json={
        "text": message,
        "sendername": "AI",
        "recivername": "unbekannter Empfänger",
        "messagestatus": 1
    })


def register_message_tools(mcp: FastMCP) -> None:
    mcp.add_tool(
        send_message,
        name="send_message",
        description="""Sends a message to CommandX.
        
        Args:
        """)

