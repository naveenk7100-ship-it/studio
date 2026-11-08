import tiktoken
import time
import os
import pypdf
import pypdfium2

# 1. Real Token Computation for Video 1
enc = tiktoken.get_encoding("cl100k_base")
prompt_text = "How does ChatGPT actually think?"
token_ids = enc.encode(prompt_text)
tokens = [enc.decode([tid]) for tid in token_ids]
print("--- VIDEO 1: TOKENIZATION PROOF ---")
print("Prompt:", prompt_text)
print("Tokens:", tokens)
print("Token IDs:", token_ids)

# 2. Real Benchmark Run for Video 2
# Test on a real PDF in the workspace: prompt_library_index.pdf
pdf_path = r"C:\Users\navee\OneDrive\Desktop\prompt_library_index.pdf"
if not os.path.exists(pdf_path):
    print("PDF not found at:", pdf_path)
else:
    print("\n--- VIDEO 2: REAL RUN BENCHMARK ---")
    print("Testing PDF:", pdf_path, "Size:", os.path.getsize(pdf_path), "bytes")
    
    # Run pypdf on first 5 pages
    t0 = time.perf_counter()
    reader = pypdf.PdfReader(pdf_path)
    pypdf_text = ""
    for page in reader.pages[:5]:
        pypdf_text += page.extract_text() or ""
    t_pypdf = (time.perf_counter() - t0) * 1000
    print(f"pypdf (5 pages): {t_pypdf:.2f} ms | Words extracted: {len(pypdf_text.split())}")
    
    # Run pypdfium2 on first 5 pages
    t0 = time.perf_counter()
    doc = pypdfium2.PdfDocument(pdf_path)
    pdfium_text = ""
    for i in range(min(5, len(doc))):
        page = doc.get_page(i)
        tp = page.get_textpage()
        pdfium_text += tp.get_text_range() or ""
        tp.close()
        page.close()
    doc.close()
    t_pdfium = (time.perf_counter() - t0) * 1000
    print(f"pypdfium2 (5 pages): {t_pdfium:.2f} ms | Words extracted: {len(pdfium_text.split())}")
    speedup = t_pypdf / t_pdfium if t_pdfium > 0 else 1.0
    print(f"Speedup: {speedup:.1f}x faster with pypdfium2 (C++ PDFium engine)")
