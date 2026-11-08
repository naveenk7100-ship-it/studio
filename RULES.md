# FLASH FINAL SPEC V7: THE SINGLE SOURCE OF TRUTH

This document is the absolute single source of truth for FLASH CONTENT OS, replacing every earlier prompt and specification. Read this file, `lessons.json`, and `tests/regression/` at the start of every session. Work in ONE conversation only.

---

## 0. STATE, BOUNDARIES & BUDGET
- **Budget**: Zero budget (no Cloudflare, no paid APIs, no stock media, no AI-generated images).
- **Tools**: GitHub CLI (`gh`) and built-in `GITHUB_TOKEN` only. No personal access token (PAT).
- **Live Posting**: DO NOT post live until user explicitly commands `GO`. Production cron enabled, posting stays gated.
- **Evidence & Verification**: Never claim a number not measured; print raw evidence in reports; end every report with an explicit list of what could NOT be verified.
- **Language**: **Tenglish only** (romanized Telugu plus English) for scripts and captions. Keep a `LANG` configuration setting (`LANG=tenglish`) so other languages can be added later. Native Telugu script is used ONLY inside the Gemini TTS payload when needed for authentic pronunciation; on-screen captions use romanized Tenglish.

---

## A. GOALS (Strict Priority Order)
1. **Voice and Captions Match Perfectly**: Exact 1:1 word mapping, word-by-word highlight, verified by caption readback gate on the final MP4.
2. **Zero Fake or False Information**: Every claim backed by a real proof visual, data point, or execution log. Zero hallucinations.
3. **Logo Timing**: The FLASH logo appears **ONLY in the last 2.0–2.5 seconds** of the video (the end card), NEVER on top, bottom, or anywhere else during the video.
4. **Music Always Low; Explanation Crystal Clear**: Music at least 22 dB below voice during speech; never more than +6 dB in pauses; integrated music loudness in speech windows $\le -36\text{ LUFS}$. Final master $-14.0 \pm 0.5\text{ LUFS}$, true peak $\le -1.5\text{ dBTP}$, 48 kHz.
5. **Premium, Natural-Editor Look**: Next-level procedural 3D visuals and technical blueprints matching the explanation; never flat slides or static cards.
6. **Memorable**: Viewers must remember the core explanation after one watch (hook $\le 2\text{s}$, 1-line promise, 3 beats with visual anchors, spoken recap in last 4s before end card, 1 callback analogy).
7. **Daily Output**: Two videos ready every morning (different topic types, 30–60s each).

---

## B. DAILY PRODUCTION PLAN
- **Schedule**: Two videos READY (rendered, gated, deployed to dashboard) by 08:00 IST daily (hard deadline 09:30 IST), with a 3-day buffer (6 videos) topped up every 6 hours. Retries every 30 minutes; open a GitHub issue *"Today's videos are ready"* assigned to the user.
- **Pair Rule**:
  - **12:30 PM IST Slot = TOOLS**: Best tool for a real job, how to use it in steps, real-life workflow (40–55 seconds).
  - **8:30 PM IST Slot = AI DISCOVERY**: How it works in 3D, working repo, interesting AI fact/myth-busting, or fresh drop (45–60 seconds).
  - The two daily videos must differ in content pillar, domain tags, and visual recipes (similarity gate on tags and topic embeddings).
  - **Weekly Mix**: Tools 7, Discovery 7 (~3 how-it-works, 2 repos, 1 fact, 1 fresh drop).
- **Freshness Limits**:
  - Drops & News: $\le 48\text{ h}$.
  - Releases: $\le 14\text{ days}$.
  - Repos: Created $\le 30\text{ days}$ with proven star velocity.
  - Tools, How-It-Works, and Facts: May be evergreen but must be 100% accurate and checked against current official documentation.
  - `covered.json` ledger blocks repeated topics for 60 days. Skip a slot rather than produce a weak or stale topic.
- **Duration Guidelines**: Fact: 30–40s; Repo: 35–45s; Tool: 40–55s; How-It-Works: 45–60s. Pick by content density, never pad.

---

