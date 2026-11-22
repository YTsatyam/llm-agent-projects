# LLM agent projects

Small LLM projects, each measured on a test set. Free tools only (Gemini API free tier, SQLite, Python).

| Project | What it is | Result |
|---|---|---|
| [MCP agent](mcp-agent/) | MCP server with notes search and GitHub tools, plus an agent; also runs in Claude Desktop | correct tool on 15/15 tasks |
| [Text-to-SQL agent](text-to-sql/) | Plain-English questions to SQL, with read-only access, AST validation and a timeout | 30/30 on the main set, 19/20 on a harder set; no destructive statement reached the database |
| LLM router | Planned: route easy questions to a small model and hard ones to a large one | not started |

Setup: `pip install -r requirements.txt`, then put `GEMINI_API_KEY=...` in a `.env` file at the repo root.