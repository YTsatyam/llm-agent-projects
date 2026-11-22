import re, sqlite3, sys, time, pathlib
import sqlglot
from sqlglot import exp
HERE = pathlib.Path(__file__).resolve().parent
sys.path.append(str(HERE.parent))
from common.llm import chat, SMALL, BIG


DB = HERE / "chinook.db"
BLOCKED = (exp.Insert, exp.Update, exp.Delete, exp.Drop, exp.Create,
           exp.Alter, exp.Command)


def connect():
    return sqlite3.connect(f"file:{DB}?mode=ro", uri=True)  # guardrail 1: read-only


SCHEMA = "\n".join(r[0] for r in connect().execute("SELECT sql FROM sqlite_master WHERE type='table'"))


def validate(sql):  # guardrail 2: validation
    trees = sqlglot.parse(sql, read="sqlite")
    if len(trees) != 1:
        raise ValueError("Only one statement is allowed.")
    tree = trees[0]
    if not isinstance(tree, exp.Query) or any(tree.find(t) for t in BLOCKED):
        raise ValueError("Only read queries are allowed.")
    if isinstance(tree, exp.Select) and not tree.args.get("limit"):
        tree = tree.limit(100)
    return tree.sql(dialect="sqlite")


def run(sql, seconds=3):  # guardrail 3: timeout
    con = connect(); deadline = time.time() + seconds
    con.set_progress_handler(lambda: time.time() > deadline, 10_000)
    cur = con.execute(sql)
    return [d[0] for d in cur.description], cur.fetchall()


def ask_sql(question):
    prompt = f"SQLite schema:\n{SCHEMA}\n\nWrite ONE SQLite query that answers: {question}\nReturn only the SQL."
    sql = chat(SMALL, [{"role": "user", "content": prompt}]).choices[0].message.content
    sql = re.sub(r"```(sql)?", "", sql).strip()
    return validate(sql)


def answer(question):
    sql = ask_sql(question)
    cols, rows = run(sql)
    msg = f"Question: {question}\nColumns: {cols}\nRows: {rows[:20]}\nAnswer in one or two sentences."
    return sql, chat(SMALL, [{"role": "user", "content": msg}]).choices[0].message.content


if __name__ == "__main__":
    sql, text = answer(sys.argv[1]); print(sql, "\n", text)