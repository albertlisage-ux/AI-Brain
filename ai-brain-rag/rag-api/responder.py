"""Generate answers using DeepSeek API."""

import httpx
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_BASE, DEEPSEEK_MODEL


def build_prompt(question: str, context_chunks: list[dict]) -> str:
    """Build a prompt with retrieved context for DeepSeek."""
    context_parts = []
    for i, chunk in enumerate(context_chunks):
        source = f"[{chunk['filepath']} → {chunk['heading']}]"
        context_parts.append(f"### {source}\n{chunk['content']}")

    context_str = "\n\n".join(context_parts)

    prompt = f"""You are an AI assistant with access to a personal knowledge base. Answer based on the provided context. If context is insufficient, say so. Do NOT list source citations in your answer — the UI will show them separately.

## Context

{context_str}

## Question

{question}

## Answer
"""
    return prompt


async def ask_deepseek(question: str, context_chunks: list[dict]) -> str:
    """Send a prompt to DeepSeek and return the answer."""
    if not DEEPSEEK_API_KEY:
        return "Error: DEEPSEEK_API_KEY is not configured."

    prompt = build_prompt(question, context_chunks)

    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(
            f"{DEEPSEEK_API_BASE}/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": DEEPSEEK_MODEL,
                "messages": [
                    {"role": "system", "content": "You are a helpful knowledge base assistant. Answer concisely and cite sources."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.3,
                "max_tokens": 2048,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
