import asyncio, json, pathlib, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).resolve().parent
sys.path.append(str(HERE))
from agent import ask

lines = (HERE / "tasks.jsonl").read_text(encoding="utf-8").splitlines()
tasks = [json.loads(l) for l in lines if l.strip()]
results, tool_ok, ans_ok = [], 0, 0

for i, t in enumerate(tasks, 1):
    answer, used = "", []
    for attempt in range(3):                        # retry on rate-limit errors
        try:
            answer, used = asyncio.run(ask(t["question"]))
            break
        except Exception as e:
            answer = f"ERROR: {e}"
            if "429" in str(e):
                time.sleep(30)
            else:
                break
    answer = answer or ""
    right_tool = bool(used) and used[0] == t["expected_tool"]
    right_answer = all(k.lower() in answer.lower() for k in t["answer_contains"])
    tool_ok += right_tool
    ans_ok += right_answer
    print(f"{i:2}. tool {'OK ' if right_tool else 'BAD'} | answer {'OK ' if right_answer else 'BAD'} | used={used}")
    results.append({"n": i, "question": t["question"], "expected_tool": t["expected_tool"],
                    "tools_used": used, "right_tool": right_tool,
                    "right_answer_auto": right_answer, "answer": answer})
    time.sleep(5)                                   # stay under the per-minute limit

print(f"\nTool choice: {tool_ok}/{len(tasks)}   Auto-checked answers: {ans_ok}/{len(tasks)}")
(HERE / "results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")