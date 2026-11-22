import json
from text2sql import run

for i, line in enumerate(open("tests.jsonl", encoding="utf-8"), 1):
    if not line.strip():
        print(f"{i:2}. BLANK LINE - delete it")
        continue
    c = json.loads(line)
    try:
        cols, rows = run(c["gold_sql"])
    except Exception as e:
        print(f"{i:2}. ERROR: {e}")
        continue
    flags = []
    if len(rows) > 100:
        flags.append("OVER 100 ROWS")
    if any(v is None for r in rows for v in r):
        flags.append("HAS NULL")
    show = rows if len(rows) <= 5 else rows[0]
    print(f"{i:2}. {len(rows):3} rows  {show}  {' '.join(flags)}")