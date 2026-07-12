#!/usr/bin/env python3
"""
AI-Brain MCP Server

Provides MCP tools for Codex / VS Code to search and read the knowledge base.
Uses SSE transport for Docker deployment.
"""

import json
import logging
import os
import uvicorn
from fastapi import FastAPI

from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport

from tools import search_knowledge, read_note, list_notes, get_project_context, get_skill

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s %(message)s")
logger = logging.getLogger("mcp-server")

# Create FastMCP server
mcp = FastMCP("ai-brain-mcp", instructions="AI-Brain knowledge base query tools")


@mcp.tool(description="Search the AI-Brain knowledge base for relevant notes. Returns chunks with scores.")
def search_knowledge_tool(query: str, top_k: int = 5, folder: str | None = None) -> str:
    """Search the knowledge base for relevant chunks."""
    results = search_knowledge(query=query, top_k=top_k, folder=folder)
    return json.dumps(results, ensure_ascii=False, indent=2)


@mcp.tool(description="Read the full content of a markdown note by its relative path.")
def read_note_tool(filepath: str) -> str:
    """Read the full content of a note."""
    content = read_note(filepath=filepath)
    if content is None:
        return f"Note not found: {filepath}"
    return content


@mcp.tool(description="List all markdown notes, optionally filtered by folder.")
def list_notes_tool(folder: str | None = None) -> str:
    """List all notes."""
    notes = list_notes(folder=folder)
    return json.dumps(notes, ensure_ascii=False, indent=2)


@mcp.tool(description="Get context from all notes related to a specific project.")
def get_project_context_tool(project_name: str, top_k: int = 8) -> str:
    """Get project context."""
    results = get_project_context(project_name=project_name, top_k=top_k)
    return json.dumps(results, ensure_ascii=False, indent=2)


@mcp.tool(description="Retrieve a skill document by name.")
def get_skill_tool(skill_name: str) -> str:
    """Get a skill document."""
    result = get_skill(skill_name=skill_name)
    if result is None:
        return f"Skill not found: {skill_name}"
    return result["content"]


# === SSE Transport for Docker ===
app = FastAPI(title="AI-Brain MCP")
sse = SseServerTransport("/mcp/")


@app.get("/sse")
async def handle_sse(request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await mcp._mcp_server.run(streams[0], streams[1], mcp._mcp_server.create_initialization_options())


@app.post("/mcp/")
async def handle_mcp(request):
    return await sse.handle_post_message(request.scope, request.receive, request._send)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8100"))
    logger.info("MCP Server starting on port %d (SSE transport)", port)
    uvicorn.run(app, host="0.0.0.0", port=port)
