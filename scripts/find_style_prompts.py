import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

with open(r"C:\Users\navee\OneDrive\Desktop\studio\prompt_library_index.json", "r", encoding="utf-8") as f:
    lib = json.load(f)

remotion_prompts = [p for p in lib if "remotion" in p.get("tags", []) or "remotion" in p.get("prompt", "").lower()]
print(f"Total Remotion prompts: {len(remotion_prompts)}")
for p in remotion_prompts[:30]:
    tags_str = ", ".join(p.get("tags", []))
    prompt_snippet = p.get("prompt", "")[:120].replace("\n", " ")
    print(f"ID {p['id']} | Tags: [{tags_str}] | Excerpt: {prompt_snippet}...")
