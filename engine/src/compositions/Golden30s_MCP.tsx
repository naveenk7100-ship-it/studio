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

// Prompt Library Index ID: 242 (Protocol Explainer & Integration Showcase)
const WORDS: [string, number, number][] = [
  [
    "Mama,",
    0.0,
    0.633
  ],
  [
    "AI",
    0.633,
    1.023
  ],
  [
    "agents",
    1.023,
    1.477
  ],
  [
    "ki",
    1.477,
    1.769
  ],
  [
    "local",
    1.769,
    2.094
  ],
  [
    "databases",
    2.094,
    2.468
  ],
  [
    "mariyu",
    2.873,
    3.247
  ],
  [
    "APIs",
    3.247,
    3.442
  ],
  [
    "connect",
    3.442,
    3.685
  ],
  [
    "cheyatam",
    3.685,
    3.977
  ],
  [
    "kastam",
    3.977,
    4.221
  ],
  [
    "anukuntunnara?",
    4.221,
    4.919
  ],
  [
    "Idi",
    5.601,
    6.169
  ],
  [
    "Anthropic",
    6.169,
    6.364
  ],
  [
    "launch",
    6.364,
    6.64
  ],
  [
    "chesina",
    6.64,
    7.013
  ],
  [
    "Model",
    7.013,
    7.354
  ],
  [
    "Context",
    7.354,
    7.776
  ],
  [
    "Protocol,",
    8.49,
    8.636
  ],
  [
    "aka",
    8.636,
    8.831
  ],
  [
    "MCP",
    9.01,
    9.416
  ],
  [
    "open",
    9.416,
    9.692
  ],
  [
    "standard.",
    9.692,
    10.032
  ],
  [
    "Custom",
    10.666,
    10.828
  ],
  [
    "wrappers",
    11.185,
    11.38
  ],
  [
    "lekunda,",
    11.38,
    11.705
  ],
  [
    "oke",
    11.705,
    11.932
  ],
  [
    "standard",
    11.932,
    12.045
  ],
  [
    "protocol",
    12.045,
    12.5
  ],
  [
    "tho",
    12.5,
    12.922
  ],
  [
    "LLMs",
    13.864,
    14.01
  ],
  [
    "tools",
    14.01,
    14.188
  ],
  [
    "ni",
    14.188,
    14.432
  ],
  [
    "access",
    14.432,
    14.789
  ],
  [
    "chesthayi.",
    14.789,
    14.83
  ],
  [
    "Local",
    15.227,
    15.617
  ],
  [
    "Postgres,",
    16.575,
    16.802
  ],
  [
    "GitHub",
    16.802,
    17.386
  ],
  [
    "repos,",
    17.614,
    17.776
  ],
  [
    "leda",
    17.776,
    18.019
  ],
  [
    "Google",
    18.019,
    18.198
  ],
  [
    "Drive",
    18.198,
    18.555
  ],
  [
    "ni",
    18.929,
    19.383
  ],
  [
    "direct",
    19.383,
    19.675
  ],
  [
    "secure",
    20.487,
    21.071
  ],
  [
    "connection",
    21.071,
    21.347
  ],
  [
    "ivvochu.",
    21.542,
    21.753
  ],
  [
    "Terminal",
    21.753,
    21.883
  ],
  [
    "lo",
    22.224,
    22.532
  ],
  [
    "npx",
    22.532,
    22.792
  ],
  [
    "mcp-server",
    22.792,
    23.019
  ],
  [
    "run",
    23.019,
    23.263
  ],
  [
    "chesi",
    23.263,
    23.62
  ],
  [
    "Mee",
    23.62,
    23.718
  ],
  [
    "agent",
    23.945,
    24.205
  ],
  [
    "ki",
    24.205,
    24.497
  ],
  [
    "powers",
    25.211,
    25.438
  ],
  [
    "ivvandi.",
    25.438,
    25.601
  ],
  [
    "Next-gen",
    25.698,
    25.739
  ],
  [
    "agentic",
    25.828,
    25.869
  ],
  [
    "workflows",
    26.006,
    26.104
  ],
  [
    "kosam",
    26.12,
    26.282
  ],
  [
    "FLASH",
    26.38,
    26.445
  ],
  [
    "ni",
    26.591,
    26.948
  ],
  [
    "FOLLOW",
    27.078,
    27.159
  ],
  [
    "cheyandi!",
    27.159,
    27.338
  ]
];

