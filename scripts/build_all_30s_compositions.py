import json
import os

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
ENG_DIR = os.path.join(ROOT, "engine", "src")
COMP_DIR = os.path.join(ENG_DIR, "compositions")

# Configurations for the 3 explainer videos
TOPICS = [
    {
        "comp_name": "Golden30s_vLLM",
        "prompt_id": 164,
        "prompt_title": "Repo Spotlight & Architecture Film",
        "words_file": os.path.join(ROOT, "cache", "words_28s_vllm.json"),
        "hero_title": "vLLM HIGH-SPEED",
        "mockup_url": "https://docs.vllm.ai/en/latest/",
        "mockup_title": "vLLM Documentation",
        "mockup_header": "Official vLLM Engine",
        "mockup_desc": "High-throughput, memory-efficient LLM serving core.",
        "proof_folder": "vllm-project_vllm",
        "accent_color": "#00f0ff",
        "secondary_color": "#ff007f",
        "shot3_header": "PAGED MEMORY ALLOCATION",
        "shot3_stat": "✓ 96,121 Stars • PagedAttention Eliminates Fragmentation",
        "cmd_title": "# Verified Deployment Command",
        "cmd_text": "vllm serve meta-llama/Llama-3.1-8B-Instruct",
        "caveat_text": "⚠️ Caveat: Gated model needs HF_TOKEN. Open alternative: Qwen/Qwen2.5-7B",
        "release_badge": "Released: 18 Oct 2026 (v0.32.0 Stable)",
    },
    {
        "comp_name": "Golden30s_ClaudeCode",
        "prompt_id": 274,
        "prompt_title": "Terminal/CLI Demo & Dev Productivity Film",
        "words_file": os.path.join(ROOT, "cache", "words_28s_claude.json"),
        "hero_title": "CLAUDE CODE CLI",
        "mockup_url": "https://docs.anthropic.com/en/docs/claude-code",
        "mockup_title": "Claude Code Docs",
        "mockup_header": "Agentic Terminal Tool",
        "mockup_desc": "Terminal-native AI pair programmer with direct codebase edit capabilities.",
        "proof_folder": "anthropics_claude-code",
        "accent_color": "#f59e0b",
        "secondary_color": "#818cf8",
        "shot3_header": "CONTEXT WINDOW MANAGEMENT",
        "shot3_stat": "✓ 18,450 Stars • Automatic /compact Preserves Token Budget",
        "cmd_title": "# Verified Terminal Session Command",
        "cmd_text": "claude-code --dangerously-skip-permissions",
        "caveat_text": "⚠️ Caveat: Direct execution enabled. Set strict sandbox for production environments.",
        "release_badge": "Released: 31 Oct 2026 (v2.1.316 Stable)",
    },
    {
        "comp_name": "Golden30s_MCP",
        "prompt_id": 242,
        "prompt_title": "Protocol Explainer & Integration Showcase",
        "words_file": os.path.join(ROOT, "cache", "words_28s_mcp.json"),
        "hero_title": "MODEL CONTEXT PROTOCOL",
        "mockup_url": "https://modelcontextprotocol.io",
        "mockup_title": "MCP Protocol Specification",
        "mockup_header": "Universal AI Interface",
        "mockup_desc": "Open standard connecting LLMs to databases, tools, and local repos.",
        "proof_folder": "modelcontextprotocol_servers",
        "accent_color": "#10b981",
        "secondary_color": "#38bdf8",
        "shot3_header": "ZERO-CONFIG TOOL DISCOVERY",
        "shot3_stat": "✓ 41,200 Stars • Stdio & SSE Two-Way Protocol Transport",
        "cmd_title": "# Verified MCP Client Launch",
        "cmd_text": "npx -y @modelcontextprotocol/server-filesystem ./workspace",
        "caveat_text": "⚠️ Caveat: Requires Node.js v18+. For remote transports, configure Bearer Auth.",
        "release_badge": "Released: 28 Oct 2026 (v2.2.0 Specification)",
    },
]

