# TIL: Using `ellmer`, `gander`, `chores`, and `ensure` to Draft R Docs + Tests with an Ollama Connection
_Date: 2026-01-15_

Today I learned a practical workflow for **LLM-assisted R package development** using four complementary tools:

- **`ellmer`**: the core chat interface to LLM providers (including Ollama).
- **`gander`**: a low-friction in-editor chat that streams responses into your project.
- **`chores`**: “assistants” that *do* specific tasks (rewrite code, draft docs, etc.) from a selection.
- **`ensure`**: an addin focused on **LLM-assisted unit test generation**.

The big win: you can generate **documentation and tests directly in your project** (instead of copy/paste from a browser), then iterate quickly.

---

## ✅ Prereqs

You'll need to set the `OLLAMA_BASE_URL` in the environment (recommended via `.Renviron`):

```r
usethis::edit_r_environ()
```

Put the definition of your base URL there: 

```text
OLLAMA_BASE_URL=http://localhost:11434
```

Usually Ollama does not require credentials, only if you're accessing Ollama behind a secured endpoint that enforces authentication, you’ll need an **Ollama API key** in your environment. 

Add a line like:

```text
OLLAMA_API_KEY=your_key_here
```

Restart R so the environment variable is loaded.

---

## 1) `ellmer`: the engine for chat + tool calling

At the lowest level, `ellmer` gives you a unified interface to providers. A minimal Ollama chat:

```r
library(ellmer)

chat <- chat_ollama(
  model = "qwen3-coder"  # example model; pick what you have access to
)

chat$chat("Write roxygen2 documentation for an R function that downloads a CSV and validates columns.")
```

### Why I like it
- One API for multiple providers
- Streaming support
- Works nicely as a foundation for other tooling

---

## 2) `gander`: chat that understands your project context

`gander` is the "chat in the IDE" layer. Instead of pasting context manually, it can incorporate:
- the code you’re working on
- objects in your environment
- relevant project files (depending on setup)

Typical usage pattern:
1. select some code (or place cursor in a function)
2. trigger the gander addin via keybinding
3. ask for improvements / documentation / explanation
4. it streams the response **directly into your editor**

**Great for:**
- explaining what a function does
- proposing refactors
- drafting doc sections from existing code

---

## 3) `chores`: assistants for "do this repetitive thing"

`chores` is designed around **helpers** that run on a code selection. Examples of `chores`:
- rewrite / refactor selected code
- draft roxygen docs for a function
- generate a vignette outline
- convert base → tidyverse (or the other way around)

A key idea: you can create your own custom assistants by writing short prompt files.

### Custom helper example (concept)
Create a Markdown prompt file like:

```text
my-roxygen-replace.md
```

…and write instructions describing what should happen to the selected code (e.g., "replace selection with a roxygen2 block in English, include params/return/examples, keep it concise").

Then load your helper directory (depending on your setup):

```r
library(chores)
directory_load()
```

Now you can trigger the chores addin, pick your helper, and it will **apply the transformation**.

---

## 4) `ensure`: generate unit tests with {testthat}

`ensure` is laser-focused on writing unit tests. Workflow I’m trying:

1. write a small function (or select part of it)
2. run the ensure addin
3. it drafts a test file / test blocks
4. I edit assertions and edge cases until they match my standards

This pairs well with a test-first mindset:
- start with a single function
- generate tests incrementally
- keep refining prompts by editing the generated tests

Example shape of output (what I aim for):

```r
test_that("parse_input() rejects missing columns", {
  df <- tibble::tibble(a = 1)
  expect_error(parse_input(df), "missing column")
})

test_that("parse_input() returns standardized types", {
  df <- tibble::tibble(a = "1", b = "2025-01-01")
  out <- parse_input(df)
  expect_true(is.integer(out$a))
})
```

---

## Putting it together: a workflow that feels "native" in RStudio/Positron

### My mental model
- **ellmer** = the chat engine (provider + API)
- **gander** = "conversational pairing" inside the project
- **chores** = quick task automation on a code selection
- **ensure** = targeted unit test generation

### Practical loop I’m using
1. Implement or refactor a function.
2. Use **chores** to draft roxygen docs from the function body.
3. Use **gander** to review clarity, naming, and edge cases (with project context).
4. Use **ensure** to generate tests, then tighten them by hand.
5. Run `R CMD check` and iterate.

---

## Define "house style" prompts with `AGENTS.md`

`AGENTS.md` is a README.md for agents: a dedicated, predictable place to provide the context and instructions to help AI coding agents work on your project. It inherits detailed context coding that agents need: build steps, tests, and conventions that might clutter a README or aren’t relevant to human contributors.

Some agents directly search for `AGENTS.md` inside the repo, like the VSCode extension `Continue` or `Github Copilot`. 

To create `AGENTS.md` there exist three clear rules:
- Give agents a clear, predictable place for instructions.
- Keep READMEs concise and focused on human contributors.
- Provide precise, agent-focused guidance that complements existing README and docs.

I created my `AGENTS.md` with sections for R and Python, since I'm using both languages in my projects. See my full example [`here: AGENTS.md`](./AGENTS.md).

--- 

## What I’ll refine next

- Turn my informal preferences (naming, error messages, documentation tone) into explicit **"house style" prompts** that I can reuse across projects.
- Build a small library of **custom chores helpers** for patterns I repeat often:
  - input validation + informative errors
  - cli messaging
  - standard roxygen2 blocks
- Tighten my **test-generation loop** with `ensure` by:
  - adding more edge-case–focused prompts
  - enforcing my preferred assertion patterns
- Experiment with different Ollama models to see which ones perform best for:
  - documentation vs.
  - refactoring vs.
  - test generation

---

## Key Takeaways

- LLM-assisted development works best when tools are **specialized**, not generic.
- Separating concerns matters:
  - chatting ≠ task execution ≠ test generation.
- Keeping everything **inside the project** (via `gander`, `chores`, `ensure`) removes friction and encourages iteration.
- Good results depend less on "clever prompts" and more on:
  - clear conventions
  - explicit instructions
  - fast feedback loops.
- An `AGENTS.md` file is a powerful way to encode project-specific expectations so AI output stays aligned over time.
