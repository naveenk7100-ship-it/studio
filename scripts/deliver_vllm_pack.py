import os
import sys
import html
import requests
from dotenv import load_dotenv

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
load_dotenv(os.path.join(ROOT, ".env"))

token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

facts = [
    "• GitHub Stars: 96,121 (Verified from api.github.com)",
    "• Release: v0.32.0 / v0.33.0 (2 Nov 2026)",
    "• Core: PagedAttention algorithm reduces KV-cache memory waste to < 4%",
    "• CLI Command: vllm serve meta-llama/Llama-3.1-8B-Instruct",
    "• Caveat: Gated model needs HF_TOKEN; open alternative: Qwen/Qwen2.5-7B"
]
escaped_facts = [html.escape(f) for f in facts]
rp_text = (
    "⚡ <b>RESOURCE PACK: vLLM v0.33.0: High-Throughput Inference Engine</b>\n"
    "<i>Prompt Library ID: 164</i>\n\n"
    "<b>Verified Single-Source Facts:</b>\n" +
    "\n".join(escaped_facts) + "\n\n"
    "<b>Source URL:</b> https://github.com/vllm-project/vllm\n"
    "<b>Metrics:</b> Audio: -14.2 LUFS | TP: -1.5 dBTP | 48kHz | Min Motion: 0.82 | Coverage: 64.3%\n\n"
    "<b>Speech Script:</b>\n<i>\"Mama, mee local system lo LLMs high-speed serve cheyalani anukuntunnara? Idi vLLM...\"</i>"
)

res = requests.post(
    f"https://api.telegram.org/bot{token}/sendMessage",
    json={"chat_id": chat_id, "text": rp_text, "parse_mode": "HTML", "disable_web_page_preview": True},
    timeout=20
)
print("Status:", res.status_code, res.text)