## C. A+ RESEARCH AND TRUTH GATES
- **Primary Sources**: $\ge 3$ independent primary sources per video (official documentation, peer-reviewed arXiv papers, vendor engineering blogs, repository READMEs, pricing/feature specifications).
- **Research Dossier (`research_dossier.json`)**:
  - One-sentence promise.
  - Facts with exact quotes and absolute source URLs.
  - Common misconceptions and corrections.
  - Simplifications explicitly noted (labeled "simplified").
  - Unknown/proprietary details explicitly declared (labeled "unknown").
  - Confidence rating ($\ge 0.95$).
  - Sentence-by-sentence shot plan.
  - Three comprehension questions for teach-back validation.
  - Entailment pass: Claim verified against quote to eliminate overclaims. Closed products (e.g. ChatGPT, Claude) report only publicly documented architecture; example numbers labeled "example".
- **Proof for Every Claim**:
  - Real captures via Playwright (mobile viewport ~420 px, device scale factor 3, cookie banners hidden).
  - Project figures from README/docs (license permitting).
  - Openly licensed figures (arXiv, Wikimedia Commons, NASA).
  - Real terminal output executed directly in the Actions sandbox.
  - `image_ledger.json`: Source URL, license, author, capture timestamp, perceptual hash, and usage location. Attribution in description, first comment, and a subtle "source" tag on the proof image (never a persistent intrusive chip).
- **Commands & Verbatim Integrity**:
  - Verbatim from current project docs, exact tool version. Never use unsafe flags (e.g. `--dangerously-skip-permissions`).
  - Author and tool names strictly from GitHub API or official site (never guessed).
  - No dates inside video frames. Dates and version numbers belong in caption, description, and first comment.
  - Banned on screen: Relative time words ("yesterday", "recently"), spelled-out numbers (use digits like "386", not "three hundred"), Telugu script (TTS payload only), hype/self-praise, internal debug labels (`VERIFIED`, `READY`, `AUTONOMOUS`, `PILLAR A`). Step numbering (`1`, `2`, `3`) is allowed only for actual tutorial instructions.

---

## D. PRESENTATION, EDITING & 3D ENGINE
- **Narrative Structure**:
  1. **Hook (0–2 s)**: Strongest real visual + question or surprising true fact.
  2. **Promise (1 line)**: Clear value proposition.
  3. **Three Beats**: Each with a distinct visual anchor (3D scene or proof image) and a 1-line takeaway.
  4. **Recap Line**: Spoken in the last 4 seconds before the end card.
  5. **Analogy Callback**: One conceptual analogy returned to before the finish.
  6. **End Card (Last 2.0–2.5 s)**: FLASH logo, profile ring, animated Follow pill, and soft pop foley.
- **Scripting (Plain Tenglish)**:
  - Sentences $\le 12$ words, one idea per sentence, define technical terms on first use, natural direct conversational cadence.
  - Every sentence visually illustrated by what the voice speaks at that exact second.
- **Visual Language**:
  - Motivated camera moves, match cuts, semantic transitions (e.g. zoom into token $\to$ arrive in embedding space).
  - Easing and anticipation, varied shot scale, restrained typography, $\ge 3$ depth layers per shot, subtle grain and light, maximum 1 controlled RGB-split glitch, zero camera shake.
  - 12 procedural 3D recipes (`TokenStream`, `EmbeddingSpace`, `AttentionBeams`, `TransformerLayers`, `NextWordProbabilities`, `BeforeAfterPanels`, `ComparisonStage`, `PipelineConveyor`, `ApiCallFlow`, `AgentLoop`, `RetrievalCloud`, `TimelineRoad`) plus topic-specific variations.
  - Never repeat the same recipe or image twice in a row; no repeated image within a video.
  - Style prompt IDs selected from `prompt_library_index.json` (Explainers & Motion graphics first); logged and never reused within 14 days.

---

## E. BRANDING RULES
- **Zero In-Video Branding**: NO logo, NO logo mark, NO handle pill, NO header/footer brand text during the main body of the video.
- **End Card Only (Last 2.0–2.5 s)**:
  - FLASH circular logo mark with profile ring.
  - `FOLLOW @flash__ai__digital` pill animating to `FOLLOWING` with checkmark.
  - Subtitle: *"Daily AI and dev updates, with sources"*.
  - Soft UI pop audio effect.
