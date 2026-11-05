"""
FLASH Content OS - 4 Cinematic Visual-Metaphor Essay Generator
Builds 4 production-grade Remotion compositions adhering strictly to all prompt rules:
1. CinematicEssay_Unslop.tsx
2. CinematicEssay_UV.tsx
3. CinematicEssay_Kimi.tsx
4. CinematicEssay_Craft.tsx
And registers them in Root.tsx along with ShowcaseBumper.
"""

import os
import sys
import json

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
ENG_DIR = os.path.join(ROOT, "engine", "src", "compositions")
CACHE_DIR = os.path.join(ROOT, "cache")
ROOT_TSX = os.path.join(ROOT, "engine", "src", "Root.tsx")

TOPICS = [
    {
        "comp_id": "CinematicEssay-Unslop",
        "file_name": "CinematicEssay_Unslop.tsx",
        "prompt_id": 98,
        "style_name": "Fanning Cards & De-Slop Transformer",
        "accent_word": "PRECISION",
        "accent_color": "#00E5FF",
        "words_file": os.path.join(CACHE_DIR, "words_final_unslop.json"),
        "hero_title": "heydamir / unslop",
        "hero_sub": "Vibecoded UI De-Slopper & Human Styler",
        "proof_folder": "heydamir_unslop",
        "source_domain": "github.com/heydamir/unslop",
        "source_date": "29 Oct 2026",
        "stat_label": "GITHUB STARS",
        "stat_val": "9,054",
        "counter_target": 9054,
        "cmd_title": "# Claude Code Execution Commands",
        "cmd_lines": [
            "git clone https://github.com/heydamir/unslop",
            "cp -r unslop/skills/unslop ~/.claude/skills/",
            "/unslop this dashboard"
        ],
        "license_credit": "Created by Damir Sokolovsky (@heydamir) · CC BY 4.0",
        "caveat_body": "Transforms UI tokens, contrast ratios and typography; does not rewrite business backend logic.",
        "steps": [
            "Audit UI slop and hierarchy",
            "Generate human design tokens",
            "Apply redline layout pass"
        ]
    },
    {
        "comp_id": "CinematicEssay-UV",
        "file_name": "CinematicEssay_UV.tsx",
        "prompt_id": 150,
        "style_name": "Velocity Gauge & Pipeline Flow",
        "accent_word": "VELOCITY",
        "accent_color": "#FF9100",
        "words_file": os.path.join(CACHE_DIR, "words_final_uv.json"),
        "hero_title": "astral-sh / uv 0.13.7",
        "hero_sub": "Fast Python Package & Project Manager",
        "proof_folder": "astral_uv",
        "source_domain": "github.com/astral-sh/uv",
        "source_date": "03 Nov 2026",
        "stat_label": "GITHUB STARS",
        "stat_val": "91,559",
        "counter_target": 91559,
        "cmd_title": "# High-Speed Package Manager Execution",
        "cmd_lines": [
            "curl -LsSf https://astral.sh/uv/install.sh | sh",
            "uv pip install fastapi",
            "uv venv"
        ],
        "license_credit": "astral-sh / uv · Apache-2.0 / MIT",
        "caveat_body": "Replaces pip, pip-tools and virtualenv with Rust-based resolver architecture.",
        "steps": [
            "Resolve dependency graph",
            "Cache wheels concurrently",
            "Link virtualenv in milliseconds"
        ]
    },
    {
        "comp_id": "CinematicEssay-Kimi",
        "file_name": "CinematicEssay_Kimi.tsx",
        "prompt_id": 164,
        "style_name": "Neural Tile Wall & Architecture Flow",
        "accent_word": "REASONING",
        "accent_color": "#7C4DFF",
        "words_file": os.path.join(CACHE_DIR, "words_final_kimi.json"),
        "hero_title": "Moonshot AI Kimi K3.1 Pro",
        "hero_sub": "Open Weights & Reasoning Control",
        "proof_folder": "moonshot_kimi",
        "source_domain": "huggingface.co/moonshotai/Kimi-K3.1-Pro",
        "source_date": "04 Nov 2026",
        "stat_label": "HACKER NEWS SCORE",
        "stat_val": "532 Points",
        "counter_target": 532,
        "cmd_title": "# Official Model Card Client Usage",
        "cmd_lines": [
            "response = client.chat.completions.create(",
            "    model='kimi-k3.1-pro',",
            "    reasoning_effort='max'",
            ")"
        ],
        "license_credit": "Moonshot AI · Kimi K3.1 Pro Model License",
        "caveat_body": "Requires multi-node GPU cluster (8x 80GB VRAM) for unquantized local inference (~2.8T MoE parameters).",
        "steps": [
            "Download open model weights",
            "Configure reasoning effort",
            "Execute client completion call"
        ]
    },
    {
        "comp_id": "CinematicEssay-Craft",
        "file_name": "CinematicEssay_Craft.tsx",
        "prompt_id": 210,
        "style_name": "Clean-Room Reverse Engineering & Compiler Pipeline",
        "accent_word": "ARCHITECT",
        "accent_color": "#10B981",
        "words_file": os.path.join(CACHE_DIR, "words_final_craft.json"),
        "hero_title": "storytold / craft-anything",
        "hero_sub": "Clean-Room Software Engine in 100% Rust",
        "proof_folder": "storytold_craft",
        "source_domain": "github.com/storytold/craft-anything",
        "source_date": "31 Oct 2026",
        "stat_label": "GITHUB STARS",
        "stat_val": "13,530",
        "counter_target": 13530,
        "cmd_title": "# Rust Clean-Room Engine Execution",
        "cmd_lines": [
            "git clone https://github.com/storytold/craft-anything",
            "cargo run --release -p craft-anything",
            "craft-anything-cli doctor"
        ],
        "license_credit": "storytold / craft-anything · MIT / Apache-2.0",
        "caveat_body": "Inspects target apps and drives coding agents to reconstruct clean-room implementations in Rust.",
        "steps": [
            "Inspect target application",
            "Synthesize architecture spec",
            "Compile clean-room build"
        ]
    }
]

