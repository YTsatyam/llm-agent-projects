import asyncio, json, sys, pathlib
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
HERE = pathlib.Path(__file__).resolve().parent
sys.path.append(str(HERE.parent))
from common.llm import chat, SMALL


async def ask(question):
    tools_used = []
    params = StdioServerParameters(command=sys.executable, args=[str(HERE / "server.py")])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = [{"type": "function", "function": {"name": t.name,
                     "description": t.description,
                     "parameters": t.inputSchema}} for t in (await
                     session.list_tools()).tools]
            messages = [{"role": "system", "content": "Use the tools when they help. Answer briefly."},
                        {"role": "user", "content": question}]
            for _ in range(5):                      # hard stop so it can't loop forever
                msg = chat(SMALL, messages, tools=tools).choices[0].message
                if not msg.tool_calls:
                    return msg.content, tools_used
                messages.append(msg.model_dump(exclude_none=True))
                for call in msg.tool_calls:
                    tools_used.append(call.function.name)
                    out = await session.call_tool(call.function.name,
                                                  json.loads(call.function.arguments))
                    messages.append({"role": "tool", "tool_call_id": call.id,
                                     "content": out.content[0].text})
            return "Stopped after 5 steps.", tools_used


if __name__ == "__main__":
    answer, _ = asyncio.run(ask(sys.argv[1]))
    print(answer)