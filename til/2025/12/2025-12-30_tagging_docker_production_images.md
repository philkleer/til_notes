# 🧠 TIL: Getting Docker Image Tags Right in a Company Harbor Registry
_Date: 2025-12-30_

Today I learned (the hard way) how **clear Docker image tagging rules** make a big difference when working with a company Harbor registry and CI/CD pipelines. 

This note documents the **decisions, rationale, and pitfalls** I encountered while cleaning up image tags for *development* vs *production* builds.

## 🎯 The Core Problem

Over time, our image tagging strategy became confusing:

- Tags like **`latest`** and **`current`** were ambiguous.
- Development images were versioned, even though they change frequently.
- It wasn’t always obvious which image was **safe for production**.
- CI pipelines sometimes rebuilt the same image twice.

This made it harder to reason about:
- what was deployed,
- what was still under development,
- and which image should be pulled by default.

## 🧩 New Tagging Rules I Introduced

### 1) Non-`main` branches → *development images*

For any branch that is **not** `main`, the pipeline now pushes:

- `dev`
- `dev-<commit-sha>`

```text
image:dev
image:dev-a1b2c3d
```

**Why this works well**
- No need to update the `VERSION` file during development.
- `dev` always points to the *latest development build*.
- `dev-<commit>` uniquely identifies a specific build for debugging or rollback.

### 2) Merges into `main` → *production images*

For merge requests into `main`:

1. The pipeline still builds a development image (as above).
2. When a release commit is detected:
   - the `VERSION` file changes
   - commit message matches `New version release X.Y.Z`
3. The pipeline:
   - tags the image with the semantic version
   - adds a **`prod`** tag to indicate the production image

**Meaning**
- `prod` = *the image currently used in production*, always points to the *latest production build*
- version tags = immutable historical releases for debugging or rollback.

## 🔁 Simplifying the Build Tags

Previously, we had multiple mutable tags:
- `DOCKER_DEV_TAG`
- `DOCKER_CURRENT_TAG`

I replaced this with a single, explicit variable:

```makefile
DOCKER_BUILD_TAG
```

Now the pipeline controls intent explicitly:

```bash
make DOCKER_BUILD_TAG=dev docker-push
make DOCKER_BUILD_TAG=prod docker-push-release
```

**Benefits**
- Fewer moving parts
- Clear semantics
- Less accidental misuse of *current* vs *latest*

## 🧠 Naming Matters: `prod` vs `latest`

One key insight: **names encode assumptions**.

- `latest` → ambiguous (latest *what*?)
- `current` → unclear lifecycle
- `prod` / `dev` → explicit and intentional

Using `prod` / `dev` makes it immediately obvious which image:
- is deployed,
- should be pulled by default in production/development,
- and represents a stable release (`prod`).

## 🧠 Key Takeaways

- Separate **development** and **production** tags clearly.
- Development images should be mutable; production images should not.
- Avoid ambiguous tags like `latest` when intent matters.
- Encode meaning in tag names (`dev`, `prod`, version numbers).
- CI/CD pipelines should reflect lifecycle stages explicitly.
- Regularly review pipelines for redundant or duplicated steps.
