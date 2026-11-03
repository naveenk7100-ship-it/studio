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
import { RadarSweep } from "../components/RadarSweep";
import { BrowserMockup3D } from "../components/BrowserMockup3D";
import { PopCaptions } from "../components/PopCaptions";

const CLAUDE_WORDS: [string, number, number][] = [
  ["Mama,", 0.0, 0.82],
  ["Claude", 0.0, 0.82],
  ["Code", 1.08, 1.56],
  ["lo", 1.56, 1.82],
  ["/compact", 1.82, 2.2],
  ["command", 2.2, 2.56],
  ["thelusa?", 2.56, 3.04],
  ["Context", 3.04, 3.42],
  ["limit", 3.42, 4.38],
  ["thagginchi", 4.38, 4.96],
  ["history", 4.96, 5.86],
  ["summarize", 5.86, 6.28],
  ["chesthundi.", 6.28, 6.9],
  ["Clear", 6.9, 7.1],
  ["kaadhu,", 7.1, 7.28],
  ["summary", 7.28, 7.78],
  ["matrame.", 7.78, 8.12],
  ["Daily", 8.12, 8.86],
  ["pro", 8.86, 9.08],
  ["tech", 9.08, 10.48],
  ["tips", 10.48, 10.84],
  ["kosam", 10.84, 11.62],
  ["FLASH", 11.62, 12.22],
  ["ni", 12.22, 12.84],
  ["FOLLOW", 12.84, 13.12],
  ["cheyandi!", 13.12, 13.54],
];

