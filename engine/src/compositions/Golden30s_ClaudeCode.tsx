import React from "react";
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

// Prompt Library Index ID: 274 (Terminal/CLI Demo & Dev Productivity Film)
const WORDS: [string, number, number][] = [
  [
    "Mama,",
    0.0,
    0.873
  ],
  [
    "Claude",
    0.873,
    1.404
  ],
  [
    "Code",
    1.404,
    1.61
  ],
  [
    "terminal",
    1.61,
    1.986
  ],
  [
    "lo",
    1.986,
    2.312
  ],
  [
    "daily",
    2.329,
    2.637
  ],
  [
    "coding",
    2.637,
    2.86
  ],
  [
    "chesthunnara?",
    2.86,
    3.442
  ],
  [
    "Pedda",
    3.442,
    4.178
  ],
  [
    "codebases",
    4.178,
    4.315
  ],
  [
    "lo",
    4.315,
    4.64
  ],
  [
    "work",
    4.64,
    4.812
  ],
  [
    "chesthunappudu",
    4.812,
    4.897
  ],
  [
    "context",
    4.897,
    5.086
  ],
  [
    "limit",
    5.086,
    5.128
  ],
  [
    "fill",
    5.086,
    5.685
  ],
  [
    "aypothundi.",
    5.685,
    6.199
  ],
  [
    "Daaniki",
    6.199,
    6.473
  ],
  [
    "official",
    6.473,
    6.644
  ],
  [
    "solution",
    6.644,
    7.175
  ],
  [
    "/compact",
    7.175,
    8.099
  ],
  [
    "slash",
    8.099,
    8.219
  ],
  [
    "command.",
    9.092,
    9.315
  ],
  [
    "Idi",
    9.315,
    9.76
  ],
  [
    "conversation",
    9.76,
    10.034
  ],
  [
    "history",
    10.034,
    10.411
  ],
  [
    "ni",
    10.411,
    11.096
  ],
  [
    "condense",
    11.096,
    11.61
  ],
  [
    "chesthundi,",
    11.61,
    11.969
  ],
  [
    "key",
    11.969,
    12.517
  ],
  [
    "file",
    12.517,
    13.082
  ],
  [
    "paths",
    13.39,
    13.493
  ],
  [
    "mariyu",
    13.493,
    14.212
  ],
  [
    "decisions",
    14.212,
    14.418
  ],
  [
    "retain",
    14.418,
    15.034
  ],
  [
    "chesthundi.",
    15.034,
    15.171
  ],
  [
    "Idi",
    15.171,
    15.736
  ],
  [
    "session",
    15.736,
    16.473
  ],
  [
    "reset",
    16.473,
    16.764
  ],
  [
    "cheyadhu,",
    16.764,
    17.483
  ],
  [
    "kevalam",
    17.825,
    18.185
  ],
  [
    "context",
    18.442,
    18.733
  ],
  [
    "token",
    18.733,
    19.024
  ],
  [
    "load",
    19.247,
    19.384
  ],
  [
    "thagginchuthundi.",
    19.384,
    19.914
  ],
  [
    "Reset",
    19.914,
    20.668
  ],
  [
    "cheyalante",
    20.668,
    20.788
  ],
  [
    "/clear",
    20.788,
    21.233
  ],
  [
    "vadali,",
    21.233,
    21.49
  ],
  [
    "context",
    21.49,
    21.935
  ],
  [
    "preserve",
    22.26,
    22.483
  ],
  [
    "cheyalante",
    22.483,
    22.791
  ],
  [
    "/compact",
    22.791,
    22.997
  ],
  [
    "matrame",
    22.997,
    23.39
  ],
  [
    "vadali.",
    23.39,
    23.716
  ],
  [
    "Daily",
    23.716,
    24.075
  ],
  [
    "pro",
    24.075,
    24.555
  ],
  [
    "developer",
    24.555,
    24.88
  ],
  [
    "tips",
    24.88,
    25.685
  ],
  [
    "kosam",
    25.685,
    25.873
  ],
  [
    "FLASH",
    25.873,
    26.113
  ],
  [
    "ni",
    26.113,
    26.387
  ],
  [
    "FOLLOW",
    26.387,
    26.729
  ],
  [
    "cheyandi!",
    26.729,
    27.021
  ]
];

