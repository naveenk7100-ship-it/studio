import json

for vid in ["today_1_anatomy", "today_2_browseruse"]:
    path = f"C:/Users/navee/OneDrive/Desktop/studio/cache/words_final_{vid}.json"
    with open(path, "r", encoding="utf-8") as f:
        words = json.load(f)
    print(f"=== SENTENCE BOUNDARIES FOR {vid} ===")
    cur_sentence = []
    for w in words:
        cur_sentence.append(w["word"])
        if w["word"].endswith("?") or w["word"].endswith("."):
            print(f"  [{w['end']:.2f}s | frame {int(w['end']*30)}] {' '.join(cur_sentence)}")
            cur_sentence = []
    if cur_sentence:
        print(f"  [End: {words[-1]['end']:.2f}s] {' '.join(cur_sentence)}")
