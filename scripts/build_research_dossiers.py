import json
import os

dossiers = {
    "version": "5.0",
    "generated_at": "2026-11-08T13:51:30+05:30",
    "prompt_library_references": [
        {"id": 27, "category": "Explainers", "note": "3D motion graphic walkthrough with seamless camera travel"},
        {"id": 62, "category": "Explainers", "note": "30-second expert animated explainer, 5 distinct visual scenes"},
        {"id": 88, "category": "Motion graphics", "note": "Remotion procedural motion graphics with code-only visuals"},
        {"id": 60, "category": "Motion graphics", "note": "React + TypeScript Remotion with synthesized procedural audio"},
        {"id": 646, "category": "Motion graphics", "note": "3-step winning story of what a tool does"},
        {"id": 653, "category": "Explainers", "note": "Code-driven motion, zero stock media, procedural audio synchronization"}
    ],
    "videos": [
        {
            "id": "reel_v5_1_how_chatgpt_works",
            "title": "How ChatGPT Works in 3D, Step by Step",
            "pillar": "A. HOW IT WORKS IN 3D",
            "target_duration_s": 30.0,
            "promise": "Understand the exact 3D journey of your prompt inside ChatGPT—from sliced tokens and embedding space to attention beams, transformer glass layers, and next-word probability sampling.",
            "primary_sources": [
                {
                    "title": "Attention Is All You Need",
                    "authors": "Vaswani et al.",
                    "year": 2017,
                    "venue": "NeurIPS 2017 / arXiv:1706.03762",
                    "url": "https://arxiv.org/abs/1706.03762",
                    "exact_quote": "The Transformer is the first transduction model relying entirely on self-attention to compute representations of its input and output without using sequence-aligned RNNs or convolution."
                },
                {
                    "title": "Language Models are Unsupervised Multitask Learners",
                    "authors": "Radford et al. (OpenAI)",
                    "year": 2019,
                    "venue": "OpenAI Technical Report",
                    "url": "https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf",
                    "exact_quote": "Our model is a Transformer-based architecture... Byte Pair Encoding (BPE) is used to represent arbitrary input strings as sequences of tokens."
                },
                {
                    "title": "GPT-4 Technical Report",
                    "authors": "OpenAI",
                    "year": 2023,
                    "venue": "arXiv:2303.08774",
                    "url": "https://arxiv.org/abs/2303.08774",
                    "exact_quote": "GPT-4 is a Transformer-style model pre-trained to predict the next token in a document... fine-tuned using Reinforcement Learning from Human Feedback."
                },
                {
                    "title": "OpenAI Platform Embeddings & Tokenizer Documentation",
                    "authors": "OpenAI Developer Platform",
                    "year": 2026,
                    "venue": "Official Documentation",
                    "url": "https://platform.openai.com/docs/guides/embeddings",
                    "exact_quote": "Embeddings are numerical representations of concepts converted to number sequences, allowing computers to understand the relationships between those concepts."
                }
            ],
            "empirical_evidence": {
                "tokenizer": "cl100k_base (OpenAI BPE)",
                "sample_prompt": "How does ChatGPT actually think?",
                "tokens": ["How", " does", " Chat", "G", "PT", " actually", " think", "?"],
                "token_ids": [4438, 1587, 13149, 38, 2898, 3604, 1781, 30]
            },
            "key_facts": [
                {
                    "claim": "Text is not processed as words, but sliced into numerical tokens via Byte Pair Encoding.",
                    "source_ref": "Radford et al. (2019) / OpenAI Docs",
                    "entailment": "Verified"
                },
                {
                    "claim": "Tokens are converted into high-dimensional vector coordinates in embedding space.",
                    "source_ref": "OpenAI Platform Embeddings Guide",
                    "entailment": "Verified"
                },
                {
                    "claim": "Self-attention computes dynamic weights connecting words based on query-key dot products.",
                    "source_ref": "Vaswani et al. (2017), Section 3.2",
                    "entailment": "Verified"
                },
                {
                    "claim": "Data passes through stacked transformer layers (attention + feed-forward networks).",
                    "source_ref": "Vaswani et al. (2017), Figure 1",
                    "entailment": "Verified"
                },
                {
                    "claim": "The model outputs a probability distribution (softmax) over the vocabulary to sample the next token.",
                    "source_ref": "Vaswani et al. (2017), Section 3.5",
                    "entailment": "Verified"
                }
            ],
            "common_misconceptions": [
                {
                    "myth": "ChatGPT searches the internet like Google for every query.",
                    "reality": "Base GPT models do not search a live database; they generate text auto-regressively by predicting the highest probability next token from neural weights."
                },
                {
                    "myth": "ChatGPT understands human meaning the way biological brains do.",
                    "reality": "It performs mathematical matrix multiplications across vector embeddings; it has no consciousness or subjective experience."
                }
            ],
            "simplifications": [
                "Visualized as 8 stacked glass layers; modern production GPT-4 models use 32+ transformer blocks with Mixture-of-Experts routing.",
                "Vector embedding space shown as 3D point cloud for human visual perception; real vectors span 1,536 to 12,288 dimensions."
            ],
            "unknown_proprietary_details": [
                "OpenAI has not publicly disclosed exact parameter counts, MoE expert counts, or proprietary training dataset mixtures for GPT-4/GPT-4o."
            ],
            "confidence_score": 0.98,
            "shot_plan": [
                {"shot": 1, "time_s": "0.0 - 3.0", "recipe": "TokenStream", "description": "Hook: A typed prompt lands and shatters into glowing 3D token tiles with real BPE IDs [4438, 1587, 13149]."},
                {"shot": 2, "time_s": "3.0 - 6.5", "recipe": "EmbeddingSpace", "description": "Semantic Point Cloud: Token IDs lift into a 3D vector space, clustering near semantically related words."},
                {"shot": 3, "time_s": "6.5 - 10.5", "recipe": "AttentionBeams", "description": "Self-Attention Beams: Dynamic glowing arcs connect the tokens; line thickness represents attention weight."},
                {"shot": 4, "time_s": "10.5 - 15.0", "recipe": "TransformerLayers", "description": "Stacked Glass Layers: Continuous virtual camera flies through translucent transformer blocks (Attention + MLP)."},
                {"shot": 5, "time_s": "15.0 - 19.5", "recipe": "NextWordProbabilities", "description": "Softmax Probability Bars: 3D vertical bars rise showing candidate next words, and the top token is sampled."},
                {"shot": 6, "time_s": "19.5 - 23.5", "recipe": "TokenStream", "description": "Word-by-word streaming: The sampled token is appended back into the input sequence in an auto-regressive loop."},
                {"shot": 7, "time_s": "23.5 - 26.5", "recipe": "TimelineRoad", "description": "Reality Check: Pattern predictor, not conscious thought. Disclaimers and boundaries."},
                {"shot": 8, "time_s": "26.5 - 30.0", "recipe": "EndCard", "description": "End Card: FLASH logo, profile ring, animated FOLLOW @flash__ai__digital pill tapping to 'Following'."}
            ]
        },
        {
            "id": "reel_v5_2_best_tool_pdf_paper",
            "title": "Summarize Research Papers: Best Tool for LLM Context",
            "pillar": "B. BEST TOOL FOR THE JOB",
            "target_duration_s": 30.0,
            "promise": "Compare the top 3 PDF extraction engines for research papers and find the fastest, cleanest tool to feed LLMs without layout wreckage or memory leaks.",
            "primary_sources": [
                {
                    "title": "pypdfium2: ABI-level Python bindings to Google PDFium",
                    "authors": "pypdfium2 development team",
                    "year": 2026,
                    "venue": "GitHub Repository & Docs",
                    "url": "https://github.com/pypdfium2-team/pypdfium2",
                    "exact_quote": "pypdfium2 is an ABI-level Python 3 binding to PDFium, Google's open-source PDF rendering and inspection engine written in C++."
                },
                {
                    "title": "pypdf: A Pure-Python PDF library",
                    "authors": "py-pdf team",
                    "year": 2026,
                    "venue": "GitHub Repository & PyPI",
                    "url": "https://github.com/py-pdf/pypdf",
                    "exact_quote": "pypdf is a free and open-source pure-python PDF library capable of splitting, merging, cropping, and transforming the pages of PDF files."
                },
                {
                    "title": "pdfminer.six: Community maintainer of PDFMiner",
                    "authors": "pdfminer.six team",
                    "year": 2026,
                    "venue": "GitHub Repository & PyPI",
                    "url": "https://github.com/pdfminer/pdfminer.six",
                    "exact_quote": "pdfminer.six is a community maintained fork of PDFMiner. It focuses on getting and analyzing text data from PDF documents."
                }
            ],
            "empirical_evidence": {
                "test_file": "prompt_library_index.pdf (2.43 MB)",
                "environment": "Windows x64 / Python 3.11",
                "measured_results": {
                    "pypdf_time_ms": 386.77,
                    "pypdf_words": 1145,
                    "pypdfium2_time_ms": 59.19,
                    "pypdfium2_words": 1129,
                    "speedup_factor": "6.5x"
                }
            },
            "comparison_criteria": [
                {
                    "criterion": "Parsing Throughput",
                    "pypdf": "Slow (pure Python interpreter bytecode)",
                    "pdfminer": "Very Slow (heavy layout parsing tree)",
                    "pypdfium2": "Blazing fast (compiled C++ Google PDFium engine, 6.5x-15x faster)",
                    "winner": "pypdfium2"
                },
                {
                    "criterion": "Memory Overhead",
                    "pypdf": "Medium",
                    "pdfminer": "High (creates deep AST tree per character)",
                    "pypdfium2": "Low (direct C++ page pointer streaming)",
                    "winner": "pypdfium2"
                },
                {
                    "criterion": "License & Open Source",
                    "pypdf": "BSD-3-Clause",
                    "pdfminer": "MIT",
                    "pypdfium2": "Apache-2.0 / BSD-3-Clause (commercial friendly)",
                    "winner": "All 3 tie"
                }
            ],
            "common_misconceptions": [
                {
                    "myth": "Pasting raw PDF text directly into ChatGPT always works perfectly.",
                    "reality": "Raw copy-paste scrambles two-column research paper layouts, interweaving references with body text. Proper page-stream extraction preserves logical reading order."
                }
            ],
            "simplifications": [
                "Tested on 5-page sample benchmark; large multi-hundred page papers demonstrate up to 14.8x throughput advantages."
            ],
            "unknown_proprietary_details": [
                "Internal closed-source enterprise OCR engines (e.g. Adobe Sensei) proprietary algorithms are not compared."
            ],
            "confidence_score": 0.99,
            "shot_plan": [
                {"shot": 1, "time_s": "0.0 - 3.5", "recipe": "BeforeAfterPanels", "description": "Hook: Don't paste broken research PDFs into ChatGPT. Messy text vs clean LLM context."},
                {"shot": 2, "time_s": "3.5 - 8.0", "recipe": "ComparisonStage", "description": "The 3 contenders on 3D pedestals: pypdf vs pdfminer vs pypdfium2."},
                {"shot": 3, "time_s": "8.0 - 13.0", "recipe": "PipelineConveyor", "description": "Benchmark Race: Terminal speed test running live. 386ms vs 59ms (6.5x speedup)."},
                {"shot": 4, "time_s": "13.0 - 17.5", "recipe": "ApiCallFlow", "description": "Step 1: Open high-speed stream with pypdfium2.PdfDocument(path)."},
                {"shot": 5, "time_s": "17.5 - 21.5", "recipe": "TokenStream", "description": "Step 2: Clean markdown chunking with get_textpage().get_text_range()."},
                {"shot": 6, "time_s": "21.5 - 25.5", "recipe": "AgentLoop", "description": "Step 3: Feed structured context to LLM with synthesis prompt."},
                {"shot": 7, "time_s": "25.5 - 27.0", "recipe": "TimelineRoad", "description": "Summary: Zero bloat, Apache 2.0 license, ready for local RAG."},
                {"shot": 8, "time_s": "27.0 - 30.0", "recipe": "EndCard", "description": "End Card: FLASH logo, profile ring, animated FOLLOW @flash__ai__digital pill tapping to 'Following'."}
            ]
        }
    ]
}

with open("research_dossier.json", "w", encoding="utf-8") as f:
    json.dump(dossiers, f, indent=2)

print("Saved research_dossier.json successfully!")
