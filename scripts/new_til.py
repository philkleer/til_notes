#!/usr/bin/env python3
import sys, os, datetime, re, textwrap

def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'\s+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s or "til"

def main():
    if len(sys.argv) < 2:
        print("Usage: new_til.py \"short title\"")
        sys.exit(1)
    title = sys.argv[1]
    today = datetime.date.today()
    slug = slugify(title)
    rel_dir = os.path.join("til", f"{today.year}", f"{today.month:02d}")
    os.makedirs(rel_dir, exist_ok=True)
    path = os.path.join(rel_dir, f"{today.isoformat()}-{slug}.md")
    if os.path.exists(path):
        print(f"Refusing to overwrite existing file: {path}")
        sys.exit(2)
    content = textwrap.dedent(f"""
    ---
    title: "{title}"
    date: {today.isoformat()}
    tags: []
    ---

    <Write a few bullet points about what you learned today. Keep it brief.>
    """).strip() + "\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created {path}")

if __name__ == "__main__":
    main()
