# -*- coding: utf-8 -*-
"""
check_drift.py — 自动化版本漂移检测
比对三层是否一致：DB(model/status/prompt) vs REGISTRY.json vs automations/<id>/prompt.md
任何不一致即报红。
"""
import sqlite3, os, json, hashlib, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = "/Users/jungle1499/.workbuddy/workbuddy.db"
REG = os.path.join(ROOT, "REGISTRY.json")

def sha256(s):
    return hashlib.sha256((s or "").encode("utf-8")).hexdigest()

def main():
    reg = json.load(open(REG, encoding="utf-8"))
    con = sqlite3.connect(DB); cur = con.cursor()
    cur.execute("""SELECT id,model_id,status,prompt FROM automations
                   WHERE status='ACTIVE' AND deleted_at IS NULL""")
    db = {r[0]: {"model": r[1], "status": r[2], "prompt": r[3]} for r in cur.fetchall()}
    con.close()

    issues = []
    reg_tasks = reg["tasks"]

    # 1) REGISTRY 中每个任务 vs DB
    for tid, meta in reg_tasks.items():
        if tid not in db:
            issues.append(f"[缺失] REGISTRY 有但 DB 无 ACTIVE: {tid} ({meta['name']})")
            continue
        d = db[tid]
        expect_model = meta.get("model", "hy3")
        if d["model"] != expect_model:
            issues.append(f"[模型] {tid} ({meta['name']}) model={d['model']} != 期望 {expect_model}")
        if d["status"] != "ACTIVE":
            issues.append(f"[状态] {tid} ({meta['name']}) status={d['status']} != ACTIVE")
        # prompt 文件 vs DB
        pf = os.path.join(ROOT, meta["prompt_file"])
        if not os.path.exists(pf):
            issues.append(f"[文件] {tid} prompt.md 不存在: {pf}")
        else:
            txt = open(pf, encoding="utf-8").read()
            if sha256(txt) != meta.get("prompt_sha256"):
                # 文件与 REGISTRY 记录不一致（可能文件被改未 commit）
                issues.append(f"[文件hash] {tid} ({meta['name']}) prompt.md 与 REGISTRY 记录 sha 不一致（文件已改未登记）")
            if sha256(txt) != sha256(d["prompt"]):
                issues.append(f"[DB同步] {tid} ({meta['name']}) prompt.md 与 DB prompt 不一致（需 sync_to_db）")
        # 模板版本钉死声明
        pf2 = os.path.join(ROOT, meta["prompt_file"])
        if os.path.exists(pf2):
            t = open(pf2, encoding="utf-8").read()
            if "模板版本钉死" not in t and "pinned-" not in t:
                issues.append(f"[模板钉死] {tid} ({meta['name']}) prompt.md 未含模板版本钉死声明")

    # 2) DB 有但 REGISTRY 未登记的 ACTIVE 任务
    for tid in db:
        if tid not in reg_tasks:
            issues.append(f"[未登记] DB ACTIVE 但 REGISTRY 无: {tid} (model={db[tid]['model']})")

    print("=" * 64)
    print(f"漂移检测报告  |  REGISTRY 任务数={len(reg_tasks)}  DB ACTIVE 数={len(db)}")
    print("=" * 64)
    if not issues:
        print("✅ 全部一致，无漂移。")
        return 0
    print(f"❌ 发现 {len(issues)} 处不一致：\n")
    for i in issues:
        print("  - " + i)
    return 1

if __name__ == "__main__":
    sys.exit(main())
