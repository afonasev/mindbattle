import hashlib
import json
from pathlib import Path

native_id = "01a15ea2-3302-7a52-9b1c-526dadc9599b"
journal = Path(f"/Users/eaafonasev/.codex/sessions/2026/10/21/rollout-2026-10-21T18-24-10-{native_id}.jsonl")
output_path = Path(__file__).with_name("native-web-attempts.json")
records = [json.loads(line) for line in journal.open()]
assert sum(1 for row in records if row.get("type") == "session_meta" and row.get("payload", {}).get("id") == native_id) == 1
calls = {}
outputs = {}
for row in records:
    payload = row.get("payload", {})
    if row.get("type") != "response_item":
        continue
    if payload.get("type") in {"custom_tool_call", "function_call"}:
        code = payload.get("input", payload.get("arguments", ""))
        if isinstance(code, str) and "tools.web__run(" in code:
            calls[payload.get("call_id")] = row
    elif payload.get("type") in {"custom_tool_call_output", "function_call_output"}:
        outputs[payload.get("call_id")] = row

def label(call):
    code = call["payload"].get("input", "")
    if "search_query" in code:
        return "discovery_search"
    if "turn0search3" in code:
        return "primary_document_open_failed_timeout"
    if "turn0search1" in code:
        return "official_alternative_open_metadata_only"
    return "unclassified"

ordered = []
for call_id, call in calls.items():
    if call_id not in outputs:
        continue
    ordered.append({"label": label(call), "callId": call_id, "requestRecord": call, "resultRecord": outputs[call_id]})
assert len(ordered) == 3, f"Expected exactly three web calls, found {len(ordered)}"
payload = {
    "sourceNativeId": native_id,
    "nativeJournal": str(journal),
    "preservationMethod": "Exact native response_item request/result records copied without rewriting; only these three tools.web__run wrappers.",
    "networkCallCount": len(ordered),
    "calls": ordered,
}
output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"path": str(output_path.resolve()), "sha256": hashlib.sha256(output_path.read_bytes()).hexdigest(), "calls": [{"label": row["label"], "callId": row["callId"], "requestOrdinal": row["requestRecord"]["ordinal"], "resultOrdinal": row["resultRecord"]["ordinal"]} for row in ordered]}))
