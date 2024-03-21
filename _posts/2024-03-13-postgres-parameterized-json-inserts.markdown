---
title:  "PostgreSQL parameterized json inserts"
date:   2024-03-13 17:18:25 -0500
categories:
- postgresql
- sql
- database
- data engineering
author: steven
---
## PostgreSQL parameterized update/insert/upsert queries using jsonb columns, which are updated based on existing values

![](</assets/images/article1.png>)

I also published this to [Medium](https://medium.com/@steven.miers_96836/postgresql-parameterized-update-insert-upsert-queries-using-json-or-jsonb-columns-which-are-8c21cd200ba9); my first article there!
The other day, I found myself writing a query for a client to store daily event aggregations with the details stored in a `jsonb` column. Rather than storing discrete events separately, the requirements were to aggregate multiple event metrics into a single row per day for each metric_type, so I chose to use a `postgreSQL` “UPSERT”. There isn’t an actual “UPSERT” statement in postgreSQL; it actually takes the form:

```sql
INSERT INTO table_name ...
ON CONFLICT(field_name) DO
UPDATE SET other_field_name=...
```

Basically, the UPSERT allows us to INSERT a record if none is present for that day and metric_type, and otherwise UPDATE the record with the new data.
Here is the SQL/DDL for creating the table for this example:

```sql
CREATE TABLE IF NOT EXISTS tps.event_metrics
(
    metric_type text COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    metrics jsonb,
    day date
    CONSTRAINT event_metrics_day_metric_type_unique UNIQUE (day, metric_type)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS tps.event_metrics
    OWNER to postgres;

CREATE INDEX IF NOT EXISTS event_metrics_metric_type_index
    ON tps.event_metrics USING btree
    (event_type COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
```

Note the CONSTRAINT clause that will cause a UNIQUE violation if an attempt is made to insert a row with the same day and metric_type.
Essentially the metrics jsonb column is a dictionary with a name for a key and an associated count. I wasn’t exactly sure how to increment the values in the dictionary defined by the jsonb column, and even less how to do this with query parameters. I googled around and found some “solutions” that didn’t work for my situation, and eventually pieced something together that worked perfectly:

```sql
-- Insert that occurs if constraint is not violated:
INSERT INTO
    tps.event_metrics (
        "day", "metric_type", "created_at", "updated_at", "metrics"
    )
VALUES (
    $1, $2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, concat(
        '{',
        '  "requested":', $3::int,
        ', "completed":', $4::int,
        ', "errors":', $5::int,
        ', "with_description":', $6::int,
        ', "with_photos":', $7::int,
        '}'
    )::jsonb
)

-- If there is a conflict, we update and increment:
ON CONFLICT (day, event_type) DO UPDATE SET
    "updated_at" = CURRENT_TIMESTAMP,
    "metrics" = concat(
      '{',
      '  "requested":', COALESCE(event_metrics.metrics->>'requested','0')::int + $3::int,
      ', "completed":', COALESCE(event_metrics.metrics->>'completed','0')::int + $4::int,
      ', "errors":', COALESCE(event_metrics.metrics->>'errors','0')::int + $5::int,
      ', "with_description":', COALESCE(event_metrics.metrics->>'with_description','0')::int + $6::int,
      ', "with_photos":', COALESCE(event_metrics.metrics->>'with_photos','0')::int + $7::int,
      '}'
 )::jsonb

RETURNING *
```

### A few things to note:
* The jsonb “dictionary” is cobbled together using string concatenation. This can get messy, especially with so many entries, so I thought it should at least “look” like a dictionary.
* This is just a subset of what we might store in that column, and this example is modified from the real implementation, which is part of a closed-source project.
* Note the `::jsonb` suffix added to the built-up-dictionary. This was absent on many of the examples I found. I can attest that it is required (we are using version 14 of `postgreSQL`).
* Also note the `::int` suffix used on the parameters, as well as the existing entries in the `jsonb` field.
* `COALESCE` is used so we will always have a valid number to start from, even if these keys are missing from the `jsonb` field.
* The `UPDATE SET` clause requires the field name be qualified with the table name (`event_metrics.metrics`), or a ambiguous reference error is encountered.
* Finally, see the `->>` operator used to access entries in the `jsonb` field.

### Summary
The json and jsonb columns provided by postgreSQL are powerful indeed. It may not be as obvious how to manipulate them when compared to first-order columns. This took me a few hours to figure out; hopefully it will be faster for you.

PostgreSQL provides more than a few functions to extract information and modify information for these fields. See documentation on json and jsonb functions [here](https://www.postgresql.org/docs/current/functions-json.html).

See the documentation on postgreSQL json/jsonb fields [here](https://www.postgresql.org/docs/current/datatype-json.html).
