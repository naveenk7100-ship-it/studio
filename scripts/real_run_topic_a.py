"""
Real Run Execution: Topic A (pypdfium2 on arXiv 1706.03762)
Generates empirical data, page renders, block bounding boxes, timing benchmarks, and token counts.
"""
import os
import sys
import time
import json
import statistics
import pypdfium2 as pdfium
import pypdf
from pdfminer.high_level import extract_text as pdfminer_extract
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
PDF_PATH = os.path.join(ROOT, "cache", "arxiv_1706_03762.pdf")
ASSETS_DIR = os.path.join(ROOT, "engine", "public", "real_assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# 1. Inspect Document
doc = pdfium.PdfDocument(PDF_PATH)
page_count = len(doc)
print(f"Loaded arXiv 1706.03762: {page_count} pages, {os.path.getsize(PDF_PATH)} bytes")

# 2. Render Real Page 1 Image
page0 = doc[0]
width_pt, height_pt = page0.get_size()
render_scale = 2.0
bitmap = page0.render(scale=render_scale)
pil_img = bitmap.to_pil()
rendered_page_path = os.path.join(ASSETS_DIR, "arxiv_1706_03762_p1.png")
pil_img.save(rendered_page_path)
print(f"Rendered Page 1 to {rendered_page_path} ({pil_img.size[0]}x{pil_img.size[1]} px)")

# 3. Extract Real Text Blocks & Character Coordinates
textpage = page0.get_textpage()
full_p1_text = textpage.get_text_range()
num_chars = textpage.count_chars()
print(f"Page 1 Character count: {num_chars}")

# Extract line boxes
n_rects = textpage.count_rects()
block_boxes = []
for i in range(n_rects):
    r = textpage.get_rect(i)
    l, b, r_pt, t = r
    # Convert to image coordinates (scale=2.0, top-down)
    px_l = l * render_scale
    px_r = r_pt * render_scale
    px_t = (height_pt - t) * render_scale
    px_b = (height_pt - b) * render_scale
    bounded_text = textpage.get_text_bounded(l, b, r_pt, t).strip()
    block_boxes.append({
        "block_idx": i,
        "text": bounded_text,
        "pdf_coords": [round(l, 1), round(b, 1), round(r_pt, 1), round(t, 1)],
        "px_box": [round(px_l, 1), round(px_t, 1), round(px_r, 1), round(px_b, 1)]
    })

print(f"Extracted {len(block_boxes)} text rectangles on Page 1")

# 4. Check Two-Column Reading Order Limitation
# On page 1 of Attention Is All You Need, the introduction has two columns.
# Let's inspect the stream to see the extraction sequence across columns.
lines = full_p1_text.splitlines()
non_empty_lines = [line.strip() for line in lines if line.strip()]
print(f"Total non-empty lines on Page 1: {len(non_empty_lines)}")

# 5. Measure Empirical Timings on 15 Pages (5 Repeated Runs)
N_RUNS = 5
print(f"\nRunning {N_RUNS} repeated benchmark runs across all {page_count} pages...")

# pypdfium2
times_pdfium = []
for r in range(N_RUNS):
    t0 = time.perf_counter()
    d = pdfium.PdfDocument(PDF_PATH)
    txt_all = "".join([p.get_textpage().get_text_range() for p in d])
    t1 = time.perf_counter()
    times_pdfium.append((t1 - t0) * 1000.0)

# pypdf
times_pypdf = []
for r in range(N_RUNS):
    t0 = time.perf_counter()
    reader = pypdf.PdfReader(PDF_PATH)
    txt_all_pypdf = "".join([p.extract_text() or "" for p in reader.pages])
    t1 = time.perf_counter()
    times_pypdf.append((t1 - t0) * 1000.0)

# pdfminer.six
times_pdfminer = []
for r in range(N_RUNS):
    t0 = time.perf_counter()
    txt_all_miner = pdfminer_extract(PDF_PATH)
    t1 = time.perf_counter()
    times_pdfminer.append((t1 - t0) * 1000.0)

mean_pdfium = round(statistics.mean(times_pdfium), 2)
stdev_pdfium = round(statistics.stdev(times_pdfium), 2)
mean_pypdf = round(statistics.mean(times_pypdf), 2)
stdev_pypdf = round(statistics.stdev(times_pypdf), 2)
mean_pdfminer = round(statistics.mean(times_pdfminer), 2)
stdev_pdfminer = round(statistics.stdev(times_pdfminer), 2)

speedup_vs_pypdf = round(mean_pypdf / mean_pdfium, 2)
speedup_vs_miner = round(mean_pdfminer / mean_pdfium, 2)

print(f"pypdfium2:   {mean_pdfium} +/- {stdev_pdfium} ms")
print(f"pypdf:       {mean_pypdf} +/- {stdev_pypdf} ms ({speedup_vs_pypdf}x slower)")
print(f"pdfminer:    {mean_pdfminer} +/- {stdev_pdfminer} ms ({speedup_vs_miner}x slower)")

# 6. Real Tokenizer Count with tiktoken (if available)
token_counts = {}
try:
    import tiktoken
    enc_cl100k = tiktoken.get_encoding("cl100k_base")
    enc_gpt2 = tiktoken.get_encoding("gpt2")
    
    tokens_p1_cl100k = len(enc_cl100k.encode(full_p1_text))
    tokens_all_cl100k = len(enc_cl100k.encode(txt_all))
    tokens_p1_gpt2 = len(enc_gpt2.encode(full_p1_text))
    tokens_all_gpt2 = len(enc_gpt2.encode(txt_all))
    
    token_counts = {
        "p1_cl100k_tokens": tokens_p1_cl100k,
        "doc_15p_cl100k_tokens": tokens_all_cl100k,
        "p1_gpt2_tokens": tokens_p1_gpt2,
        "doc_15p_gpt2_tokens": tokens_all_gpt2,
        "raw_characters_doc": len(txt_all),
        "raw_words_doc": len(txt_all.split())
    }
    print(f"Real Token Counts: Doc Total = {tokens_all_cl100k} cl100k tokens ({len(txt_all.split())} words)")
except ImportError:
    print("tiktoken not installed yet, token counting deferred")

# 7. Compile and save results
results = {
    "topic": "Topic A: pypdfium2 Real Run",
    "pdf_source": {
        "title": "Attention Is All You Need",
        "arxiv_id": "1706.03762",
        "url": "https://arxiv.org/abs/1706.03762",
        "page_count": page_count,
        "file_size_bytes": os.path.getsize(PDF_PATH)
    },
    "page1_render": {
        "path": "engine/public/real_assets/arxiv_1706_03762_p1.png",
        "width_px": pil_img.size[0],
        "height_px": pil_img.size[1],
        "render_scale": render_scale,
        "num_chars": num_chars,
        "num_rect_blocks": len(block_boxes)
    },
    "block_boxes_sample": block_boxes[:30],
    "first_10_lines": non_empty_lines[:10],
    "benchmarks": {
        "runs_count": N_RUNS,
        "environment": "Windows x64 / Python 3.11",
        "libraries": {
            "pypdfium2": {"mean_ms": mean_pdfium, "stdev_ms": stdev_pdfium, "all_ms": times_pdfium},
            "pypdf": {"mean_ms": mean_pypdf, "stdev_ms": stdev_pypdf, "all_ms": times_pypdf, "ratio": speedup_vs_pypdf},
            "pdfminer.six": {"mean_ms": mean_pdfminer, "stdev_ms": stdev_pdfminer, "all_ms": times_pdfminer, "ratio": speedup_vs_miner}
        }
    },
    "token_metrics": token_counts,
    "limitations_observed": {
        "two_column_behavior": "pypdfium2 streams text in the raw internal content stream order. If a PDF layout puts column 1 line 1, then column 2 line 1 in the stream, textpage.get_text_range() will return them in that stream order without visual re-ordering. It is a parser and renderer, not an OCR or layout re-flow engine."
    }
}

out_data_path = os.path.join(ROOT, "runs", "real_run_topic_a_data.json")
with open(out_data_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(f"\nTopic A Real Run Completed. Saved to {out_data_path}")