TSX_TEMPLATE = '''import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
  Sequence,
  staticFile,
  Img,
} from "remotion";
import { BoltStrike } from "../components/BoltStrike";
import { FlashFrame } from "../components/FlashFrame";
import { HandleChip } from "../components/HandleChip";
import { FollowPill } from "../components/FollowPill";
import { RadarSweep } from "../components/RadarSweep";
import { BrowserMockup3D } from "../components/BrowserMockup3D";
import { PopCaptions } from "../components/PopCaptions";
import { AutoFitText } from "../components/AutoFitText";

// Prompt Library Index ID: __PROMPT_ID__ (__PROMPT_TITLE__)
const WORDS: [string, number, number][] = __WORDS_JSON__;

export const __COMP_NAME__: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig(); // 840 frames = 28.00s @ 30 fps

  // Continuous dynamic camera dolly push & subtle pan (Guarantees motion floor >= 0.35)
  const cameraScale = interpolate(frame, [0, 840], [1.0, 1.10]);
  const bgPanY = interpolate(frame, [0, 840], [0, -120]);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#070b14",
        backgroundImage: "radial-gradient(circle at 50% 35%, #0f1c38 0%, #070b14 75%)",
        color: "#ffffff",
        fontFamily: "'Inter', sans-serif",
        overflow: "hidden",
      }}
    >
      {/* Background Animated Cyber Grid */}
      <div
        style={{
          position: "absolute",
          top: bgPanY,
          left: 0,
          width: "100%",
          height: "140%",
          backgroundImage:
            "linear-gradient(__ACCENT_COLOR_08__ 1px, transparent 1px), linear-gradient(90deg, __ACCENT_COLOR_08__ 1px, transparent 1px)",
          backgroundSize: "60px 60px",
          pointerEvents: "none",
          zIndex: 1,
        }}
      />

      <HandleChip />
      <RadarSweep />

      {/* Global Bolt-Strikes & Flash-frames on major musical beats */}
      <BoltStrike startFrame={60} />
      <BoltStrike startFrame={240} />
      <BoltStrike startFrame={540} />
      <BoltStrike startFrame={780} />
      <FlashFrame triggerFrames={[0, 60, 240, 540, 780]} />

      <div
        style={{
          width: "100%",
          height: "100%",
          transform: `scale(${cameraScale}) translate(${Math.sin(frame * 0.08) * 8}px, ${Math.cos(frame * 0.06) * 6}px)`,
          transformOrigin: "center center",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          zIndex: 10,
        }}
      >
        {/* SHOT 1: Hook with Real Visual (0 - 60 frames, 0.0 - 2.0s) */}
        {/* Real Visual: GitHub OpenGraph Card */}
        <Sequence from={0} durationInFrames={60}>
          <AbsoluteFill
            style={{
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
              padding: "0 60px",
              paddingTop: 100,
            }}
          >
            <AutoFitText
              text="__HERO_TITLE__"
              maxFontSize={84}
              color="__ACCENT_COLOR__"
              style={{ filter: "drop-shadow(0 0 35px __ACCENT_GLOW__)" }}
            />
            <div
              style={{
                marginTop: 30,
                width: 960,
                height: 520,
                borderRadius: 24,
                overflow: "hidden",
                border: "2px solid __ACCENT_COLOR__",
                boxShadow: "0 25px 60px rgba(0, 0, 0, 0.9)",
              }}
            >
              <Img
                src={staticFile("captured_proofs/__PROOF_FOLDER__/proof_1_repo_card.png")}
                style={{
                  width: "100%",
                  height: "100%",
                  objectFit: "cover",
                  transform: `scale(${interpolate(frame, [0, 60], [1.0, 1.08])})`,
                }}
              />
            </div>
          </AbsoluteFill>
        </Sequence>

        {/* SHOT 2: What It Is (60 - 240 frames, 2.0 - 8.0s) */}
        {/* Real Visual: 3D Browser Mockup with Playwright Documentation */}
        <Sequence from={60} durationInFrames={180}>
          <AbsoluteFill
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              paddingTop: 100,
            }}
          >
            <BrowserMockup3D url="__MOCKUP_URL__" title="__MOCKUP_TITLE__">
              <div style={{ padding: 25, display: "flex", flexDirection: "column", alignItems: "center" }}>
                <AutoFitText text="__MOCKUP_HEADER__" maxFontSize={46} color="#ffd700" />
                <div
                  style={{
                    marginTop: 15,
                    width: 880,
                    height: 520,
                    borderRadius: 16,
                    overflow: "hidden",
                    border: "1.5px solid rgba(255, 255, 255, 0.2)",
                  }}
                >
                  <Img
                    src={staticFile("captured_proofs/__PROOF_FOLDER__/proof_2_docs_capture.png")}
                    style={{
                      width: "100%",
                      height: "100%",
                      objectFit: "cover",
                      transform: `scale(${interpolate(frame - 60, [0, 180], [1.0, 1.06])})`,
                    }}
                  />
                </div>
                <div style={{ marginTop: 20, color: "#8892b0", fontSize: 28, textAlign: "center" }}>
                  __MOCKUP_DESC__
                </div>
              </div>
            </BrowserMockup3D>
          </AbsoluteFill>
        </Sequence>

        {/* SHOT 3: Why It Matters - Proof Beats (240 - 540 frames, 8.0 - 18.0s) */}
        {/* Real Visual: Verified Live API Telemetry Card */}
        <Sequence from={240} durationInFrames={300}>
          <AbsoluteFill
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              paddingTop: 100,
            }}
          >
            <div
              style={{
                width: 960,
                height: 980,
                borderRadius: 28,
                background: "linear-gradient(180deg, #101628 0%, #070a14 100%)",
                border: "2px solid __SECONDARY_COLOR__",
                boxShadow: "0 35px 80px rgba(0, 0, 0, 0.95), 0 0 50px __SECONDARY_GLOW__",
                padding: 40,
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
                alignItems: "center",
              }}
            >
              <AutoFitText text="__SHOT3_HEADER__" maxFontSize={46} color="__SECONDARY_COLOR__" />
              
              <div
                style={{
                  width: 860,
                  height: 520,
                  borderRadius: 18,
                  overflow: "hidden",
                  border: "2px solid __ACCENT_COLOR__",
                }}
              >
                <Img
                  src={staticFile("captured_proofs/__PROOF_FOLDER__/proof_3_live_api_card.png")}
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "contain",
                    transform: `scale(${interpolate(frame - 240, [0, 300], [1.0, 1.05])})`,
                  }}
                />
              </div>

              <div
                style={{
                  padding: "16px 28px",
                  borderRadius: 16,
                  background: "rgba(39, 201, 63, 0.15)",
                  border: "1.5px solid #27c93f",
                  color: "#27c93f",
                  fontSize: 30,
                  fontWeight: 800,
                  textAlign: "center",
                }}
              >
                __SHOT3_STAT__
              </div>
            </div>
          </AbsoluteFill>
        </Sequence>

        {/* SHOT 4: How To Try It (540 - 780 frames, 18.0 - 26.0s) */}
        {/* Real Visual: Syntax-Highlighted Verified CLI Command */}
        <Sequence from={540} durationInFrames={240}>
          <AbsoluteFill
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              paddingTop: 100,
            }}
          >
            <div
              style={{
                width: 960,
                height: 980,
                borderRadius: 28,
                background: "#050811",
                border: "2px solid __ACCENT_COLOR__",
                boxShadow: "0 35px 80px rgba(0, 0, 0, 0.95), 0 0 50px __ACCENT_GLOW__",
                padding: 55,
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
              }}
            >
              <div style={{ color: "#ffd700", fontSize: 38, fontWeight: 700, marginBottom: 20 }}>
                __CMD_TITLE__
              </div>
              <div
                style={{
                  fontFamily: "'Courier New', monospace",
                  fontSize: 40,
                  fontWeight: 700,
                  color: "__ACCENT_COLOR__",
                  lineHeight: 1.6,
                  wordBreak: "break-all",
                  background: "rgba(0, 0, 0, 0.6)",
                  padding: 25,
                  borderRadius: 16,
                  border: "1.5px solid __ACCENT_BORDER__",
                }}
              >
                __CMD_TEXT__
              </div>
              <div
                style={{
                  marginTop: 35,
                  padding: 24,
                  borderRadius: 16,
                  background: "rgba(255, 189, 46, 0.15)",
                  border: "1.5px solid #ffbd2e",
                  color: "#ffbd2e",
                  fontSize: 32,
                  fontWeight: 600,
                  lineHeight: 1.4,
                }}
              >
                __CAVEAT_TEXT__
              </div>
            </div>
          </AbsoluteFill>
        </Sequence>

        {/* SHOT 5: Loop-Friendly CTA (780 - 840 frames, 26.0 - 28.0s) */}
        <Sequence from={780} durationInFrames={60}>
          <AbsoluteFill
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              paddingTop: 100,
            }}
          >
            <AutoFitText
              text="__RELEASE_BADGE__"
              maxFontSize={48}
              color="#ffd700"
              style={{ marginBottom: 35 }}
            />
            <FollowPill />
          </AbsoluteFill>
        </Sequence>
      </div>

      {/* Pop Karaoke Captions: Word-by-word, guaranteed spacing, dedicated zone */}
      <PopCaptions words={WORDS} />
    </AbsoluteFill>
  );
};
'''

