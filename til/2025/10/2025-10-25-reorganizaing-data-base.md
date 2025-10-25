# TIL: Reorganizing a database and structuring migrations for cleaner data flow
_Date: 2025-10-25_

## Context
I was restructuring an existing database to adopt new data patterns and normalize parts of the schema.  
At the same time, I wanted a clear folder layout to separate different phases of data handling.

## Folder structure
```
data/
├── input/          # raw source data
├── processed/      # transformed/intermediate data
└── migration/      
    ├── scripts/    # Goose migrations
    ├── logs/       
    └── output/     # post-migration exports
```

## Approach
1. Designed **new schemas** and documented relationships before applying migrations.  
2. Used SQL migration files and tracked them with `goose` for reproducibility.  
3. Split the data workflow into stages (input → processed → migrated output).  
4. Validated migrated data with checksums and sample queries.

## Results
- Clear boundary between raw and processed data.
- Easier rollbacks since all migrations and transformations are versioned.
- Smooth onboarding for new developers — folder layout reflects the data lifecycle.

## Lessons Learned
- Folder organization matters as much as schema design.
- Version-controlled migration scripts make schema evolution safer.
- Logging and exporting outputs help verify migration success.
