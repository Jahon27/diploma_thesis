import re

def clean_generated_code(content: str | None) -> str:
    if not content or not content.strip():
        raise RuntimeError("LLM returned empty code.")

    code = content.strip()
    # Remove an opening Markdown code fence.
    code = re.sub(r"\A```(?:python|py)?[ \t]*\r?\n","", code, flags=re.IGNORECASE,)
    # Remove a closing Markdown code fence.
    code = re.sub(r"\r?\n```[ \t]*\Z", "", code,)
    return code.strip() + "\n"
