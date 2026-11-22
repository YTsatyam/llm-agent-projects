import json, sys, time
from text2sql import ask_sql, run

tag = sys.argv[1] if len(sys.argv) > 1 else "v1"
test_file = sys.argv[2] if len(sys.argv) > 2 else "tests.jsonl"
cases = [json.loads(l) for l in open(test_file, encoding="utf-8") if l.strip()]
correct, log = 0, []

for i, c in enumerate(cases, 1):
    sql = None
    try:
        sql = ask_sql(c["question"])
        got = sorted(map(tuple, run(sql)[1]), key=repr)
        want = sorted(map(tuple, run(c["gold_sql"])[1]), key=repr)
        ok = got == want
        status = "ok" if ok else "wrong rows"
    except Exception as e:
        ok, status = False, f"error: {e}"
    correct += ok
    log.append({"n": i, "question": c["question"], "agent_sql": sql,
                "gold_sql": c["gold_sql"], "correct": ok, "status": status})
    print(f"{i:2}. {'OK  ' if ok else 'FAIL'} {c['question'][:70]}" + ("" if ok else f"  [{status}]"))
    time.sleep(4)  # stay under the free tier's per-minute limit

print(f"\n{correct}/{len(cases)} correct")
with open(f"results_{tag}.json", "w", encoding="utf-8") as f:
    json.dump({"version": tag, "score": correct, "total": len(cases), "cases": log},
              f, indent=2, ensure_ascii=False)