# -*- coding: utf-8 -*-
"""
sync_from_db.py — 把 DB 当前真实 prompt 拉到本地文件（用于比对/审计）
用法:
  python3 scripts/sync_from_db.py <task_id>
  python3 scripts/sync_from_db.py --all
注意: 会**覆盖**本地 automations/<id>/prompt.md，仅用于"看线上真实状态"，
      不反向污染 DB。覆盖前自动备份为 prompt.db_bak.md。
"""
import sqlite3, os, json, sys, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = "/Users/jungle1499/.workbuddy/workbuddy.db"
REG = os.path.join(ROOT, "REGISTRY.json")

def pull_one(tid, meta):
    pf = os.path.join(ROOT, meta["prompt_file"])
    con = sqlite3.connect(DB); cur = con.cursor()
    cur.execute("SELECT prompt FROM automations WHERE id=?", (tid,))
    row = cur.fetchone(); con.close()
    if not row or row[0] is None:
        print(f"  [跳过] {tid} DB 无 prompt")
        return
    if os.path.exists(pf):
        shutil.copy(pf, pf + ".db_bak.md")
    os.makedirs(os.path.dirname(pf), exist_ok=True)
    open(pf, "w", encoding="utf-8").write(row[0])
    print(f"  [已拉取] {tid} ({meta['name']}) 备份原文件为 prompt.db_bak.md")

def main():
    args = sys.argv[1:]
    reg = json.load(open(REG, encoding="utf-8"))
    if "--all" in args:
        for tid, meta in reg["tasks"].items():
            pull_one(tid, meta)
    elif args:
        for tid in args:
            if tid in reg["tasks"]:
                pull_one(tid, reg["tasks"][tid])
            else:
                print(f"  [未知] {tid}")
    else:
        print("用法: sync_from_db.py <task_id> | --all")
        sys.exit(2)
    print("完成。本地文件已反映 DB 真实状态（原文件备份为 .db_bak.md）。")

if __name__ == "__main__":
    main()
