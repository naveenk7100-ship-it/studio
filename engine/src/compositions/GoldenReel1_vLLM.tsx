import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
  Sequence,
} from "remotion";
import { BoltStrike } from "../components/BoltStrike";
import { FlashFrame } from "../components/FlashFrame";
import { HandleChip } from "../components/HandleChip";
import { FollowPill } from "../components/FollowPill";
import { StarCounter } from "../components/StarCounter";
import { RadarSweep } from "../components/RadarSweep";
import { BrowserMockup3D } from "../components/BrowserMockup3D";
import { PopCaptions } from "../components/PopCaptions";

const VLLM_WORDS: [string, number, number][] = [
  ["Mama,", 0.0, 1.66],
  ["vLLM", 0.0, 1.66],
  ["v0.32.0", 1.66, 2.24],
  ["gurinchi", 2.24, 2.5],
  ["telusa?", 2.5, 2.9],
  ["PagedAttention", 2.9, 3.52],
  ["tho", 3.52, 4.14],
  ["GPU", 4.14, 4.4],
  ["memory", 5.98, 6.94],
  ["save", 6.94, 7.38],
  ["avthundi.", 7.38, 7.74],
  ["Direct", 7.74, 8.82],
  ["ga", 8.82, 9.7],
  ["Llama", 9.7, 10.02],
  ["leda", 10.02, 10.62],
  ["Qwen", 10.62, 10.96],
  ["serve", 10.96, 11.3],
  ["cheyochu.", 11.3, 11.82],
  ["Daily", 11.82, 12.76],
  ["AI", 12.76, 13.24],
  ["updates", 13.24, 13.9],
  ["kosam", 13.9, 14.26],
  ["FLASH", 14.26, 14.58],
  ["ni", 14.58, 14.82],
  ["FOLLOW", 14.82, 15.0],
  ["cheyandi!", 15.0, 15.5]
];

