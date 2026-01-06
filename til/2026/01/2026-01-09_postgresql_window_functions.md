# TIL: Learning Window Functions in PostgreSQL (with Practical Examples)
_Date: 2026-01-09_

Today I learned how **window functions** in PostgreSQL allow you to perform analytical calculations **across rows related to the current row**, *without collapsing results like `GROUP BY` does*.  
They are essential for rankings, running totals, comparisons over time, and advanced reporting.

---

## 🪟 What are Window Functions?

A **window function** performs a calculation over a *window* of rows:

```sql
<function>() OVER (
  PARTITION BY ...
  ORDER BY ...
  ROWS BETWEEN ...
)
```

Key difference from aggregation:
- `GROUP BY` → reduces rows
- **Window functions** → keep all rows

---

## 🔑 Core Clauses

### `PARTITION BY`
Splits data into independent groups.

```sql
AVG(sales) OVER (PARTITION BY region)
```

---

### `ORDER BY`
Defines row order *inside* the partition.

```sql
SUM(sales) OVER (PARTITION BY region ORDER BY day)
```

---

### Frames (`ROWS BETWEEN ...`)
Controls *how much* of the partition is used.

```sql
SUM(sales) OVER (
  PARTITION BY region
  ORDER BY day
  ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
)
```

---

## 🔄 Value Navigation Functions

### `LAG()` / `LEAD()`

```sql
LAG(sales)  OVER (PARTITION BY region ORDER BY day) AS prev_sales,
LEAD(sales) OVER (PARTITION BY region ORDER BY day) AS next_sales
```

---

### `FIRST_VALUE()` / `LAST_VALUE()`

```sql
FIRST_VALUE(sales) OVER (
  PARTITION BY region
  ORDER BY day
)

LAST_VALUE(sales) OVER (
  PARTITION BY region
  ORDER BY day
  ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)
```

⚠️ `LAST_VALUE()` requires explicit frame expansion.

---

## 🏆 Ranking Functions

```sql
RANK()       OVER (PARTITION BY region ORDER BY sales DESC)
DENSE_RANK() OVER (PARTITION BY region ORDER BY sales DESC)
NTILE(4)     OVER (ORDER BY sales DESC)
```

---

## 📊 Aggregate Window Functions

```sql
MAX(value) OVER (PARTITION BY group_id)
SUM(value) OVER (PARTITION BY group_id)
AVG(value) OVER (PARTITION BY group_id)
MIN(value) OVER (PARTITION BY group_id)
```

---

## 🧵 `STRING_AGG()` as Window Function

```sql
STRING_AGG(user_name, ', ')
  OVER (PARTITION BY team)
```

---

## 🧩 Handling Missing Values

```sql
COALESCE(LAG(value) OVER (...), 0)
```

---

## 🧠 Advanced SQL Concepts

### Pivoting

```sql
SUM(value) FILTER (WHERE category = 'A') OVER (...)
```

---

### Rollup & Cube

```sql
GROUP BY ROLLUP(region, state)
GROUP BY CUBE(region, state)
```

---

## 💡 Practical Pattern: Filtering with CTEs

```sql
WITH region_filter(region) AS (
  VALUES ('Norte'), ('Nordeste')
)
SELECT *
FROM measurements m
JOIN region_filter rf ON rf.region = m.region;
```

---

## 📐 Weighted Aggregation Pattern

```sql
ROUND(
  (SUM(avg_tcp * n) / SUM(n))::numeric,
  1
) AS avg_tcp_down_median_mbps
```

---

## 🧠 Key Takeaways

- Window functions keep row-level detail
- Frames matter, especially for `LAST_VALUE`
- Ranking functions avoid self-joins
- CTEs + windows = readable analytics SQL