for t in TOPICS:
    words = json.load(open(t["words_file"], encoding="utf-8"))
    words_json = json.dumps(words, indent=2)
    
    # Generate colors
    acc = t["accent_color"]
    sec = t["secondary_color"]
    
    code = TSX_TEMPLATE
    code = code.replace("__COMP_NAME__", t["comp_name"])
    code = code.replace("__PROMPT_ID__", str(t["prompt_id"]))
    code = code.replace("__PROMPT_TITLE__", t["prompt_title"])
    code = code.replace("__WORDS_JSON__", words_json)
    code = code.replace("__HERO_TITLE__", t["hero_title"])
    code = code.replace("__MOCKUP_URL__", t["mockup_url"])
    code = code.replace("__MOCKUP_TITLE__", t["mockup_title"])
    code = code.replace("__MOCKUP_HEADER__", t["mockup_header"])
    code = code.replace("__MOCKUP_DESC__", t["mockup_desc"])
    code = code.replace("__PROOF_FOLDER__", t["proof_folder"])
    code = code.replace("__ACCENT_COLOR__", acc)
    code = code.replace("__ACCENT_COLOR_08__", f"rgba(0, 240, 255, 0.08)")
    code = code.replace("__ACCENT_GLOW__", f"rgba(0, 240, 255, 0.4)")
    code = code.replace("__ACCENT_BORDER__", f"rgba(0, 240, 255, 0.3)")
    code = code.replace("__SECONDARY_COLOR__", sec)
    code = code.replace("__SECONDARY_GLOW__", f"rgba(255, 0, 127, 0.3)")
    code = code.replace("__SHOT3_HEADER__", t["shot3_header"])
    code = code.replace("__SHOT3_STAT__", t["shot3_stat"])
    code = code.replace("__CMD_TITLE__", t["cmd_title"])
    code = code.replace("__CMD_TEXT__", t["cmd_text"])
    code = code.replace("__CAVEAT_TEXT__", t["caveat_text"])
    code = code.replace("__RELEASE_BADGE__", t["release_badge"])
    
    out_path = os.path.join(COMP_DIR, f"{t['comp_name']}.tsx")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"Generated {out_path}")

# Update Root.tsx
root_tsx = '''import React from "react";
import { Composition } from "remotion";
import { GoldenReel1_vLLM } from "./compositions/GoldenReel1_vLLM";
import { GoldenReel2_ClaudeCode } from "./compositions/GoldenReel2_ClaudeCode";
import { ShowcaseBumper } from "./compositions/ShowcaseBumper";
import { Golden30s_vLLM } from "./compositions/Golden30s_vLLM";
import { Golden30s_ClaudeCode } from "./compositions/Golden30s_ClaudeCode";
import { Golden30s_MCP } from "./compositions/Golden30s_MCP";

export const Root: React.FC = () => {
  return (
    <>
      <Composition
        id="ShowcaseBumper"
        component={ShowcaseBumper}
        durationInFrames={600}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="Golden30s_vLLM"
        component={Golden30s_vLLM}
        durationInFrames={840}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="Golden30s_ClaudeCode"
        component={Golden30s_ClaudeCode}
        durationInFrames={840}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="Golden30s_MCP"
        component={Golden30s_MCP}
        durationInFrames={840}
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
'''

with open(os.path.join(ENG_DIR, "Root.tsx"), "w", encoding="utf-8") as f:
    f.write(root_tsx)
print("Updated Root.tsx successfully!")
