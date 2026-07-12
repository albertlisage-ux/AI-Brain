#!/usr/bin/env python3
"""
AI-Brain MCP Server

Provides MCP tools for Codex / VS Code to search and read the knowledge base.
Listens on stdio (for MCP) or HTTP (for testing).
"""

import json
import logging
import sys

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

from tools import search_knowledge, read_note, list_notes, get_project_context, get_skill

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s %(message)s")
logger = logging.getLogger("mcp-server")

server = Server("ai-brain-mcp")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    return [
        Tool(
            name="search_knowledge",
            description="Search the AI-Brain knowledge base for relevant notes. Returns chunks with scores.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query"},
                    "top_k": {"type": "number", "description": "Number of results (default 5)", "default": 5},
                    "folder": {"type": "string", "description": "Optional folder filter (e.g. '03 Skills')"},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="read_note",
            description="Read the full content of a markdown note by its relative path.",
            inputSchema={
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Relative path to the note (e.g. '03 Skills/pdf-skill.md')"},
                },
                "required": ["filepath"],
            },
        ),
        Tool(
            name="list_notes",
            description="List all markdown notes, optionally filtered by folder.",
            inputSchema={
                "type": "object",
                "properties": {
                    "folder": {"type": "string", "description": "Optional folder filter"},
                },
            },
        ),
        Tool(
            name="get_project_context",
            description="Get context from all notes related to a specific project.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {"type": "string", "description": "Project name (e.g. 'LinkTech-hydraulic')"},
                    "top_k": {"type": "number", "description": "Number of results (default 8)", "default": 8},
                },
                "required": ["project_name"],
            },
        ),
        Tool(
            name="get_skill",
            description="Retrieve a skill document by name.",
            inputSchema={
                "type": "object",
                "properties": {
                    "skill_name": {"type": "string", "description": "Skill name (e.g. 'pdf-skill')"},
                },
                "required": ["skill_name"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent | ImageContent | EmbeddedResource]:
    logger.info("Tool called: %s %s", name, arguments)

    try:
        if name == "search_knowledge":
            results = search_knowledge(
                query=arguments["query"],
                top_k=int(arguments.get("top_k", 5)),
                folder=arguments.get("folder"),
            )
            output = json.dumps(results, ensure_ascii=False, indent=2)
            return [TextContent(type="text", text=output)]

        elif name == "read_note":
            content = read_note(filepath=arguments["filepath"])
            if content is None:
                return [TextContent(type="text", text=f"Note not found: {arguments['filepath']}")]
            return [TextContent(type="text", text=content)]

        elif name == "list_notes":
            notes = list_notes(folder=arguments.get("folder"))
            output = json.dumps(notes, ensure_ascii=False, indent=2)
            return [TextContent(type="text", text=output)]

        elif name == "get_project_context":
            results = get_project_context(
                project_name=arguments["project_name"],
                top_k=int(arguments.get("top_k", 8)),
            )
            output = json.dumps(results, ensure_ascii=False, indent=2)
            return [TextContent(type="text", text=output)]

        elif name == "get_skill":
            result = get_skill(skill_name=arguments["skill_name"])
            if result is None:
                return [TextContent(type="text", text=f"Skill not found: {arguments['skill_name']}")]
            return [TextContent(type="text", text=result["content"])]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        logger.exception("Tool error")
        return [TextContent(type="text", text=f"Error: {e}")]


async def main():
    async with server.run(
        InitializationOptions(
            server_name="ai-brain-mcp",
            server_version="1.0.0",
            capabilities=server.get_capabilities(
                notification_options=NotificationOptions(),
                experimental_capabilities={},
            ),
        ),
    ):
        logger.info("MCP Server running on stdio")
        # Keep running
        import asyncio
        while True:
            await asyncio.sleep(3600)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
