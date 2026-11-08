import json

with open("prompt_library_index.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("--- EXPLAINERS & MOTION GRAPHICS WITH TECH / 3D / REMOTION ---")
for p in data:
    cat = p.get("category", "")
    if cat in ("Explainers", "Motion graphics"):
        txt = (p.get("prompt", "") + " " + p.get("title", "")).lower()
        if any(w in txt for w in ["remotion", "explainer", "3d", "ai", "code", "model", "data", "benchmark", "visual", "workflow"]):
            clean = p.get("prompt", "").replace("\n", " ")[:140].encode("ascii", errors="replace").decode("ascii")
            print(f"ID {p.get('id')} [{cat}]: {clean}")
