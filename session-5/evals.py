# Code-based evaluation functions for LinkedIn post generation

import re


def check_no_banned_phrases(llm_output: str) -> dict:
    """Check that the output does not contain banned phrases like 'no fluff' or 'no hacks'."""
    banned_phrases = [
        "no fluff",
        "no-fluff",        # hyphen-minus (U+002D)
        "no\u2011fluff",   # non-breaking hyphen (U+2011)
        "no hacks",
        "no-hacks",        # hyphen-minus (U+002D)
        "no\u2011hacks",   # non-breaking hyphen (U+2011)
    ]
    text_lower = llm_output.lower()
    found = []
    for phrase in banned_phrases:
        if phrase in text_lower:
            found.append(phrase)

    if found:
        return {"passed": False, "details": f"found: {', '.join(repr(p) for p in found)}"}
    return {"passed": True, "details": ""}


def check_no_tricolons(llm_output: str) -> dict:
    """Check that the output does not contain tricolon patterns."""
    # Pattern 1: Comma-separated tricolons — "X, Y, and Z" or "X, Y, & Z"
    comma_pattern = r"\b\w[\w\s]*,\s+\w[\w\s]*,\s+(?:and|&)\s+\w[\w\s]*\b"

    # Pattern 2: Period-separated tricolons on the same line — "X. Y. Z."
    period_pattern = r"(?<!\.\.)([A-Z][^.!?\n]+\.)\s+([A-Z][^.!?\n]+\.)\s+([A-Z][^.!?\n]+\.)"

    # Pattern 3: Newline-separated tricolons — three short parallel phrases on consecutive lines
    newline_pattern = r"\n([^\n]{5,60})\n\n([^\n]{5,60})\n\n([^\n]{5,60})\n"

    # Check comma-separated tricolons
    match = re.search(comma_pattern, llm_output, re.IGNORECASE)
    if match:
        return {"passed": False, "details": f"tricolon (comma-separated): '{match.group().strip()}'"}

    # Check period-separated tricolons with structural similarity filter
    for match in re.finditer(period_pattern, llm_output):
        a, b, c = match.group(1).strip(), match.group(2).strip(), match.group(3).strip()
        lengths = [len(a), len(b), len(c)]
        avg = sum(lengths) / 3
        # Only flag if each sentence is short (≤50 chars) and similar length (within 2× of average)
        # Real tricolons are punchy ("I came. I saw. I conquered."), not full paragraphs
        if all(l <= 30 for l in lengths) and all(l > avg * 0.4 and l < avg * 2.0 for l in lengths):
            snippet = f"{a} {b} {c}"
            return {"passed": False, "details": f"tricolon (period-separated): '{snippet}'"}

    # For newline pattern, only flag if all three segments are structurally similar
    # (similar length, don't start with a number — to avoid flagging listicles)
    for match in re.finditer(newline_pattern, llm_output):
        a, b, c = match.group(1).strip(), match.group(2).strip(), match.group(3).strip()
        # Skip if any segment starts with a number (listicle item)
        if any(re.match(r"^\d", seg) for seg in (a, b, c)):
            continue
        lengths = [len(a), len(b), len(c)]
        avg = sum(lengths) / 3
        # Flag if all three are within 2x of each other's length
        if all(l > avg * 0.4 and l < avg * 2.0 for l in lengths):
            snippet = f"{a} / {b} / {c}"
            return {"passed": False, "details": f"tricolon (newline-separated): '{snippet}'"}

    return {"passed": True, "details": ""}


def check_em_dash_count(llm_output: str) -> dict:
    """Check that the output contains at most one em dash."""
    count = llm_output.count("—")
    passed = count <= 1
    return {"passed": passed, "details": f"em dash count: {count}"}