export const GoldenReel2_ClaudeCode: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Dynamic continuous camera dolly push & grid pan
  const cameraScale = interpolate(frame, [0, 450], [1.0, 1.12]);
  const bgPanY = interpolate(frame, [0, 450], [0, -65]);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#070b14",
        backgroundImage: `radial-gradient(circle at 50% 35%, #18172c 0%, #070b14 75%)`,
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
            "linear-gradient(rgba(255, 0, 127, 0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(255, 0, 127, 0.08) 1px, transparent 1px)",
          backgroundSize: "60px 60px",
          pointerEvents: "none",
          zIndex: 1,
        }}
      />

      <HandleChip />
      <RadarSweep />

      {/* Global Bolt-Strikes & Flash-frames snapped to beat grid */}
      <BoltStrike startFrame={50} />
      <BoltStrike startFrame={140} />
      <BoltStrike startFrame={240} />
      <BoltStrike startFrame={350} />
      <FlashFrame triggerFrames={[0, 50, 140, 240, 350]} />

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
        {/* SHOT 1: Cold Open (0 - 50 frames, 0 - 1.66s) */}
        <Sequence from={0} durationInFrames={50}>
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
                fontSize: 90, // Title >= 80px
                fontWeight: 900,
                textAlign: "center",
                color: "#ff007f",
                letterSpacing: 2.0,
                textTransform: "uppercase",
                filter: "drop-shadow(0 0 40px rgba(255, 0, 127, 0.55))",
              }}
            >
              CLAUDE CODE PRO
            </div>
            <div
              style={{
                marginTop: 35,
                fontSize: 48, // Body >= 46px
                fontWeight: 800,
                color: "#00f0ff",
                background: "rgba(0, 240, 255, 0.15)",
                padding: "16px 36px",
                borderRadius: 24,
                border: "2px solid rgba(0, 240, 255, 0.6)",
                boxShadow: "0 0 35px rgba(0, 240, 255, 0.3)",
              }}
            >
              /compact Command
            </div>
          </AbsoluteFill>
        </Sequence>

        {/* SHOT 2: Session UI Capture (50 - 140 frames, 1.66 - 4.66s) */}
        <Sequence from={50} durationInFrames={90}>
          <AbsoluteFill
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              paddingTop: 140,
            }}
          >
            {/* Hero Visual >= 45% height (1020px / 1920px = 53.1%) */}
            <div
              style={{
                width: 1000,
                height: 1020,
                borderRadius: 28,
                border: "2px solid rgba(0, 240, 255, 0.5)",
                background: "linear-gradient(180deg, #0e1526 0%, #060a14 100%)",
                padding: 60,
                boxShadow: "0 35px 80px rgba(0, 0, 0, 0.95), 0 0 45px rgba(0, 240, 255, 0.2)",
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
              }}
            >
              <div style={{ color: "#ffd700", fontSize: 44, fontWeight: 700, marginBottom: 25 }}>
                Authentic Claude Code CLI Session
              </div>
              <div
                style={{
                  fontFamily: "'Courier New', monospace",
                  fontSize: 50, // Code/Body >= 46px
                  fontWeight: 800,
                  color: "#ffffff",
                  lineHeight: 1.6,
                  background: "rgba(0, 0, 0, 0.5)",
                  padding: "20px 28px",
                  borderRadius: 16,
                  border: "1.5px solid rgba(255, 255, 255, 0.15)",
                }}
              >
                claude&gt; <span style={{ color: "#00f0ff" }}>/compact</span>
              </div>
              <div
                style={{
                  marginTop: 35,
                  color: "#cbd5e1",
                  fontSize: 46, // Body >= 46px
                  lineHeight: 1.5,
                  fontWeight: 600,
                }}
              >
                Summarizes conversation history while preserving critical context and tool results.
              </div>
            </div>
          </AbsoluteFill>
        </Sequence>

        {/* SHOT 3: 3D Browser Mockup with Official Anthropic Docs (140 - 240 frames, 4.66 - 8.0s) */}
        <Sequence from={140} durationInFrames={100}>
          <AbsoluteFill
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              paddingTop: 140,
            }}
          >
            {/* Hero Visual >= 45% height (53.1%) */}
            <BrowserMockup3D url="https://docs.anthropic.com/en/docs/claude-code" title="Claude Code Docs">
              <div
                style={{
                  fontSize: 48, // Body >= 46px
                  fontWeight: 900,
                  color: "#ffd700",
                  marginBottom: 25,
                }}
              >
                ✓ Official Anthropic Docs Verification
              </div>
              <div
                style={{
                  fontSize: 46, // Body >= 46px
                  color: "#ffffff",
                  lineHeight: 1.5,
                  fontWeight: 600,
                }}
              >
                &quot;Use <span style={{ color: "#00f0ff" }}>/compact</span> to condense session history when nearing context limits. Does NOT delete past state.&quot;
              </div>
              <div
                style={{
                  marginTop: 35,
                  fontSize: 46, // Body >= 46px
                  color: "#27c93f",
                  fontWeight: 800,
                  padding: "16px 24px",
                  borderRadius: 16,
                  background: "rgba(39, 201, 63, 0.15)",
                  border: "1.5px solid #27c93f",
                  width: "fit-content",
                }}
              >
                • Contrast: /clear resets entire session
              </div>
            </BrowserMockup3D>
          </AbsoluteFill>
        </Sequence>

        {/* SHOT 4: Context Comparison with Dynamic Animated Energy (240 - 350 frames, 8.0 - 11.66s) */}
        {/* Dynamic motion injected: pulsing progress bar, floating spring delta, animated token scale */}
        <Sequence from={240} durationInFrames={110}>
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
                background: "linear-gradient(180deg, #101524 0%, #070a12 100%)",
                border: "2px solid rgba(255, 215, 0, 0.5)",
                boxShadow: "0 35px 80px rgba(0, 0, 0, 0.95), 0 0 50px rgba(255, 215, 0, 0.2)",
                padding: 55,
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
              }}
            >
              <div
                style={{
                  fontSize: 52,
                  fontWeight: 900,
                  color: "#ffd700",
                  textAlign: "center",
                  letterSpacing: 1.5,
                }}
              >
                COMMAND CONTRAST
              </div>

              {/* Before Card */}
              <div
                style={{
                  padding: 30,
                  borderRadius: 20,
                  background: "rgba(255, 95, 86, 0.12)",
                  border: "2px solid #ff5f56",
                  transform: `translateX(${Math.sin((frame - 240) * 0.12) * 6}px)`,
                }}
              >
                <div style={{ fontSize: 44, fontWeight: 800, color: "#ff5f56" }}>
                  BEFORE /compact
                </div>
                <div style={{ fontSize: 46, color: "#ffffff", marginTop: 12, lineHeight: 1.4 }}>
                  Full verbose tool transcripts & raw outputs near context limits.
                </div>
              </div>

              {/* Dynamic Animated Token Reduction Meter */}
              <div
                style={{
                  width: "100%",
                  height: 20,
                  background: "rgba(255, 255, 255, 0.1)",
                  borderRadius: 10,
                  overflow: "hidden",
                  position: "relative",
                }}
              >
                <div
                  style={{
                    height: "100%",
                    width: `${interpolate(frame, [240, 310], [92, 28], { extrapolateRight: "clamp" })}%`,
                    background: "linear-gradient(90deg, #ff007f, #00f0ff)",
                    borderRadius: 10,
                    boxShadow: "0 0 20px #00f0ff",
                  }}
                />
              </div>

              {/* After Card */}
              <div
                style={{
                  padding: 30,
                  borderRadius: 20,
                  background: "rgba(39, 201, 63, 0.12)",
                  border: "2px solid #27c93f",
                  transform: `translateX(${Math.cos((frame - 240) * 0.12) * 6}px)`,
                }}
              >
                <div style={{ fontSize: 44, fontWeight: 800, color: "#27c93f" }}>
                  AFTER /compact
                </div>
                <div style={{ fontSize: 46, color: "#ffffff", marginTop: 12, lineHeight: 1.4 }}>
                  High-signal condensed summary retaining file paths & decisions.
                </div>
              </div>
            </div>
          </AbsoluteFill>
        </Sequence>

        {/* SHOT 5: Proof & Outro (350 - 450 frames, 11.66 - 15.0s) */}
        <Sequence from={350} durationInFrames={100}>
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
                color: "#00f0ff",
                marginBottom: 35,
                textAlign: "center",
              }}
            >
              CLAUDE CODE CLI • OFFICIAL DOCS
            </div>
            <FollowPill />
          </AbsoluteFill>
        </Sequence>
      </div>

      {/* Pop Karaoke Captions: Word-by-word, max 3 words, active highlight */}
      <PopCaptions words={CLAUDE_WORDS} />
    </AbsoluteFill>
  );
};