- **Verification**: Template matching and OCR scan across all sampled frames must confirm zero logo presence prior to the end card window.

---

## F. VOICE, CAPTIONS & MUSIC
- **Voice Stem Calibration**:
  - Gemini TTS (`Sadaltager` default), mixed-script payload for authentic Telugu pronunciation.
  - Pace: 4.6–5.6 syllable-peaks per second.
  - Pauses: 15–22% of speech time.
  - Pitch variation: 4.0–5.5 semitones.
  - Clean phrase endings (end-energy ratio $\le 0.5$), head 150 ms, tail $\ge 300\text{ ms}$.
- **Captions & Alignment**:
  - 1:1 strict word mapping between TTS script and caption text (zero paraphrase, digits instead of words).
  - Word-by-word highlight, 2–4 words visible simultaneously, font size $\ge 56\text{ px}$, fixed lower-third caption zone that never covers proof images or 3D centers.
  - Forced alignment via WhisperX / faster-whisper on the isolated voice stem.
- **Caption Readback Gate on Final MP4**:
  - At the temporal midpoint of every word, OCR the caption region:
    - Highlighted word must match expected word for $\ge 98\%$ of words.
    - No caption unchanged $> 1.2\text{ s}$ while speech continues.
    - Zero caption visible during silence or end card.
    - Word onset error: median $\le 60\text{ ms}$, p95 $\le 120\text{ ms}$.
    - Last caption finishes within 0.4s of the final spoken word.
  - Print per-word alignment table (`word`, `expected_time`, `caption_time`, `error_ms`).
- **Music & Audio Mastering**:
  - Original procedural music, 96–112 BPM, calm bed.
  - **Speech Ducking**: Music at least 22 dB below voice during speech; pause swell limited to $\le +6\text{ dB}$ (never loud); integrated music loudness during speech windows $\le -36\text{ LUFS}$.
  - Soft riser into end card; subtle UI pop.
  - **Final Mix**: $-14.0 \pm 0.5\text{ LUFS}$, true peak $\le -1.5\text{ dBTP}$, sample rate **exactly 48 kHz** (stereo/mono AAC 192k).

---

## G. REAL-FILE QUALITY GATES
Every video must generate `runs/<id>/gates.json` directly from the rendered master and 720p files:
1. **Motion MAD**: Consecutive $108 \times 192$ grayscale frames at 10 fps: median $\ge 3.0$, no second $< 1.5$.
2. **Empty Area (User Metric)**: Gaussian blur $\sigma=3$, pixels within 14 gray levels of median and local gradient $< 2 \le 35\%$ in every sampled second. Reconcile with edge-based method.
3. **Framing & Typography**: $\ge 3$ depth layers, hero element $\ge 60\%$ of frame, headlines $\ge 80\text{ px}$, labels $\ge 40\text{ px}$, captions $\ge 56\text{ px}$, contrast $\ge 4.5:1$.
4. **Banned Words & Dates**: 0 banned words, 0 dates in video frames.
5. **Teach-Back Gate**: 3 comprehension questions generated from the dossier tested against the transcript + OCR via LLM. Must derive answers with 100% entailment.
6. **Regression Suite**: All tests in `tests/regression/` run on real produced files and pass.

---

## H. DASHBOARD, ARCHIVE & SOCIAL WORKFLOW
- **Dashboard (`docs/review/index.html`)**:
  - Tabs: TODAY (2 daily videos, player, cover, caption, description, tags, first comment, dossier, gate matrix, approval buttons), QUEUE (3-day buffer), POSTED, ANALYTICS (empty state until live), HEALTH, SETTINGS.
  - Badges read live from `runs/<id>/gates.json`.
  - Remove all obsolete style tests and legacy reels from Pages and repo. Media cleaned after posting.
- **Copy Packages**:
  - Caption: Hook, 2–3 Tenglish lines, "Sources in comments", license credit, "More in bio", 5–8 niche hashtags.
  - Description: Full dates, versions, and source citations.
  - First Comment: Exact links, quickstart commands, and paper URLs.
- **Doubt Loop**: Daily poll of user comments $\to$ clustered questions $\to$ draft grounded answers.
- **Live Posting**: Strictly gated until user explicitly gives `GO`.