TEMPLATE_TSX = '''import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  Sequence,
  staticFile,
  Img,
} from "remotion";

const WORDS = __WORDS_JSON__;

const AutoFitText: React.FC<{ text: string; maxFontSize: number; color?: string }> = ({
  text,
  maxFontSize,
  color = "#FFFFFF",
}) => {
  const len = text.length;
  let fontSize = maxFontSize;
  if (len > 30) fontSize = Math.floor(maxFontSize * 0.72);
  else if (len > 22) fontSize = Math.floor(maxFontSize * 0.85);

  return (
    <div
      style={{
        fontSize,
        fontWeight: 800,
        color,
        letterSpacing: -0.5,
        textAlign: "center",
        lineHeight: 1.15,
        wordBreak: "break-word",
        maxWidth: 960,
      }}
    >
      {text}
    </div>
  );
};

export const __COMP_EXPORT__: React.FC = () => {
  const frame = useCurrentFrame();

  // Controlled chromatic aberration glitch: EXACTLY 4 frames (510..514) on the burst beat
  const isGlitch = frame >= 510 && frame < 514;
  const glitchOffset = isGlitch ? 6 : 0;

  // Active word in forced-alignment words list
  const currentSec = frame / 30;
  const currentWordObj = WORDS.find((w: any) => currentSec >= w.start && currentSec <= w.end);
  const currentWordIdx = currentWordObj ? WORDS.indexOf(currentWordObj) : -1;

  // Group into max 3 words window
  let captionText = "";
  if (currentWordIdx >= 0 && currentWordIdx < WORDS.length) {
    const startIdx = Math.max(0, currentWordIdx - 1);
    const endIdx = Math.min(WORDS.length, startIdx + 3);
    captionText = WORDS.slice(startIdx, endIdx).map((w: any) => w.word).join(" ");
  }

  // Camera ease: smooth, monotonic push across the reel
  const globalPush = interpolate(frame, [0, 840], [1.0, 1.045]);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#07090E",
        overflow: "hidden",
        fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
      }}
    >
      {/* GLITCH RGB SPLIT LAYER 1: CYAN */}
      {isGlitch && (
        <AbsoluteFill
          style={{
            transform: `translateX(${glitchOffset}px)`,
            mixBlendMode: "screen",
            opacity: 0.6,
            filter: "url(#cyan-glow)",
          }}
        />
      )}

      {/* PERSISTENT CHANNEL HANDLE CHIP (TOP-LEFT) for Phase Correlation Gate */}
      <div
        style={{
          position: "absolute",
          top: 130,
          left: 50,
          height: 65,
          width: 430,
          borderRadius: 32,
          background: "rgba(13, 17, 23, 0.92)",
          border: "1.5px solid rgba(0, 229, 255, 0.4)",
          display: "flex",
          alignItems: "center",
          padding: "0 22px",
          gap: 14,
          zIndex: 100,
          boxShadow: "0 8px 30px rgba(0, 0, 0, 0.6)",
        }}
      >
        <div
          style={{
            width: 14,
            height: 14,
            borderRadius: "50%",
            background: "#00E5FF",
            boxShadow: "0 0 12px #00E5FF",
          }}
        />
        <div style={{ fontSize: 24, fontWeight: 800, color: "#FFFFFF", letterSpacing: 0.5 }}>
          @flash__ai__digital
        </div>
      </div>

      {/* SHOT 1: (0 - 120f, 0.0 - 4.0s) Hook & Radar Signal Field */}
      <Sequence from={0} durationInFrames={120}>
        {(() => {
          const shotFrame = frame;
          const opacity = interpolate(shotFrame, [0, 8, 112, 120], [0, 1, 1, 0]);
          const push = interpolate(shotFrame, [0, 120], [1.0, 1.04]);
          const radarSweep = (shotFrame * 4) % 360;
          return (
            <AbsoluteFill
              style={{
                opacity,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                paddingTop: 60,
                transform: `scale(${push})`,
              }}
            >
              {/* Radar Grid Circles */}
              <div
                style={{
                  position: "absolute",
                  width: 720,
                  height: 720,
                  borderRadius: "50%",
                  border: "1.5px solid rgba(0, 229, 255, 0.15)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  transform: `rotate(${radarSweep}deg)`,
                }}
              >
                <div
                  style={{
                    position: "absolute",
                    top: 0,
                    width: 2,
                    height: 360,
                    background: "linear-gradient(to top, rgba(0, 229, 255, 0.8), transparent)",
                  }}
                />
              </div>

              {/* Hook Visual: Hero Proof Screenshot */}
              <div
                style={{
                  width: 940,
                  height: 680,
                  borderRadius: 24,
                  overflow: "hidden",
                  border: "2px solid rgba(255, 255, 255, 0.18)",
                  boxShadow: "0 20px 60px rgba(0, 0, 0, 0.7)",
                  marginBottom: 32,
                  zIndex: 2,
                }}
              >
                <Img
                  src={staticFile("captured_proofs/__PROOF_FOLDER__/proof_1_repo_card.png")}
                  style={{ width: "100%", height: "100%", objectFit: "cover" }}
                />
              </div>

              {/* Lower-third source domain */}
              <div
                style={{
                  display: "inline-block",
                  padding: "8px 20px",
                  borderRadius: 12,
                  background: "rgba(15, 23, 42, 0.85)",
                  border: "1px solid rgba(0, 229, 255, 0.3)",
                  fontSize: 22,
                  fontWeight: 700,
                  color: "#00E5FF",
                  zIndex: 2,
                }}
              >
                __SOURCE_DOMAIN__ • __SOURCE_DATE__
              </div>
            </AbsoluteFill>
          );
        })()}
      </Sequence>

      {/* SHOT 2: (120 - 250f, 4.0 - 8.33s) Sonar Rings & Bold Serif Accent */}
      <Sequence from={120} durationInFrames={130}>
        {(() => {
          const shotFrame = Math.max(0, frame - 120);
          const opacity = interpolate(shotFrame, [0, 8, 122, 130], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const push = interpolate(shotFrame, [0, 130], [1.0, 1.045], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const sonarR1 = (shotFrame * 6) % 400;
          const sonarR2 = ((shotFrame * 6) + 180) % 400;
          return (
            <AbsoluteFill
              style={{
                opacity,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                paddingTop: 60,
                transform: `scale(${push})`,
              }}
            >
              {/* Expanding Sonar Rings */}
              <div
                style={{
                  position: "absolute",
                  width: sonarR1 * 2,
                  height: sonarR1 * 2,
                  borderRadius: "50%",
                  border: "2px solid rgba(0, 229, 255, 0.3)",
                  opacity: 1 - sonarR1 / 400,
                }}
              />
              <div
                style={{
                  position: "absolute",
                  width: sonarR2 * 2,
                  height: sonarR2 * 2,
                  borderRadius: "50%",
                  border: "2px solid rgba(0, 229, 255, 0.2)",
                  opacity: 1 - sonarR2 / 400,
                }}
              />

              {/* Bold Serif Display Accent Word */}
              <div
                style={{
                  fontFamily: "Georgia, 'Times New Roman', serif",
                  fontSize: 104,
                  fontWeight: 900,
                  color: "__ACCENT_COLOR__",
                  letterSpacing: 4,
                  marginBottom: 16,
                  textShadow: "0 0 35px rgba(0, 229, 255, 0.4)",
                  zIndex: 2,
                }}
              >
                __ACCENT_WORD__
              </div>

              <div style={{ width: 920, textAlign: "center", marginBottom: 28, zIndex: 2 }}>
                <AutoFitText text="__HERO_TITLE__" maxFontSize={64} color="#FFFFFF" />
                <div style={{ fontSize: 30, fontWeight: 600, color: "#94A3B8", marginTop: 12 }}>
                  __HERO_SUB__
                </div>
              </div>

              <div
                style={{
                  width: 940,
                  height: 480,
                  borderRadius: 20,
                  overflow: "hidden",
                  border: "2px solid rgba(255, 255, 255, 0.2)",
                  boxShadow: "0 16px 45px rgba(0, 0, 0, 0.6)",
                  zIndex: 2,
                }}
              >
                <Img
                  src={staticFile("captured_proofs/__PROOF_FOLDER__/proof_2_docs_capture.png")}
                  style={{ width: "100%", height: "100%", objectFit: "contain" }}
                />
              </div>
            </AbsoluteFill>
          );
        })()}
      </Sequence>

      {/* SHOT 3: (250 - 380f, 8.33 - 12.67s) Fanning Proof Cards */}
      <Sequence from={250} durationInFrames={130}>
        {(() => {
          const shotFrame = Math.max(0, frame - 250);
          const opacity = interpolate(shotFrame, [0, 8, 122, 130], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const push = interpolate(shotFrame, [0, 130], [1.0, 1.04], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const fanAngle1 = interpolate(shotFrame, [0, 40], [0, -6], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const fanAngle2 = interpolate(shotFrame, [0, 40], [0, 6], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          return (
            <AbsoluteFill
              style={{
                opacity,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                paddingTop: 70,
                transform: `scale(${push})`,
              }}
            >
              <div style={{ width: 940, textAlign: "center", marginBottom: 24 }}>
                <div style={{ fontSize: 24, fontWeight: 800, color: "#00E5FF", letterSpacing: 2 }}>
                  CHAPTER 02 • SYSTEM ARCHITECTURE
                </div>
                <AutoFitText text="__HERO_TITLE__" maxFontSize={58} color="#FFFFFF" />
              </div>

              {/* Fanning Cards Stack */}
              <div style={{ position: "relative", width: 940, height: 680, display: "flex", justifyContent: "center" }}>
                {/* Background Card Left */}
                <div
                  style={{
                    position: "absolute",
                    width: 860,
                    height: 580,
                    borderRadius: 20,
                    overflow: "hidden",
                    border: "1.5px solid rgba(255, 255, 255, 0.15)",
                    transform: `rotate(${fanAngle1}deg) translateY(20px)`,
                    boxShadow: "0 10px 30px rgba(0, 0, 0, 0.5)",
                    opacity: 0.75,
                  }}
                >
                  <Img
                    src={staticFile("captured_proofs/__PROOF_FOLDER__/proof_1_repo_card.png")}
                    style={{ width: "100%", height: "100%", objectFit: "cover" }}
                  />
                </div>

                {/* Background Card Right */}
                <div
                  style={{
                    position: "absolute",
                    width: 860,
                    height: 580,
                    borderRadius: 20,
                    overflow: "hidden",
                    border: "1.5px solid rgba(255, 255, 255, 0.15)",
                    transform: `rotate(${fanAngle2}deg) translateY(20px)`,
                    boxShadow: "0 10px 30px rgba(0, 0, 0, 0.5)",
                    opacity: 0.75,
                  }}
                >
                  <Img
                    src={staticFile("captured_proofs/__PROOF_FOLDER__/proof_3_live_api_card.png")}
                    style={{ width: "100%", height: "100%", objectFit: "contain" }}
                  />
                </div>

                {/* Foreground Hero Card */}
                <div
                  style={{
                    position: "absolute",
                    width: 900,
                    height: 620,
                    borderRadius: 24,
                    overflow: "hidden",
                    border: "2.5px solid rgba(0, 229, 255, 0.5)",
                    boxShadow: "0 25px 70px rgba(0, 0, 0, 0.8)",
                    zIndex: 5,
                  }}
                >
                  <Img
                    src={staticFile("captured_proofs/__PROOF_FOLDER__/proof_2_docs_capture.png")}
                    style={{ width: "100%", height: "100%", objectFit: "contain" }}
                  />
                </div>
              </div>

              <div style={{ fontSize: 22, fontWeight: 600, color: "#94A3B8", marginTop: 16 }}>
                __LICENSE_CREDIT__
              </div>
            </AbsoluteFill>
          );
        })()}
      </Sequence>

      {/* SHOT 4: (380 - 510f, 12.67 - 17.0s) Execution Pipeline & Step Flow */}
      <Sequence from={380} durationInFrames={130}>
        {(() => {
          const shotFrame = Math.max(0, frame - 380);
          const opacity = interpolate(shotFrame, [0, 8, 122, 130], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const push = interpolate(shotFrame, [0, 130], [1.0, 1.045], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const activeStep = shotFrame < 45 ? 1 : shotFrame < 90 ? 2 : 3;
          return (
            <AbsoluteFill
              style={{
                opacity,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                paddingTop: 70,
                transform: `scale(${push})`,
              }}
            >
              <div style={{ width: 940, textAlign: "center", marginBottom: 28 }}>
                <div style={{ fontSize: 24, fontWeight: 800, color: "#00E5FF", letterSpacing: 2, marginBottom: 8 }}>
                  CHAPTER 03 • EXECUTION PIPELINE
                </div>
                <AutoFitText text="__HERO_TITLE__" maxFontSize={56} color="#FFFFFF" />
              </div>

              <div style={{ display: "flex", flexDirection: "column", gap: 20, width: 940 }}>
                __STEPS_JSX__
              </div>
            </AbsoluteFill>
          );
        })()}
      </Sequence>

      {/* SHOT 5: (510 - 570f, 17.0 - 19.0s) Rapid Burst Montage (Spike > 20 MAD) */}
      <Sequence from={510} durationInFrames={60}>
        {(() => {
          const burstFrame = Math.max(0, frame - 510);
          const cutIdx = Math.floor(burstFrame / 7.5);
          const images = [
            "captured_proofs/__PROOF_FOLDER__/proof_1_repo_card.png",
            "captured_proofs/__PROOF_FOLDER__/proof_2_docs_capture.png",
            "captured_proofs/__PROOF_FOLDER__/proof_3_live_api_card.png",
            "captured_proofs/__PROOF_FOLDER__/proof_1_repo_card.png",
            "captured_proofs/__PROOF_FOLDER__/proof_2_docs_capture.png",
            "captured_proofs/__PROOF_FOLDER__/proof_3_live_api_card.png",
            "captured_proofs/__PROOF_FOLDER__/proof_1_repo_card.png",
            "captured_proofs/__PROOF_FOLDER__/proof_2_docs_capture.png",
          ];
          const activeImg = images[Math.abs(cutIdx) % images.length];
          const zoom = interpolate(burstFrame % 7.5, [0, 7.5], [1.0, 1.08], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

          return (
            <AbsoluteFill
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                paddingTop: 60,
              }}
            >
              <div
                style={{
                  width: 960,
                  height: 720,
                  borderRadius: 24,
                  overflow: "hidden",
                  border: "3px solid #00E5FF",
                  boxShadow: "0 0 50px rgba(0, 229, 255, 0.4)",
                  transform: `scale(${zoom})`,
                }}
              >
                <Img
                  src={staticFile(activeImg)}
                  style={{ width: "100%", height: "100%", objectFit: "contain" }}
                />
              </div>
            </AbsoluteFill>
          );
        })()}
      </Sequence>

      {/* SHOT 6: (570 - 660f, 19.0 - 22.0s) 3D Tilted Telemetry Card & Settle Counter */}
      <Sequence from={570} durationInFrames={90}>
        {(() => {
          const shotFrame = Math.max(0, frame - 570);
          const opacity = interpolate(shotFrame, [0, 8, 82, 90], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const push = interpolate(shotFrame, [0, 90], [1.0, 1.04], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const rotY = interpolate(shotFrame, [0, 90], [14, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const rotX = interpolate(shotFrame, [0, 90], [8, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

          // Counter settles on EXACT data object value
          const counterVal = Math.floor(
            interpolate(shotFrame, [0, 50], [Math.floor(__COUNTER_TARGET__ * 0.75), __COUNTER_TARGET__], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            })
          );

          return (
            <AbsoluteFill
              style={{
                opacity,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                paddingTop: 60,
                perspective: 1200,
                transform: `scale(${push})`,
              }}
            >
              <div
                style={{
                  width: 940,
                  height: 740,
                  borderRadius: 24,
                  overflow: "hidden",
                  border: "2px solid rgba(0, 229, 255, 0.5)",
                  boxShadow: "0 25px 70px rgba(0, 0, 0, 0.8)",
                  transform: `rotateY(${rotY}deg) rotateX(${rotX}deg)`,
                  background: "#0E1217",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  padding: "40px 30px",
                }}
              >
                <div style={{ fontSize: 24, fontWeight: 800, color: "#00E5FF", letterSpacing: 2, marginBottom: 12 }}>
                  __STAT_LABEL__
                </div>
                <div style={{ fontSize: 84, fontWeight: 900, color: "#FFFFFF", marginBottom: 20 }}>
                  {counterVal.toLocaleString()}
                </div>
                <div style={{ fontSize: 26, fontWeight: 600, color: "#94A3B8", marginBottom: 30 }}>
                  __SOURCE_DOMAIN__ • __SOURCE_DATE__
                </div>

                <div
                  style={{
                    width: 860,
                    height: 380,
                    borderRadius: 16,
                    overflow: "hidden",
                    border: "1.5px solid rgba(255, 255, 255, 0.15)",
                  }}
                >
                  <Img
                    src={staticFile("captured_proofs/__PROOF_FOLDER__/proof_1_repo_card.png")}
                    style={{ width: "100%", height: "100%", objectFit: "cover" }}
                  />
                </div>
              </div>
            </AbsoluteFill>
          );
        })()}
      </Sequence>

      {/* SHOT 7: (660 - 756f, 22.0 - 25.2s) Command Blueprint & Action Item */}
      <Sequence from={660} durationInFrames={96}>
        {(() => {
          const shotFrame = Math.max(0, frame - 660);
          const opacity = interpolate(shotFrame, [0, 8, 88, 96], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const push = interpolate(shotFrame, [0, 96], [1.0, 1.04], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          return (
            <AbsoluteFill
              style={{
                opacity,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                paddingTop: 60,
                transform: `scale(${push})`,
              }}
            >
              <div style={{ width: 940, textAlign: "center", marginBottom: 24 }}>
                <div style={{ fontSize: 24, fontWeight: 800, color: "#00E5FF", letterSpacing: 2, marginBottom: 8 }}>
                  __CMD_TITLE__
                </div>
                <AutoFitText text="__HERO_TITLE__" maxFontSize={54} color="#FFFFFF" />
              </div>

              {/* Terminal Code Card */}
              <div
                style={{
                  width: 940,
                  borderRadius: 20,
                  background: "#0D1117",
                  border: "2px solid rgba(0, 229, 255, 0.4)",
                  boxShadow: "0 20px 60px rgba(0, 0, 0, 0.7)",
                  padding: "32px 36px",
                  display: "flex",
                  flexDirection: "column",
                  gap: 16,
                  marginBottom: 24,
                }}
              >
                __CMD_JSX__
              </div>

              {/* Caveat */}
              <div
                style={{
                  width: 940,
                  borderRadius: 16,
                  background: "rgba(255, 255, 255, 0.04)",
                  border: "1px solid rgba(255, 255, 255, 0.1)",
                  padding: "18px 24px",
                  fontSize: 22,
                  color: "#94A3B8",
                  lineHeight: 1.4,
                  textAlign: "center",
                }}
              >
                __CAVEAT_BODY__
              </div>
            </AbsoluteFill>
          );
        })()}
      </Sequence>

      {/* SHOT 8: (756 - 840f, 25.2 - 28.0s) FOLLOW END CARD (Loop-Friendly Vignette Scene) */}
      <Sequence from={756} durationInFrames={84}>
        {(() => {
          const endFrame = Math.max(0, frame - 756);
          // Fade in at 0..8f; dissolve to black/initial frame at 78..84f for seamless looping
          const opacity = interpolate(endFrame, [0, 8, 76, 84], [0, 1, 1, 0.85], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const push = interpolate(endFrame, [0, 84], [1.0, 1.05], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const ringScale = interpolate(endFrame, [0, 84], [1.0, 1.4], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const ringOpacity = interpolate(endFrame, [0, 84], [0.6, 0.0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

          // Tap animation: frame 20..28 presses down, then turns into "Following" with check
          const isTapped = endFrame >= 24;
          const buttonScale = interpolate(endFrame, [18, 22, 26, 30], [1.0, 0.94, 0.94, 1.0], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });

          return (
            <AbsoluteFill
              style={{
                opacity,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                background: "radial-gradient(circle at center, #161D2A 0%, #07090E 75%)",
                transform: `scale(${push})`,
              }}
            >
              {/* Profile Avatar with Expanding Wave Ring */}
              <div
                style={{
                  position: "relative",
                  width: 220,
                  height: 220,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  marginBottom: 36,
                }}
              >
                {/* Expanding pulse ring */}
                <div
                  style={{
                    position: "absolute",
                    width: 220,
                    height: 220,
                    borderRadius: "50%",
                    border: "3px solid #00E5FF",
                    transform: `scale(${ringScale})`,
                    opacity: ringOpacity,
                  }}
                />

                {/* Profile Circle */}
                <div
                  style={{
                    width: 200,
                    height: 200,
                    borderRadius: "50%",
                    overflow: "hidden",
                    border: "4px solid #00E5FF",
                    boxShadow: "0 0 40px rgba(0, 229, 255, 0.5)",
                  }}
                >
                  <Img
                    src={staticFile("brand/profile.png")}
                    style={{ width: "100%", height: "100%", objectFit: "cover" }}
                  />
                </div>
              </div>

              {/* Interactive Follow Pill Button with Tap Animation */}
              <div
                style={{
                  transform: `scale(${buttonScale})`,
                  padding: "20px 48px",
                  borderRadius: 40,
                  background: isTapped ? "linear-gradient(135deg, #00E5FF, #00B4D8)" : "rgba(255, 255, 255, 0.08)",
                  border: isTapped ? "none" : "2px solid #00E5FF",
                  boxShadow: isTapped ? "0 0 45px rgba(0, 229, 255, 0.6)" : "none",
                  display: "flex",
                  alignItems: "center",
                  gap: 16,
                  marginBottom: 24,
                }}
              >
                <div
                  style={{
                    fontSize: 32,
                    fontWeight: 900,
                    color: isTapped ? "#07090E" : "#FFFFFF",
                    letterSpacing: 1.2,
                  }}
                >
                  {isTapped ? "Following ✓" : "FOLLOW @flash__ai__digital"}
                </div>
              </div>

              {/* Whitelisted Subtitle Line */}
              <div
                style={{
                  fontSize: 26,
                  fontWeight: 600,
                  color: "#94A3B8",
                  textAlign: "center",
                  maxWidth: 800,
                  lineHeight: 1.4,
                }}
              >
                Daily AI and dev updates, with sources
              </div>
            </AbsoluteFill>
          );
        })()}
      </Sequence>

      {/* POP CAPTIONS (Forced Alignment Driven, Safe Zone Margins) */}
      {captionText && frame < 756 && (
        <div
          style={{
            position: "absolute",
            bottom: 390,
            left: 60,
            right: 60,
            display: "flex",
            justifyContent: "center",
            zIndex: 120,
            pointerEvents: "none",
          }}
        >
          <div
            style={{
              padding: "16px 28px",
              borderRadius: 20,
              background: "rgba(9, 12, 16, 0.92)",
              border: "1.5px solid rgba(0, 229, 255, 0.4)",
              boxShadow: "0 10px 40px rgba(0, 0, 0, 0.8)",
              fontSize: 38,
              fontWeight: 800,
              color: "#FFFFFF",
              letterSpacing: 0.5,
              textAlign: "center",
              maxWidth: 900,
            }}
          >
            {captionText}
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};
'''

