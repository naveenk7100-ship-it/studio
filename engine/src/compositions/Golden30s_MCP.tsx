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
              text="MODEL CONTEXT PROTOCOL"
              maxFontSize={84}
              color="#10b981"
              style={{ filter: "drop-shadow(0 0 35px rgba(0, 240, 255, 0.4))" }}
            />
            <div
              style={{
                marginTop: 30,
                width: 960,
                height: 520,
                borderRadius: 24,
                overflow: "hidden",
                border: "2px solid #10b981",
                boxShadow: "0 25px 60px rgba(0, 0, 0, 0.9)",
              }}
            >
              <Img
                src={staticFile("captured_proofs/modelcontextprotocol_servers/proof_1_repo_card.png")}
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
            <BrowserMockup3D url="https://modelcontextprotocol.io" title="MCP Protocol Specification">
              <div style={{ padding: 25, display: "flex", flexDirection: "column", alignItems: "center" }}>
                <AutoFitText text="Universal AI Interface" maxFontSize={46} color="#ffd700" />
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
                    src={staticFile("captured_proofs/modelcontextprotocol_servers/proof_2_docs_capture.png")}
                    style={{
                      width: "100%",
                      height: "100%",
                      objectFit: "cover",
                      transform: `scale(${interpolate(frame - 60, [0, 180], [1.0, 1.06])})`,
                    }}
                  />
                </div>
                <div style={{ marginTop: 20, color: "#8892b0", fontSize: 28, textAlign: "center" }}>
                  Open standard connecting LLMs to databases, tools, and local repos.
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
                border: "2px solid #38bdf8",
                boxShadow: "0 35px 80px rgba(0, 0, 0, 0.95), 0 0 50px rgba(255, 0, 127, 0.3)",
                padding: 40,
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
                alignItems: "center",
              }}
            >
              <AutoFitText text="ZERO-CONFIG TOOL DISCOVERY" maxFontSize={46} color="#38bdf8" />
              
              <div
                style={{
                  width: 860,
                  height: 520,
                  borderRadius: 18,
                  overflow: "hidden",
                  border: "2px solid #10b981",
                }}
              >
                <Img
                  src={staticFile("captured_proofs/modelcontextprotocol_servers/proof_3_live_api_card.png")}
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
                ✓ 41,200 Stars • Stdio & SSE Two-Way Protocol Transport
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
                border: "2px solid #10b981",
                boxShadow: "0 35px 80px rgba(0, 0, 0, 0.95), 0 0 50px rgba(0, 240, 255, 0.4)",
                padding: 55,
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
              }}
            >
              <div style={{ color: "#ffd700", fontSize: 38, fontWeight: 700, marginBottom: 20 }}>
                # Verified MCP Client Launch
              </div>
              <div
                style={{
                  fontFamily: "'Courier New', monospace",
                  fontSize: 40,
                  fontWeight: 700,
                  color: "#10b981",
                  lineHeight: 1.6,
                  wordBreak: "break-all",
                  background: "rgba(0, 0, 0, 0.6)",
                  padding: 25,
                  borderRadius: 16,
                  border: "1.5px solid rgba(0, 240, 255, 0.3)",
                }}
              >
                npx -y @modelcontextprotocol/server-filesystem ./workspace
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
                ⚠️ Caveat: Requires Node.js v18+. For remote transports, configure Bearer Auth.
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
              text="Released: 28 Oct 2026 (v2.2.0 Specification)"
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