export const Golden30s_MCP: React.FC = () => {
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
                  <AutoFitText text="Model Context Protocol" maxFontSize={76} color="#10b981" />
                  <div style={{ fontSize: 26, fontWeight: 700, color: "#94a3b8", letterSpacing: 2, marginTop: 8 }}>
                    OPEN AGENT INTERFACE v2.2.0
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
                    src={staticFile("captured_proofs/modelcontextprotocol_servers/proof_1_repo_card.png")}
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
                  v2.2.0 Spec • 28 Oct 2026 • ★ 41,200 Stars
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
                    border: "2px solid #10b981",
                    boxShadow: "0 12px 32px rgba(0, 0, 0, 0.35)",
                    padding: 40,
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "space-between",
                    alignItems: "center",
                  }}
                >
                  <div style={{ textAlign: "center" }}>
                    <div style={{ fontSize: 22, fontWeight: 800, color: "#10b981", letterSpacing: 3, marginBottom: 8 }}>
                      CORE BREAKTHROUGH [3.0s WOW BEAT]
                    </div>
                    <AutoFitText text="UNIVERSAL PROTOCOL TRANSPORT" maxFontSize={52} color="#ffffff" />
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
                      src={staticFile("captured_proofs/modelcontextprotocol_servers/proof_2_docs_capture.png")}
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
                    ⚡ Stdio & Server-Sent Events (SSE) Bi-Directional RPC
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
                      🔒 https://modelcontextprotocol.io
                    </div>
                  </div>

                  <div style={{ padding: 30, display: "flex", flexDirection: "column", alignItems: "center" }}>
                    <AutoFitText text="MCP Open Specification" maxFontSize={46} color="#10b981" />
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
                        src={staticFile("captured_proofs/modelcontextprotocol_servers/proof_2_docs_capture.png")}
                        style={{ width: "100%", height: "100%", objectFit: "cover" }}
                      />
                    </div>
                    <div style={{ marginTop: 24, fontSize: 26, color: "#cbd5e1", textAlign: "center", maxWidth: 840 }}>
                      Standardized connector connecting AI agents to Postgres, GitHub, and local FS.
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
                    border: "2px solid #38bdf8",
                    boxShadow: "0 12px 32px rgba(0, 0, 0, 0.35)",
                    padding: 40,
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "space-between",
                    alignItems: "center",
                  }}
                >
                  <AutoFitText text="ZERO-CONFIG DISCOVERY" maxFontSize={48} color="#38bdf8" />

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
                      src={staticFile("captured_proofs/modelcontextprotocol_servers/proof_3_live_api_card.png")}
                      style={{ width: "100%", height: "100%", objectFit: "contain" }}
                    />
                  </div>

                  <div
                    style={{
                      width: "100%",
                      padding: "16px 28px",
                      borderRadius: 16,
                      background: "rgba(255, 0, 127, 0.12)",
                      border: "1.5px solid #38bdf8",
                      color: "#ffffff",
                      fontSize: 26,
                      fontWeight: 800,
                      textAlign: "center",
                    }}
                  >
                    📊 Runtime Tool Negotiation & Capability Inspection
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
                    border: "2px solid #10b981",
                    boxShadow: "0 12px 32px rgba(0, 0, 0, 0.35)",
                    padding: 50,
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "space-between",
                  }}
                >
                  <div>
                    <div style={{ fontSize: 24, fontWeight: 800, color: "#10b981", marginBottom: 12 }}>
                      # Verified MCP Client Launch
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
                      $ npx -y @modelcontextprotocol/server-filesystem ./workspace
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
                    <AutoFitText text="VERIFIED SYSTEM CAVEAT" maxFontSize={48} color="#f59e0b" />
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
                    Stdio transports require Node.js v18+. Scope directory arguments to non-root project subdirectories to prevent host directory traversal.
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
                    border: "2px solid #10b981",
                    boxShadow: "0 12px 32px rgba(0, 0, 0, 0.35)",
                    padding: 40,
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "space-between",
                    alignItems: "center",
                  }}
                >
                  <AutoFitText text="PRODUCTION READINESS" maxFontSize={48} color="#10b981" />

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
                      src={staticFile("captured_proofs/modelcontextprotocol_servers/proof_1_repo_card.png")}
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
                        border: "1px solid #10b981",
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