def generate_steps_jsx(steps):
    jsx = ""
    for idx, s in enumerate(steps):
        step_num = f"0{idx+1}"
        jsx += f"""
                <div
                  style={{{{
                    display: "flex",
                    alignItems: "center",
                    gap: 24,
                    padding: "24px 32px",
                    borderRadius: 18,
                    background: activeStep === {idx+1} ? "rgba(0, 229, 255, 0.15)" : "#161B22",
                    border: activeStep === {idx+1} ? "2px solid #00E5FF" : "1.5px solid #30363D",
                    boxShadow: activeStep === {idx+1} ? "0 0 25px rgba(0, 229, 255, 0.3)" : "none",
                  }}}}
                >
                  <div style={{{{ fontSize: 28, fontWeight: 900, color: activeStep === {idx+1} ? "#00E5FF" : "#64748B" }}}}>
                    {step_num}
                  </div>
                  <div style={{{{ fontSize: 32, fontWeight: 700, color: activeStep === {idx+1} ? "#FFFFFF" : "#CBD5E1" }}}}>
                    {s}
                  </div>
                </div>
        """
    return jsx

def generate_cmd_jsx(cmd_lines):
    jsx = ""
    for line in cmd_lines:
        jsx += f"""
                <div style={{{{ fontSize: 30, fontFamily: "consola, monospace", color: "#38BDF8", fontWeight: 700 }}}}>
                  {line}
                </div>
        """
    return jsx

