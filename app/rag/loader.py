from pathlib import Path


def load_knowledge_base(path: str = "data/restaurant/knowledge_base.md") -> list[dict[str, str]]:
    content = Path(path).read_text(encoding="utf-8")

    sections = []
    current_title = "General"
    current_lines: list[str] = []

    for line in content.splitlines():
        if line.startswith("## "):
            if current_lines:
                sections.append(
                    {
                        "section": current_title,
                        "content": "\n".join(current_lines).strip(),
                    }
                )

            current_title = line.replace("## ", "").strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_lines:
        sections.append(
            {
                "section": current_title,
                "content": "\n".join(current_lines).strip(),
            }
        )

    return sections
