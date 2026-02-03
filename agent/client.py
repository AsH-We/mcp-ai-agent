import sys
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def call_mcp_tool(script_path: str, tool_name: str, arguments: dict):
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[script_path],
        env=os.environ.copy()
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments)
            return result.content[0].text