def build_all():
    print("================ GENERATING 4 CINEMATIC VISUAL-METAPHOR ESSAYS ================")
    
    root_imports = []
    root_comps = []
    
    for t in TOPICS:
        comp_id = t["comp_id"]
        file_name = t["file_name"]
        comp_export = file_name.replace(".tsx", "")
        out_path = os.path.join(ENG_DIR, file_name)
        
        with open(t["words_file"], "r", encoding="utf-8") as f:
            words_data = json.load(f)
            
        steps_jsx = generate_steps_jsx(t["steps"])
        cmd_jsx = generate_cmd_jsx(t["cmd_lines"])
        
        code = TEMPLATE_TSX
        code = code.replace("__COMP_EXPORT__", comp_export)
        code = code.replace("__WORDS_JSON__", json.dumps(words_data))
        code = code.replace("__HERO_TITLE__", t["hero_title"])
        code = code.replace("__HERO_SUB__", t["hero_sub"])
        code = code.replace("__PROOF_FOLDER__", t["proof_folder"])
        code = code.replace("__SOURCE_DOMAIN__", t["source_domain"])
        code = code.replace("__SOURCE_DATE__", t["source_date"])
        code = code.replace("__STAT_LABEL__", t["stat_label"])
        code = code.replace("__STAT_VAL__", t["stat_val"])
        code = code.replace("__COUNTER_TARGET__", str(t["counter_target"]))
        code = code.replace("__CMD_TITLE__", t["cmd_title"])
        code = code.replace("__CMD_JSX__", cmd_jsx)
        code = code.replace("__LICENSE_CREDIT__", t["license_credit"])
        code = code.replace("__CAVEAT_BODY__", t["caveat_body"])
        code = code.replace("__ACCENT_WORD__", t["accent_word"])
        code = code.replace("__ACCENT_COLOR__", t["accent_color"])
        code = code.replace("__STEPS_JSX__", steps_jsx)
        
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"  [CREATED] {out_path} ({len(code)} bytes)")
        
        root_imports.append(f'import {{ {comp_export} }} from "./compositions/{comp_export}";')
        root_comps.append(f'''      <Composition
        id="{comp_id}"
        component={{{comp_export}}}
        durationInFrames={{840}}
        fps={{30}}
        width={{1080}}
        height={{1920}}
      />''')

    # Update Root.tsx
    root_code = f'''import React from "react";
import {{ Composition }} from "remotion";
import {{ ShowcaseBumper }} from "./compositions/ShowcaseBumper";
{chr(10).join(root_imports)}

export const Root: React.FC = () => {{
  return (
    <>
      <Composition
        id="ShowcaseBumper"
        component={{ShowcaseBumper}}
        durationInFrames={{600}}
        fps={{30}}
        width={{1080}}
        height={{1920}}
      />
{chr(10).join(root_comps)}
    </>
  );
}};
'''
    with open(ROOT_TSX, "w", encoding="utf-8") as f:
        f.write(root_code)
    print(f"  [UPDATED] {ROOT_TSX}")

if __name__ == "__main__":
    build_all()
