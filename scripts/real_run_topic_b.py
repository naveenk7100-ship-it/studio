"""
Real Run Execution: Topic B (GPT-2 Small Next Word Prediction)
Runs open GPT-2 small model locally, extracts real tokens, token IDs,
real attention weights, and top-5 next token probabilities.
Labels everything strictly as: 'GPT-2 (open model), example run'.
"""
import os
import sys
import json
import torch
import tiktoken
from transformers import GPT2LMHeadModel, GPT2Tokenizer

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
OUT_DIR = os.path.join(ROOT, "runs")
ASSETS_DIR = os.path.join(ROOT, "engine", "public", "real_assets")
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

# 1. Define Real Prompt
prompt = "The future of artificial intelligence is"
print(f"Loading GPT-2 (small) for real inference run...")
print(f"Prompt: \"{prompt}\"")

# 2. Tokenize with official tiktoken and transformers GPT-2 tokenizer
enc = tiktoken.get_encoding("gpt2")
token_ids = enc.encode(prompt)
token_strings = [enc.decode([tid]) for tid in token_ids]
print(f"Tokens ({len(token_ids)}): {token_strings}")
print(f"Token IDs: {token_ids}")

# 3. Load GPT-2 Model with output_attentions=True
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2", output_attentions=True)
model.eval()

# 4. Run Forward Pass
input_ids = torch.tensor([token_ids])
with torch.no_grad():
    outputs = model(input_ids)
    logits = outputs.logits # shape: (1, seq_len, vocab_size)
    attentions = outputs.attentions # 12 layers, each (1, num_heads=12, seq_len, seq_len)

# 5. Extract Next Token Probabilities via Softmax
next_token_logits = logits[0, -1, :]
probs = torch.softmax(next_token_logits, dim=-1)

# Top 5 next token predictions
top5_probs, top5_ids = torch.topk(probs, 5)
top5_results = []
for p, tid in zip(top5_probs.tolist(), top5_ids.tolist()):
    t_str = enc.decode([tid])
    top5_results.append({
        "token_id": tid,
        "token_text": t_str,
        "prob_raw": round(p, 5),
        "prob_pct": round(p * 100.0, 2)
    })

print("\nTop 5 Next-Word Predictions (Real GPT-2 Softmax Output):")
for r in top5_results:
    print(f"  ID {r['token_id']:5d} | '{r['token_text']}': {r['prob_pct']}%")

# 6. Extract Attention Weights from Layer 11, Head 0
layer_idx = 11
head_idx = 0
attn_layer11_head0 = attentions[layer_idx][0, head_idx].tolist()
# attn_layer11_head0 is a [seq_len, seq_len] matrix
print(f"\nExtracted Attention Matrix (Layer {layer_idx}, Head {head_idx}) shape: {len(attn_layer11_head0)}x{len(attn_layer11_head0[0])}")

# 7. Compile Results
results = {
    "topic": "Topic B: GPT-2 Small Next Word Prediction",
    "model_label": "GPT-2 (open model), example run",
    "model_name": "gpt2 (124M parameters, 12 layers, 12 attention heads, 768 hidden dimension)",
    "prompt": prompt,
    "tokens": [
        {"idx": i, "token": token_strings[i], "id": token_ids[i]}
        for i in range(len(token_ids))
    ],
    "top5_predictions": top5_results,
    "attention_sample": {
        "layer": layer_idx,
        "head": head_idx,
        "tokens": token_strings,
        "weights": [[round(w, 4) for w in row] for row in attn_layer11_head0]
    },
    "temperature_applied": 1.0,
    "top_p_applied": 1.0,
    "claims_boundary": "Demonstrates open GPT-2 small architecture only. Zero claims about proprietary frontier models."
}

out_data_path = os.path.join(OUT_DIR, "real_run_topic_b_data.json")
with open(out_data_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

# Also copy to engine assets
engine_asset_path = os.path.join(ROOT, "engine", "src", "assets", "real_gpt2_data.json")
with open(engine_asset_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(f"\nTopic B Real Run Completed. Saved to {out_data_path} and {engine_asset_path}")
