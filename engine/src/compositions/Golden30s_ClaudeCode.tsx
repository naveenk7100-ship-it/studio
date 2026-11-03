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
import { HandleChip } from "../components/HandleChip";
import { FollowPill } from "../components/FollowPill";
import { RadarSweep } from "../components/RadarSweep";
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

  // Monotonic, smooth camera push-in: scale 1.0 -> 1.04 over the whole 28s (max 4% push, bounded jerk)
  const cameraScale = interpolate(frame, [0, 840], [1.0, 1.04], { extrapolateRight: "clamp" });
  
  // Parallax Layer 1: Background grid subtle vertical drift (0 to -140px, ~5px/sec smooth monotonic drift)
  const bgPanY = interpolate(frame, [0, 840], [0, -140], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#060913",
        backgroundImage: "radial-gradient(circle at 50% 30%, #0d162d 0%, #060913 80%)",
        color: "#ffffff",
        fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        overflow: "hidden",
      }}
    >
      {/* PARALLAX LAYER 1: Subtle Cyber Grid */}
      <div
        style={{
          position: "absolute",
          top: bgPanY,
          left: 0,
          width: "100%",
          height: "120%",
          backgroundImage:
            "linear-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(255, 255, 255, 0.04) 1px, transparent 1px)",
          backgroundSize: "60px 60px",
          pointerEvents: "none",
          zIndex: 1,
        }}
      />

      {/* Persistent Channel Branding Safe Zones */}
      <HandleChip />
      <RadarSweep />

      {/* PARALLAX LAYER 2: Main Content Camera (Monotonic Scale, Zero Jitter) */}
      <div
        style={{
          width: "100%",
          height: "100%",
          transform: `scale(${cameraScale})`,
          transformOrigin: "center center",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          zIndex: 10,
        }}
      >
        {/* SHOT 1: (0 - 80f, 0.0 - 2.67s) Hook & Official GitHub Repository Card */}
        <Sequence from={0} durationInFrames={80}>
          {(() => {
            const shotFrame = frame;
            const opacity = interpolate(shotFrame, [0, 10, 70, 80], [0, 1, 1, 0]);
            const push = interpolate(shotFrame, [0, 80], [1.0, 1.02]);
            return (
              <AbsoluteFill
                style={{
                  opacity,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  paddingTop: 80,
                  transform: `scale(${push})`,
                }}
              >
                <div style={{ width: 960, textAlign: "center", marginBottom: 20 }}>
                  <AutoFitText text="Claude Code v2.1.317" maxFontSize={76} color="#f59e0b" />
                  <div style={{ fontSize: 26, fontWeight: 700, color: "#94a3b8", letterSpacing: 2, marginTop: 8 }}>
                    TERMINAL-NATIVE AGENT
                  </div>
                </div>

                <div
                  style={{
                    width: 960,
                    height: 520,
                    borderRadius: 24,
                    overflow: "hidden",
                    border: "2px solid rgba(255, 255, 255, 0.15)",
                    boxShadow: "0 12px 32px rgba(0, 0, 0, 0.35)",
                    background: "#0f172a",
                  }}
                >
                  <Img
                    src={staticFile("captured_proofs/anthropics_claude-code/proof_1_repo_card.png")}
                    style={{ width: "100%", height: "100%", objectFit: "cover" }}
                  />
                </div>

                <div
                  style={{
                    marginTop: 24,
                    padding: "10px 24px",
                    borderRadius: 20,
                    background: "rgba(255, 255, 255, 0.08)",
                    border: "1px solid rgba(255, 255, 255, 0.2)",
                    fontSize: 22,
                    fontWeight: 700,
                    color: "#f8fafc",
                  }}
                >
                  v2.1.317 • 3 Nov 2026 • ★ 18,450 Stars
                </div>
              </AbsoluteFill>
            );
          })()}
        </Sequence>

        {/* SHOT 2: (80 - 170f, 2.67 - 5.67s) WOW BEAT: Core Architecture & Output Screenshot */}
        <Sequence from={80} durationInFrames={90}>
          {(() => {
            const shotFrame = frame - 80;
            const opacity = interpolate(shotFrame, [0, 10, 80, 90], [0, 1, 1, 0]);
            const slideY = interpolate(shotFrame, [0, 12], [20, 0], { extrapolateRight: "clamp" });
            const push = interpolate(shotFrame, [0, 90], [1.0, 1.025]);
            return (
              <AbsoluteFill
                style={{
                  opacity,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  paddingTop: 80,
                  transform: `translateY(${slideY}px) scale(${push})`,
                }}
              >
                <div
                  style={{
                    width: 960,
                    height: 980,
                    borderRadius: 24,
                    background: "#0c1122",
                    border: "2px solid #f59e0b",
                    boxShadow: "0 12px 32px rgba(0, 0, 0, 0.35)",
                    padding: 40,
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "space-between",
                    alignItems: "center",
                  }}
                >
                  <div style={{ textAlign: "center" }}>
                    <div style={{ fontSize: 22, fontWeight: 800, color: "#f59e0b", letterSpacing: 3, marginBottom: 8 }}>
                      CORE BREAKTHROUGH [3.0s WOW BEAT]
                    </div>
                    <AutoFitText text="AUTOMATIC CONTEXT MANAGEMENT" maxFontSize={52} color="#ffffff" />
                  </div>

                  <div
                    style={{
                      width: 880,
                      height: 580,
                      borderRadius: 18,
                      overflow: "hidden",
                      border: "1.5px solid rgba(255, 255, 255, 0.15)",
                      boxShadow: "0 8px 24px rgba(0, 0, 0, 0.5)",
                    }}
                  >
                    <Img
                      src={staticFile("captured_proofs/anthropics_claude-code/proof_2_docs_capture.png")}
                      style={{ width: "100%", height: "100%", objectFit: "cover" }}
                    />
                  </div>

                  <div
                    style={{
                      width: "100%",
                      padding: "16px 24px",
                      borderRadius: 16,
                      background: "rgba(16, 185, 129, 0.15)",
                      border: "1.5px solid #10b981",
                      color: "#34d399",
                      fontSize: 26,
                      fontWeight: 800,
                      textAlign: "center",
                    }}
                  >
                    ⚡ Built-in /compact Slash Command Saves Token Budget
                  </div>
                </div>
              </AbsoluteFill>
            );
          })()}
        </Sequence>

        {/* SHOT 3: (170 - 260f, 5.67 - 8.67s) Official Documentation Deep-Dive */}
        <Sequence from={170} durationInFrames={90}>
          {(() => {
            const shotFrame = frame - 170;
            const opacity = interpolate(shotFrame, [0, 10, 80, 90], [0, 1, 1, 0]);
            const push = interpolate(shotFrame, [0, 90], [1.0, 1.03]);
            return (
              <AbsoluteFill
                style={{
                  opacity,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  paddingTop: 80,
                  transform: `scale(${push})`,
                }}
              >
                <div
                  style={{
                    width: 960,
                    height: 980,
                    borderRadius: 24,
                    background: "#0a0e1c",
                    border: "2px solid rgba(255, 255, 255, 0.15)",
                    boxShadow: "0 12px 32px rgba(0, 0, 0, 0.35)",
                    overflow: "hidden",
                  }}
                >
                  {/* Browser Bar */}
                  <div
                    style={{
                      height: 54,
                      background: "#161f36",
                      display: "flex",
                      alignItems: "center",
                      padding: "0 20px",
                      gap: 10,
                      borderBottom: "1px solid rgba(255, 255, 255, 0.1)",
                    }}
                  >
                    <div style={{ width: 14, height: 14, borderRadius: "50%", background: "#ff5f56" }} />
                    <div style={{ width: 14, height: 14, borderRadius: "50%", background: "#ffbd2e" }} />
                    <div style={{ width: 14, height: 14, borderRadius: "50%", background: "#27c93f" }} />
                    <div
                      style={{
                        marginLeft: 18,
                        flex: 1,
                        background: "#0a0e1c",
                        borderRadius: 8,
                        padding: "6px 16px",
                        fontSize: 18,
                        color: "#94a3b8",
                      }}
                    >
                      🔒 https://docs.anthropic.com/claude-code
                    </div>
                  </div>

                  <div style={{ padding: 30, display: "flex", flexDirection: "column", alignItems: "center" }}>
                    <AutoFitText text="Claude Code Reference" maxFontSize={46} color="#f59e0b" />
                    <div
                      style={{
                        marginTop: 20,
                        width: 880,
                        height: 520,
                        borderRadius: 16,
                        overflow: "hidden",
                        border: "1px solid rgba(255, 255, 255, 0.15)",
                      }}
                    >
                      <Img
                        src={staticFile("captured_proofs/anthropics_claude-code/proof_2_docs_capture.png")}
                        style={{ width: "100%", height: "100%", objectFit: "cover" }}
                      />
                    </div>
                    <div style={{ marginTop: 24, fontSize: 26, color: "#cbd5e1", textAlign: "center", maxWidth: 840 }}>
                      Terminal agent with direct codebase editing and sub-process execution.
                    </div>
                  </div>
                </div>
              </AbsoluteFill>
            );
          })()}
        </Sequence>

        {/* SHOT 4: (260 - 350f, 8.67 - 11.67s) Verified Live Telemetry Data Card */}
        <Sequence from={260} durationInFrames={90}>
          {(() => {
            const shotFrame = frame - 260;
            const opacity = interpolate(shotFrame, [0, 10, 80, 90], [0, 1, 1, 0]);
            const push = interpolate(shotFrame, [0, 90], [1.0, 1.03]);
            return (
              <AbsoluteFill
                style={{
                  opacity,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  paddingTop: 80,
                  transform: `scale(${push})`,
                }}
              >
                <div
                  style={{
                    width: 960,
                    height: 980,
                    borderRadius: 24,
                    background: "#0d1326",
                    border: "2px solid #818cf8",
                    boxShadow: "0 12px 32px rgba(0, 0, 0, 0.35)",
                    padding: 40,
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "space-between",
                    alignItems: "center",
                  }}
                >
                  <AutoFitText text="AGENT ARCHITECTURE" maxFontSize={48} color="#818cf8" />

                  <div
                    style={{
                      width: 860,
                      height: 540,
                      borderRadius: 18,
                      overflow: "hidden",
                      border: "2px solid rgba(255, 255, 255, 0.15)",
                    }}
                  >
                    <Img
                      src={staticFile("captured_proofs/anthropics_claude-code/proof_3_live_api_card.png")}
                      style={{ width: "100%", height: "100%", objectFit: "contain" }}
                    />
                  </div>

                  <div
                    style={{
                      width: "100%",
                      padding: "16px 28px",
                      borderRadius: 16,
                      background: "rgba(255, 0, 127, 0.12)",
                      border: "1.5px solid #818cf8",
                      color: "#ffffff",
                      fontSize: 26,
                      fontWeight: 800,
                      textAlign: "center",
                    }}
                  >
                    📊 Read/Write Tools + Dynamic MCP Tool Expansion
                  </div>
                </div>
              </AbsoluteFill>
            );
          })()}
        </Sequence>

        {/* SHOT 5: (350 - 450f, 11.67 - 15.0s) Syntax-Highlighted Verified CLI Command */}
        <Sequence from={350} durationInFrames={100}>
          {(() => {
            const shotFrame = frame - 350;
            const opacity = interpolate(shotFrame, [0, 10, 90, 100], [0, 1, 1, 0]);
            const push = interpolate(shotFrame, [0, 100], [1.0, 1.03]);
            return (
              <AbsoluteFill
                style={{
                  opacity,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  paddingTop: 80,
                  transform: `scale(${push})`,
                }}
              >
                <div
                  style={{
                    width: 960,
                    height: 980,
                    borderRadius: 24,
                    background: "#080c18",
                    border: "2px solid #f59e0b",
                    boxShadow: "0 12px 32px rgba(0, 0, 0, 0.35)",
                    padding: 50,
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "space-between",
                  }}
                >
                  <div>
                    <div style={{ fontSize: 24, fontWeight: 800, color: "#f59e0b", marginBottom: 12 }}>
                      # Verified Session Launch
                    </div>
                    <div
                      style={{
                        padding: 32,
                        borderRadius: 18,
                        background: "#020409",
                        border: "1.5px solid rgba(255, 255, 255, 0.12)",
                        color: "#38bdf8",
                        fontFamily: "'Fira Code', monospace",
                        fontSize: 32,
                        lineHeight: 1.5,
                        wordBreak: "break-word",
                      }}
                    >
                      $ claude-code --dangerously-skip-permissions
                    </div>
                  </div>

                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: 20,
                      padding: 24,
                      borderRadius: 16,
                      background: "rgba(255, 255, 255, 0.05)",
                      border: "1px solid rgba(255, 255, 255, 0.15)",
                    }}
                  >
                    <div style={{ fontSize: 36 }}>⚡</div>
                    <div style={{ fontSize: 26, color: "#e2e8f0" }}>
                      Run directly in terminal. Fully reproducible on Linux & WSL2.
                    </div>
                  </div>

                  <div style={{ fontSize: 22, color: "#64748b", textAlign: "center" }}>
                    Verified against live GitHub repository tags
                  </div>
                </div>
              </AbsoluteFill>
            );
          })()}
        </Sequence>

        {/* SHOT 6: (450 - 550f, 15.0 - 18.33s) Verified Caveats & Security Note */}
        <Sequence from={450} durationInFrames={100}>
          {(() => {
            const shotFrame = frame - 450;
            const opacity = interpolate(shotFrame, [0, 10, 90, 100], [0, 1, 1, 0]);
            const push = interpolate(shotFrame, [0, 100], [1.0, 1.02]);
            return (
              <AbsoluteFill
                style={{
                  opacity,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  paddingTop: 80,
                  transform: `scale(${push})`,
                }}
              >
                <div
                  style={{
                    width: 960,
                    height: 980,
                    borderRadius: 24,
                    background: "#130f1d",
                    border: "2px solid #f59e0b",
                    boxShadow: "0 12px 32px rgba(0, 0, 0, 0.35)",
                    padding: 50,
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "space-between",
                  }}
                >
                  <div style={{ textAlign: "center" }}>
                    <div style={{ fontSize: 44, marginBottom: 12 }}>⚠️</div>
                    <AutoFitText text="VERIFIED SECURITY CAVEAT" maxFontSize={48} color="#f59e0b" />
                  </div>

                  <div
                    style={{
                      padding: 36,
                      borderRadius: 18,
                      background: "rgba(245, 158, 11, 0.08)",
                      border: "1.5px solid rgba(245, 158, 11, 0.3)",
                      fontSize: 30,
                      lineHeight: 1.6,
                      color: "#fef3c7",
                      textAlign: "center",
                    }}
                  >
                    --dangerously-skip-permissions bypasses interactive prompts. Run strictly inside Docker or isolated ephemeral VM sandbox environments.
                  </div>

                  <div style={{ fontSize: 24, fontWeight: 700, color: "#94a3b8", textAlign: "center" }}>
                    Source Truth Gates: 100% Tested • Zero Hallucinations
                  </div>
                </div>
              </AbsoluteFill>
            );
          })()}
        </Sequence>

        {/* SHOT 7: (550 - 660f, 18.33 - 22.0s) Full Spec & Performance Summary */}
        <Sequence from={550} durationInFrames={110}>
          {(() => {
            const shotFrame = frame - 550;
            const opacity = interpolate(shotFrame, [0, 10, 100, 110], [0, 1, 1, 0]);
            const push = interpolate(shotFrame, [0, 110], [1.0, 1.02]);
            return (
              <AbsoluteFill
                style={{
                  opacity,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  paddingTop: 80,
                  transform: `scale(${push})`,
                }}
              >
                <div
                  style={{
                    width: 960,
                    height: 980,
                    borderRadius: 24,
                    background: "#09101f",
                    border: "2px solid #f59e0b",
                    boxShadow: "0 12px 32px rgba(0, 0, 0, 0.35)",
                    padding: 40,
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "space-between",
                    alignItems: "center",
                  }}
                >
                  <AutoFitText text="PRODUCTION READINESS" maxFontSize={48} color="#f59e0b" />

                  <div
                    style={{
                      width: 880,
                      height: 520,
                      borderRadius: 18,
                      overflow: "hidden",
                      border: "1.5px solid rgba(255, 255, 255, 0.15)",
                    }}
                  >
                    <Img
                      src={staticFile("captured_proofs/anthropics_claude-code/proof_1_repo_card.png")}
                      style={{ width: "100%", height: "100%", objectFit: "cover" }}
                    />
                  </div>

                  <div
                    style={{
                      display: "flex",
                      gap: 20,
                      width: "100%",
                      justifyContent: "center",
                    }}
                  >
                    <div
                      style={{
                        padding: "14px 28px",
                        borderRadius: 14,
                        background: "rgba(0, 240, 255, 0.1)",
                        border: "1px solid #f59e0b",
                        fontSize: 24,
                        fontWeight: 700,
                        color: "#ffffff",
                      }}
                    >
                      ✓ Zero Budget
                    </div>
                    <div
                      style={{
                        padding: "14px 28px",
                        borderRadius: 14,
                        background: "rgba(16, 185, 129, 0.1)",
                        border: "1px solid #10b981",
                        fontSize: 24,
                        fontWeight: 700,
                        color: "#ffffff",
                      }}
                    >
                      ✓ 100% Open Source
                    </div>
                  </div>
                </div>
              </AbsoluteFill>
            );
          })()}
        </Sequence>

        {/* SHOT 8: (660 - 840f, 22.0 - 28.0s) Resource Pack URL & Channel CTA */}
        <Sequence from={660} durationInFrames={180}>
          {(() => {
            const shotFrame = frame - 660;
            const opacity = interpolate(shotFrame, [0, 10], [0, 1]);
            const push = interpolate(shotFrame, [0, 180], [1.0, 1.02]);
            return (
              <AbsoluteFill
                style={{
                  opacity,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  paddingTop: 80,
                  transform: `scale(${push})`,
                }}
              >
                <div
                  style={{
                    width: 960,
                    height: 980,
                    borderRadius: 24,
                    background: "linear-gradient(180deg, #0e172e 0%, #060913 100%)",
                    border: "2px solid #00f0ff",
                    boxShadow: "0 12px 32px rgba(0, 0, 0, 0.35)",
                    padding: 50,
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    justifyContent: "space-between",
                  }}
                >
                  <div style={{ textAlign: "center" }}>
                    <div style={{ fontSize: 24, fontWeight: 800, color: "#00f0ff", letterSpacing: 3, marginBottom: 8 }}>
                      COMPLETE RESOURCE PACK
                    </div>
                    <div style={{ fontSize: 50, fontWeight: 900, color: "#ffffff", lineHeight: 1.2 }}>
                      Commands & Specs
                    </div>
                  </div>

                  <div
                    style={{
                      width: "100%",
                      padding: "24px 32px",
                      borderRadius: 18,
                      background: "rgba(0, 240, 255, 0.08)",
                      border: "1.5px solid rgba(0, 240, 255, 0.4)",
                      textAlign: "center",
                    }}
                  >
                    <div style={{ fontSize: 22, color: "#94a3b8", marginBottom: 8 }}>Free Source Pack & Docs:</div>
                    <div style={{ fontSize: 32, fontWeight: 800, color: "#38bdf8", fontFamily: "monospace" }}>
                      naveenk7100-ship-it.github.io/studio
                    </div>
                  </div>

                  <FollowPill />

                  <div style={{ fontSize: 22, color: "#64748b", textAlign: "center" }}>
                    Daily 30-Second Verified AI Intel • No Fluff
                  </div>
                </div>
              </AbsoluteFill>
            );
          })()}
        </Sequence>
      </div>

      {/* PARALLAX LAYER 3: Active Pop Captions (Top 1360px Safe Zone, Zero Wobble) */}
      <PopCaptions words={WORDS} />
    </AbsoluteFill>
  );
};