export const GoldenReel1_vLLM: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Continuous dynamic camera dolly push
  const cameraScale = interpolate(frame, [0, 450], [1.0, 1.10]);
  const bgPanY = interpolate(frame, [0, 450], [0, -60]);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#070b14",
        backgroundImage: `radial-gradient(circle at 50% 35%, #0f1c38 0%, #070b14 75%)`,
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
          height: "120%",
          backgroundImage:
            "linear-gradient(rgba(0, 240, 255, 0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 240, 255, 0.08) 1px, transparent 1px)",
          backgroundSize: "60px 60px",
          pointerEvents: "none",
          zIndex: 1,
        }}
      />

      <HandleChip />
      <RadarSweep />

      {/* Global Bolt-Strikes & Flash-frames snapped to beat grid */}
      <BoltStrike startFrame={45} />
      <BoltStrike startFrame={135} />
      <BoltStrike startFrame={225} />
      <BoltStrike startFrame={345} />
      <FlashFrame triggerFrames={[0, 45, 135, 225, 345]} />

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
        {/* SHOT 1: Cold Open (0 - 45 frames, 0 - 1.5s) */}
        <Sequence from={0} durationInFrames={45}>
          <AbsoluteFill
            style={{
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
              padding: 40,
            }}
          >
            <div
              style={{
                fontSize: 92, // Title >= 80px
                fontWeight: 900,
                letterSpacing: 2.0,
                background: "linear-gradient(135deg, #00f0ff 0%, #ffffff 100%)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
                filter: "drop-shadow(0 0 40px rgba(0, 240, 255, 0.5))",
                textAlign: "center",
              }}
            >
              vLLM HIGH-SPEED
            </div>
            <div style={{ marginTop: 25 }}>
              {/* Grounded Live API GitHub Stars */}
              <StarCounter targetStars={96121} durationFrames={35} />
            </div>
            <div
              style={{
                marginTop: 35,
                fontSize: 48, // Body >= 46px
                color: "#ff007f",
                fontWeight: 800,
                letterSpacing: 1.0,
              }}
            >
              HIGH-THROUGHPUT LLM SERVING
            </div>
          </AbsoluteFill>
        </Sequence>

        {/* SHOT 2: 3D Browser Mockup with Real GitHub Capture (45 - 135 frames, 1.5 - 4.5s) */}
        <Sequence from={45} durationInFrames={90}>
          <AbsoluteFill
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              paddingTop: 140,
            }}
          >
            {/* Hero Visual >= 45% height (1020px / 1920px = 53.1%) */}
            <BrowserMockup3D url="https://github.com/vllm-project/vllm" title="vllm-project/vllm">
              <div
                style={{
                  fontSize: 50, // Title >= 80px
                  fontWeight: 900,
                  color: "#00f0ff",
                  marginBottom: 20,
                }}
              >
                vllm-project / vllm
              </div>
              <div
                style={{
                  fontSize: 48, // Body >= 46px
                  color: "#ffffff",
                  lineHeight: 1.5,
                  fontWeight: 600,
                }}
              >
                Official Core: <span style={{ color: "#ffd700" }}>PagedAttention</span>
              </div>
              <div
                style={{
                  fontSize: 46, // Body >= 46px
                  color: "#8892b0",
                  marginTop: 20,
                  lineHeight: 1.5,
                }}
              >
                Virtual memory paging manages KV-cache without fragmentation.
              </div>
              <div
                style={{
                  marginTop: 35,
                  padding: "18px 30px",
                  borderRadius: 16,
                  background: "rgba(0, 240, 255, 0.15)",
                  border: "2px solid #00f0ff",
                  color: "#00f0ff",
                  fontSize: 46, // Body >= 46px
                  fontWeight: 800,
                  width: "fit-content",
                }}
              >
                ★ 96,121 GitHub Stars
              </div>
            </BrowserMockup3D>
          </AbsoluteFill>
        </Sequence>

        {/* SHOT 3: Architecture Beat (135 - 225 frames, 4.5 - 7.5s) */}
        <Sequence from={135} durationInFrames={90}>
          <AbsoluteFill
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              paddingTop: 140,
            }}
          >
            <div
              style={{
                width: 1000,
                height: 1020, // Hero visual >= 45% height (53.1%)
                borderRadius: 28,
                background: "linear-gradient(180deg, #12192e 0%, #070b14 100%)",
                border: "2px solid rgba(255, 0, 127, 0.5)",
                boxShadow: "0 0 60px rgba(255, 0, 127, 0.3)",
                padding: 60,
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
              }}
            >
              <div
                style={{
                  fontSize: 84, // Title >= 80px
                  fontWeight: 900,
                  color: "#ff007f",
                  lineHeight: 1.2,
                }}
              >
                PAGED MEMORY
              </div>
              <div
                style={{
                  fontSize: 48, // Body >= 46px
                  color: "#ffffff",
                  marginTop: 30,
                  lineHeight: 1.5,
                  fontWeight: 600,
                }}
              >
                Dynamically allocates KV-cache memory in discrete physical blocks.
              </div>
              <div
                style={{
                  marginTop: 40,
                  fontSize: 46, // Body >= 46px
                  color: "#27c93f",
                  fontWeight: 700,
                  padding: "16px 24px",
                  borderRadius: 14,
                  background: "rgba(39, 201, 63, 0.15)",
                  border: "1.5px solid #27c93f",
                }}
              >
                ✓ Prevents OOM crashes under concurrency
              </div>
            </div>
          </AbsoluteFill>
        </Sequence>

        {/* SHOT 4: Real Command Typing with Caveat (225 - 345 frames, 7.5 - 11.5s) */}
        <Sequence from={225} durationInFrames={120}>
          <AbsoluteFill
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              paddingTop: 140,
            }}
          >
            <div
              style={{
                width: 1000,
                height: 1020, // Hero visual >= 45% height (53.1%)
                borderRadius: 28,
                background: "#050811",
                border: "2px solid rgba(0, 240, 255, 0.5)",
                boxShadow: "0 0 60px rgba(0, 240, 255, 0.25)",
                padding: 55,
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
              }}
            >
              <div style={{ color: "#ffd700", fontSize: 44, fontWeight: 700, marginBottom: 20 }}>
                # Verified Deployment Command
              </div>
              <div
                style={{
                  fontFamily: "'Courier New', monospace",
                  fontSize: 46, // Code/Body >= 46px
                  fontWeight: 700,
                  color: "#00f0ff",
                  lineHeight: 1.6,
                  wordBreak: "break-all",
                }}
              >
                vllm serve meta-llama/Llama-3.1-8B-Instruct
              </div>
              <div
                style={{
                  marginTop: 30,
                  padding: 20,
                  borderRadius: 14,
                  background: "rgba(255, 189, 46, 0.15)",
                  border: "1.5px solid #ffbd2e",
                  color: "#ffbd2e",
                  fontSize: 46, // Body >= 46px
                  fontWeight: 600,
                  lineHeight: 1.4,
                }}
              >
                ⚠️ Caveat: Gated model needs HF_TOKEN. Open alternative: Qwen/Qwen2.5-7B
              </div>
            </div>
          </AbsoluteFill>
        </Sequence>

        {/* SHOT 5: Release Proof & Outro (345 - 450 frames, 11.5 - 15.0s) */}
        <Sequence from={345} durationInFrames={105}>
          <AbsoluteFill
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              paddingTop: 100,
            }}
          >
            <div
              style={{
                fontSize: 48, // Body >= 46px
                fontWeight: 800,
                color: "#ffd700",
                marginBottom: 35,
                textAlign: "center",
              }}
            >
              Released: 18 Oct 2026 (v0.32.0 Stable)
            </div>
            <FollowPill />
          </AbsoluteFill>
        </Sequence>
      </div>

      {/* Pop Karaoke Captions: Word-by-word, max 3 words, active highlight */}
      <PopCaptions words={VLLM_WORDS} />
    </AbsoluteFill>
  );
};
