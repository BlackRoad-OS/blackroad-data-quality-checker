#!/usr/bin/env python3
"""BlackRoad Data Quality — validate and score data assets."""
import json, re

def check_world_artifact(artifact: dict) -> dict:
    issues = []; score = 100
    required = ["id","title","type","node","timestamp"]
    for field in required:
        if field not in artifact:
            issues.append(f"Missing required field: {field}"); score -= 15
    if "type" in artifact and artifact["type"] not in ["world","lore","code"]:
        issues.append(f"Invalid type: {artifact[\"type\"]}"); score -= 10
    if "timestamp" in artifact:
        if not re.match(r"\d{4}-\d{2}-\d{2}", artifact["timestamp"]):
            issues.append("Invalid timestamp format"); score -= 5
    if "title" in artifact and len(artifact["title"]) < 3:
        issues.append("Title too short"); score -= 5
    return {"score": max(0,score), "issues": issues, "valid": len(issues) == 0}

def check_batch(artifacts: list) -> dict:
    results = [check_world_artifact(a) for a in artifacts]
    passing = sum(1 for r in results if r["valid"])
    avg_score = sum(r["score"] for r in results) / len(results) if results else 0
    all_issues = [i for r in results for i in r["issues"]]
    return {"total": len(artifacts), "passing": passing, "avg_score": round(avg_score,1), "common_issues": list(set(all_issues))[:5]}

if __name__ == "__main__":
    samples = [
        {"id":"w1","title":"Cyberpunk City","type":"world","node":"aria64","timestamp":"2026-02-23T12:00:00Z"},
        {"id":"w2","type":"invalid","node":"alice"},  # bad
        {"title":"ok","type":"lore","node":"alice","timestamp":"2026-02-23"},  # missing id
    ]
    report = check_batch(samples)
    print(json.dumps(report, indent=2))

