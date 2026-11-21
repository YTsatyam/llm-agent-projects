import pathlib, httpx
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("notes-and-github")
NOTES = pathlib.Path(__file__).parent / "notes"


@mcp.tool()
def search_notes(query: str) -> str:
    """Search my markdown notes for a keyword. Returns matching lines with file names."""
    hits = [f"{f.name}: {line.strip()}" for f in NOTES.glob("*.md")
            for line in f.read_text(encoding="utf-8").splitlines() if
            query.lower() in line.lower()]
    return "\n".join(hits[:15]) or "No matches."


@mcp.tool()
def read_github_file(repo: str, path: str = "README.md") -> str:
    """Read a file from a public GitHub repo, for example repo='rasbt/LLMs-from-scratch'."""
    r = httpx.get(f"https://raw.githubusercontent.com/{repo}/HEAD/{path}",
                  timeout=15)
    return r.text[:6000] if r.status_code == 200 else f"Error {r.status_code}"


if __name__ == "__main__":
    mcp.run(transport="stdio")