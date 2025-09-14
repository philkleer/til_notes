# TIL & Notes

> Today I Learned — small, self-contained learning notes and tiny demos.  
> Public and **work-safe** (no company IP).

**Repo:** [https://github.com/philkleer/til-and-notes](https://github.com/philkleer/til-and-notes)

## Structure
```
til/
  YYYY/
    MM/
      YYYY-MM-DD-kebab-title.md
notes/
  case-studies/
    template.md
projects/
  hello-cli/
    hello.py
scripts/
  new_til.py
```
- `til/` — bite-size notes (one per day/topic).
- `notes/case-studies/` — longer write-ups using the template.
- `projects/hello-cli/` — a tiny demo to expand.
- Everything here is personal and generic—no proprietary details.

## Quickstart
```bash
python3 scripts/new_til.py "short title here"
git add . && git commit -m "docs(til): short title" && git push
```

This will create `til/{year}/{month}/YYYY-MM-DD-short-title.md` with a boilerplate header.

## License
MIT (see `LICENSE`).
