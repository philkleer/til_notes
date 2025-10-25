# TIL: Using `goose` for lightweight database migrations
_Date: 2025-10-10_

## Context
I needed a lightweight way to manage **SQL schema migrations** for a project, without adding heavy ORM tooling.  
The [`goose`](https://github.com/pressly/goose) CLI turned out to be a clean solution.

## Why Goose
- Minimal overhead: migrations are plain `.sql` or `.go` files.
- Versioning built-in via an internal migrations table.
- Easy to integrate with CI/CD or local workflows.

## Example workflow
```bash
# Create a new migration
goose create add_users_table sql

# Apply all pending migrations
goose up

# Roll back the last migration
goose down
```

Each migration file includes an **up** and **down** section:
```sql
-- +goose Up
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- +goose Down
DROP TABLE users;
```

## Lessons Learned
- Migrations stay transparent and version-controlled.
- Simple enough for both developers and CI.
- Ideal for smaller projects that don’t need a full ORM.

## References
- [Pressly/goose GitHub](https://github.com/pressly/goose)
