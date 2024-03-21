---
title:  "PostgreSQL — returning records from queries"
date:   2024-03-15 17:18:25 -0500
categories:
- postgresql
- sql
- database
- data engineering
author: steven
---
### PostgreSQL — returning records from insert/update queries
I also published this to [Medium](https://terracoil.com/postgresql-returning-records-from-insert-update-queries-7b700853f1a8);

![](</assets/images/article2.png>)

You may have seen this:
```sql
INSERT INTO tps.labels ("name", "description") VALUES ($1, $2)
RETURNING *
```

So what if there is a UNIQUE constraint on “name”? If you insert a duplicate, you will not only get an unique violation error, there will be no record returned. If you modify the query as follows, you won’t get an error. Nothing is returned, even though the row is present in the database table:

```sql
INSERT INTO tps.labels ("name", "ascii_name", "description")
    VALUES ($1, $2, $3)
    ON CONFLICT(name) DO NOTHING
RETURNING *
```

If you need the record returned, even if it was already there, there are a number of things you can [try](https://stackoverflow.com/questions/18192570/insert-if-not-exists-else-return-id-in-postgresql). This is what works best and most cleanly for our situation:

```sql
WITH e AS(
    INSERT INTO tps.labels ("name", "description")
        VALUES ($1, $2)
    ON CONFLICT(name) DO NOTHING
    RETURNING *
)

SELECT * FROM e UNION
SELECT * from tps.labels WHERE name=$1;
```

### Note
If you need only the “id” or some subset of columns, replace the * with those column names.

### Summary
This is a reliable way to always return records from an `INSERT` or `UPDATE` query; even those that don't affect records (due to a constraint or other expected behavior).  It is accomplished via the `SELECT`/`UNION` query at the bottom.