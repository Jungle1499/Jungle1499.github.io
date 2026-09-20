# -*- coding: utf-8 -*-
"""
sync_to_db.py — 把文件(prompt.md) 同步到 DB（发布改动）
用法:
  python3 scripts/sync_to_db.py <task_id>       # 同步单个
  python3 scripts/sync_to_db.py --all            # 同步全部 REGISTRY 任务
注意: 会写 workbuddy.db 的 prompt 字段，并强制 model_id='hy3'。
      执行前请确保已 git commit 文件改动。
"""
import sqlite3, os, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = "/Users/jungle1499/.workbuddy/workbuddy.db"
REG = os.path.join(ROOT, "REGISTRY.json")

def sync_one(tid, meta):
    pf = os.path.join(ROOT, meta["prompt_file"])
    if not os.path.exists(pf):
        print(f"  [跳过] {tid} 文件不存在: {pf}")
        return False
    txt = open(pf, encoding="utf-8").read()
    con = sqlite3.connect(DB); cur = con.cursor()
    cur.execute("SELECT prompt,model_id FROM automations WHERE id=?", (tid,))
    row = cur.fetchone()
    if not row:
        print(f"  [跳过] {tid} DB 不存在")
        con.close(); return False
    old_prompt, old_model = row
    expect_model = meta.get("model", "hy3")
    cur.execute("UPDATE automations SET prompt=?, model_id=? WHERE id=?", (txt, expect_model, tid))
    con.commit(); con.close()
    changed = (old_prompt != txt) or (old_model != expect_model)
    print(f"  [{'已同步' if changed else '无变化'}] {tid} ({meta['name']}) model->{expect_model}")
    return changed

def main():
    args = sys.argv[1:]
    reg = json.load(open(REG, encoding="utf-8"))
    if "--all" in args:
        print("同步全部 REGISTRY 任务到 DB ...")
        for tid, meta in reg["tasks"].items():
            sync_one(tid, meta)
    elif args:
        for tid in args:
            if tid in reg["tasks"]:
                sync_one(tid, reg["tasks"][tid])
            else:
                print(f"  [未知] {tid} 不在 REGISTRY")
    else:
        print("用法: sync_to_db.py <task_id> | --all")
        sys.exit(2)
    print("完成。建议随后运行 check_drift.py 确认一致。")

if __name__ == "__main__":
    main()