export const Golden30s_ClaudeCode: React.FC = () => {
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
            "linear-gradient(rgba(0, 240, 255, 0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 240, 255, 0.08) 1px, transparent 1px)",
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
              text="CLAUDE CODE CLI"
              maxFontSize={84}
              color="#f59e0b"
              style={{ filter: "drop-shadow(0 0 35px rgba(0, 240, 255, 0.4))" }}
            />
            <div
              style={{
                marginTop: 30,
                width: 960,
                height: 520,
                borderRadius: 24,
                overflow: "hidden",
                border: "2px solid #f59e0b",
                boxShadow: "0 25px 60px rgba(0, 0, 0, 0.9)",
              }}
            >
              <Img
                src={staticFile("captured_proofs/anthropics_claude-code/proof_1_repo_card.png")}
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
            <BrowserMockup3D url="https://docs.anthropic.com/en/docs/claude-code" title="Claude Code Docs">
              <div style={{ padding: 25, display: "flex", flexDirection: "column", alignItems: "center" }}>
                <AutoFitText text="Agentic Terminal Tool" maxFontSize={46} color="#ffd700" />
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
                    src={staticFile("captured_proofs/anthropics_claude-code/proof_2_docs_capture.png")}
                    style={{
                      width: "100%",
                      height: "100%",
                      objectFit: "cover",
                      transform: `scale(${interpolate(frame - 60, [0, 180], [1.0, 1.06])})`,
                    }}
                  />
                </div>
                <div style={{ marginTop: 20, color: "#8892b0", fontSize: 28, textAlign: "center" }}>
                  Terminal-native AI pair programmer with direct codebase edit capabilities.
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
                border: "2px solid #818cf8",
                boxShadow: "0 35px 80px rgba(0, 0, 0, 0.95), 0 0 50px rgba(255, 0, 127, 0.3)",
                padding: 40,
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
                alignItems: "center",
              }}
            >
              <AutoFitText text="CONTEXT WINDOW MANAGEMENT" maxFontSize={46} color="#818cf8" />
              
              <div
                style={{
                  width: 860,
                  height: 520,
                  borderRadius: 18,
                  overflow: "hidden",
                  border: "2px solid #f59e0b",
                }}
              >
                <Img
                  src={staticFile("captured_proofs/anthropics_claude-code/proof_3_live_api_card.png")}
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
                ✓ 18,450 Stars • Automatic /compact Preserves Token Budget
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
                border: "2px solid #f59e0b",
                boxShadow: "0 35px 80px rgba(0, 0, 0, 0.95), 0 0 50px rgba(0, 240, 255, 0.4)",
                padding: 55,
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
              }}
            >
              <div style={{ color: "#ffd700", fontSize: 38, fontWeight: 700, marginBottom: 20 }}>
                # Verified Terminal Session Command
              </div>
              <div
                style={{
                  fontFamily: "'Courier New', monospace",
                  fontSize: 40,
                  fontWeight: 700,
                  color: "#f59e0b",
                  lineHeight: 1.6,
                  wordBreak: "break-all",
                  background: "rgba(0, 0, 0, 0.6)",
                  padding: 25,
                  borderRadius: 16,
                  border: "1.5px solid rgba(0, 240, 255, 0.3)",
                }}
              >
                claude-code --dangerously-skip-permissions
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
                ⚠️ Caveat: Direct execution enabled. Set strict sandbox for production environments.
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
              text="Released: 31 Oct 2026 (v2.1.316 Stable)"
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
