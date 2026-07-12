"""Split markdown files into overlapping chunks by headings and paragraphs."""

import re
from config import CHUNK_SIZE, CHUNK_OVERLAP


def _parse_headings(text: str) -> list[tuple[str, str, int]]:
    """
    Split markdown into (heading_chain, content_section, start_line).
    Returns list of (heading_chain, section_text, approx_char_offset).
    """
    lines = text.split("\n")
    sections: list[tuple[str, str, int]] = []
    current_heading = ""
    current_lines: list[str] = []
    offset = 0

    for line in lines:
        heading_match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading_match:
            # Save previous section
            if current_lines:
                sections.append((current_heading, "\n".join(current_lines), offset))
                offset += sum(len(l) + 1 for l in current_lines)
                current_lines = []
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            # Build heading chain: only keep headings at same or higher level
            parent_chain = current_heading.split(" > ")[:-1] if current_heading else []
            parent_chain.append(title)
            current_heading = " > ".join(parent_chain[-3:])  # max depth 3
            current_lines.append(line)
        else:
            current_lines.append(line)

    if current_lines:
        sections.append((current_heading, "\n".join(current_lines), offset))

    return sections


def _chunk_text(text: str, heading: str) -> list[dict]:
    """Further split a section if it exceeds chunk_size."""
    chunks = []
    start = 0
    text_len = len(text)

    if text_len <= CHUNK_SIZE:
        return [{"heading": heading, "content": text}]

    while start < text_len:
        end = min(start + CHUNK_SIZE, text_len)
        # Try to break at a paragraph boundary
        if end < text_len:
            # Look backwards for double newline
            break_point = text.rfind("\n\n", start, end)
            if break_point > start:
                end = break_point + 2  # include the newlines in current chunk
        chunk_text = text[start:end].strip()
        if chunk_text:
            chunks.append({"heading": heading, "content": chunk_text})
        start = end - CHUNK_OVERLAP if end < text_len else text_len

    return chunks


def chunk_markdown(filepath: str) -> list[dict]:
    """
    Read a markdown file and return chunks.
    Each chunk: {"filepath": str, "heading": str, "content": str, "chunk_index": int}
    """
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    title = filepath.rsplit("/", 1)[-1].replace(".md", "")
    sections = _parse_headings(text)
    chunks = []
    chunk_idx = 0

    for heading, section_text, _offset in sections:
        effective_heading = heading if heading else title
        for sub_chunk in _chunk_text(section_text, effective_heading):
            # Skip empty/tiny chunks
            if len(sub_chunk["content"]) < 20:
                continue
            chunks.append({
                "filepath": filepath,
                "heading": sub_chunk["heading"],
                "content": sub_chunk["content"],
                "chunk_index": chunk_idx,
            })
            chunk_idx += 1

    return chunks
