# SQL Style Guide Summary

This document summarizes key rules and best practices for SQL in analytics engineering, aligned with SQLFluff and modern dbt modeling standards.

## 1. Capitalisation & Casing

- **Keywords:** Strictly lowercase (`select`, `from`, `where`, `join`, `on`, `group by`, `order by`, `with`, `as`, `case`, `when`, `then`, `else`, `end`).
- **Functions:** Strictly lowercase (`count`, `sum`, `coalesce`, `date_trunc`, `try_to_timestamp_ntz`).
- **Identifiers:** Strictly `snake_case` for table, view, CTE, and column names (`school_id`, `created_at`, `stg_kamino__policies`).
- **Data Types:** Strictly lowercase (`varchar`, `number`, `boolean`, `timestamp_ntz`, `date`).
- **Literals:** Strictly lowercase (`null`, `true`, `false`).

## 2. Query Structure & CTEs

- **Use CTEs over Subqueries:** Structure models using Common Table Expressions rather than nested subqueries.
- **CTE Layout Convention:**
  1. **Import CTEs:** Clean 1:1 projections of upstream `ref()` or `source()` models.
  2. **Logical / Transform CTEs:** Joins, aggregations, and business transformations.
  3. **Final Select:** Simple `select * from final` (or explicit column selection).

## 3. Aliasing & Projections

- **Explicit `as`:** Always include the `as` keyword for table and column aliases (`from my_table as t`, `select col as renamed_col`).
- **Avoid `select *`:** In marts and downstream models, explicitly enumerate selected columns.
- **Type Casting:** Prefer concise shorthand casting `column::datatype` (e.g., `user_id::varchar`) when supported by the dialect.

## 4. Semantic Views (Snowflake / dbt_semantic_view)

- **Reversed Alias Semantics in Semantic View DDL:**
  \`\`\`sql
  -- Standard SQL:  source_column AS alias
  -- Semantic DDL:  table.SEMANTIC_NAME as SOURCE_COLUMN
  \`\`\`
- Semantic views emit \`SEMANTIC VIEW\` DDL and are excluded from standard SQLFluff linting due to parser grammar divergence.
- Semantic metric expressions reference source column names (the right side).

## 5. Quality & Linting

- Run \`dbt lint\` (or \`sqlfluff lint\`) on all changed models prior to committing (excluding semantic views).
- Do not disable linting rules globally; use inline \`-- noqa: <RULE>\` only for verified exceptional cases.
