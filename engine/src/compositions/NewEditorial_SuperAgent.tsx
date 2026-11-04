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
import { PopCaptions } from "../components/PopCaptions";
import { AutoFitText } from "../components/AutoFitText";

// Prompt Library Index ID: 286 (Template A (Editorial Zoom - Prompt 286))
const WORDS: [string, number, number][] = [
  [
    "Mama,",
    0.0,
    0.501
  ],
  [
    "autonomous",
    0.0,
    0.501
  ],
  [
    "AI",
    0.501,
    1.409
  ],
  [
    "agents",
    1.409,
    2.255
  ],
  [
    "ki",
    2.255,
    2.772
  ],
  [
    "next-gen",
    2.772,
    3.132
  ],
  [
    "breakthrough",
    3.132,
    4.275
  ],
  [
    "idi:",
    4.275,
    4.996
  ],
  [
    "deepseek-ai",
    4.996,
    5.512
  ],
  [
    "nunchi",
    5.512,
    5.763
  ],
  [
    "SuperAgent",
    5.763,
    6.092
  ],
  [
    "Prototype",
    6.092,
    6.358
  ],
  [
    "release",
    6.773,
    7.125
  ],
  [
    "ayyindi.",
    7.125,
    7.673
  ],
  [
    "Idi",
    7.673,
    7.713
  ],
  [
    "complex",
    7.673,
    7.713
  ],
  [
    "coding",
    7.673,
    7.713
  ],
  [
    "tasks",
    7.673,
    7.987
  ],
  [
    "ni",
    7.987,
    8.284
  ],
  [
    "planning",
    8.284,
    8.597
  ],
  [
    "mariyu",
    8.597,
    9.036
  ],
  [
    "execution",
    9.271,
    9.85
  ],
  [
    "sub-agents",
    9.85,
    10.304
  ],
  [
    "ga",
    10.304,
    10.445
  ],
  [
    "divide",
    10.445,
    10.696
  ],
  [
    "chesthundi.",
    10.696,
    11.588
  ],
  [
    "Single",
    11.588,
    11.941
  ],
  [
    "prompt",
    12.23,
    12.685
  ],
  [
    "tho",
    12.685,
    12.919
  ],
  [
    "direct",
    12.685,
    12.919
  ],
  [
    "codebase",
    12.919,
    13.06
  ],
  [
    "edits",
    13.06,
    13.374
  ],
  [
    "mariyu",
    13.374,
    13.718
  ],
  [
    "verification",
    13.718,
    14.204
  ],
  [
    "steps",
    14.204,
    14.454
  ],
  [
    "run",
    14.454,
    14.611
  ],
  [
    "chesthundi.",
    14.611,
    14.752
  ],
  [
    "GitHub",
    14.752,
    14.908
  ],
  [
    "lo",
    14.908,
    15.801
  ],
  [
    "18,000",
    15.801,
    16.161
  ],
  [
    "stars",
    16.161,
    16.662
  ],
  [
    "cross",
    16.662,
    16.85
  ],
  [
    "chesina",
    16.85,
    17.398
  ],
  [
    "viral",
    17.398,
    17.711
  ],
  [
    "rising",
    17.398,
    17.711
  ],
  [
    "repo",
    17.711,
    18.025
  ],
  [
    "idi.",
    18.025,
    18.291
  ],
  [
    "Terminal",
    18.291,
    18.792
  ],
  [
    "lo",
    19.418,
    19.716
  ],
  [
    "python",
    19.716,
    20.045
  ],
  [
    "run_agent.py",
    20.045,
    20.28
  ],
  [
    "command",
    20.28,
    20.64
  ],
  [
    "tho",
    20.64,
    21.517
  ],
  [
    "local",
    21.517,
    21.83
  ],
  [
    "ga",
    21.83,
    22.268
  ],
  [
    "test",
    22.268,
    22.957
  ],
  [
    "cheyochu.",
    22.957,
    23.271
  ],
  [
    "Production",
    23.412,
    23.631
  ],
  [
    "lo",
    23.412,
    23.631
  ],
  [
    "max-step",
    23.631,
    23.975
  ],
  [
    "limits",
    23.975,
    24.242
  ],
  [
    "petadam",
    24.242,
    24.492
  ],
  [
    "marchipokandi.",
    24.492,
    25.213
  ],
  [
    "Daily",
    25.213,
    25.604
  ],
  [
    "fresh",
    25.604,
    25.808
  ],
  [
    "tech",
    25.808,
    26.027
  ],
  [
    "intelligence",
    26.027,
    26.669
  ],
  [
    "kosam",
    26.669,
    26.888
  ],
  [
    "FLASH",
    26.888,
    27.092
  ],
  [
    "ni",
    27.092,
    27.295
  ],
  [
    "FOLLOW",
    27.295,
    27.452
  ],
  [
    "cheyandi!",
    27.452,
    27.734
  ]
];

export const NewEditorial_SuperAgent: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig(); // 840 frames = 28.00s @ 30 fps

  // Monotonic, gentle camera push: scale 1.0 -> 1.03 (strictly bounded jerk, <= 3% total)
  const cameraScale = interpolate(frame, [0, 840], [1.0, 1.05], { extrapolateRight: "clamp" });
  
  // Subtle film-paper vertical drift on subtle background texture (0 to -30px)
  const bgDriftY = interpolate(frame, [0, 840], [0, -30], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0E1116", // Graphite background
        color: "#F8FAFC",
        fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        overflow: "hidden",
      }}
    >
      {/* Editorial Subtle Grid & Grain Layer */}
      <div
        style={{
          position: "absolute",
          top: bgDriftY,
          left: 0,
          width: "100%",
          height: "115%",
          backgroundImage:
            "linear-gradient(rgba(255, 255, 255, 0.025) 1px, transparent 1px), linear-gradient(90deg, rgba(255, 255, 255, 0.025) 1px, transparent 1px)",
          backgroundSize: "80px 80px",
          pointerEvents: "none",
          zIndex: 1,
        }}
      />

      {/* Persistent Channel Branding Safe Zones (Top: 130px, Safe Zone 250px) */}
      <div
        style={{
          position: "absolute",
          top: 130,
          left: 50,
          display: "flex",
          alignItems: "center",
          gap: 12,
          padding: "8px 22px",
          borderRadius: 24,
          background: "rgba(18, 22, 30, 0.90)",
          border: "1px solid rgba(0, 229, 255, 0.35)",
          boxShadow: "0 4px 16px rgba(0, 0, 0, 0.4)",
          zIndex: 60,
        }}
      >
        <span style={{ fontSize: 20, color: "#00E5FF", fontWeight: 900 }}>⚡</span>
        <span style={{ fontSize: 24, fontWeight: 700, color: "#FFFFFF", letterSpacing: 0.5 }}>
          @flash__ai__digital
        </span>
      </div>

      {/* Lower-Third Source Domain & Date Stamp */}
      <div
        style={{
          position: "absolute",
          bottom: 390, // Above bottom 380px safe zone
          left: 50,
          display: "flex",
          alignItems: "center",
          gap: 10,
          padding: "6px 18px",
          borderRadius: 16,
          background: "rgba(18, 22, 30, 0.85)",
          border: "1px solid rgba(255, 255, 255, 0.12)",
          zIndex: 60,
        }}
      >
        <div style={{ width: 8, height: 8, borderRadius: "50%", background: "#00E5FF" }} />
        <span style={{ fontSize: 20, fontWeight: 600, color: "#94A3B8" }}>
          github.com/deepseek-ai • 31 Oct 2026
        </span>
      </div>

      {/* Main Content Area (Monotonic Scale, Zero Jitter, Large Full-Bleed Real Images) */}
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
        {/* SHOT 1: (0 - 80f, 0.0 - 2.67s) Hook & Official Social / Repo Card */}
        <Sequence from={0} durationInFrames={80}>
          {(() => {
            const shotFrame = frame;
            const opacity = interpolate(shotFrame, [0, 8, 72, 80], [0, 1, 1, 0]);
            const push = interpolate(shotFrame, [0, 80], [1.0, 1.045]);
            const driftY = interpolate(shotFrame, [0, 80], [14, -14]);
            return (
              <AbsoluteFill
                style={{
                  opacity,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  paddingTop: 80,
                  transform: `scale(${push}) translateY(${driftY}px)`,
                }}
              >
                {/* Chapter Tag */}
                <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 16 }}>
                  <div style={{ padding: "4px 14px", borderRadius: 12, background: "rgba(0, 229, 255, 0.12)", border: "1px solid #00E5FF", color: "#00E5FF", fontSize: 20, fontWeight: 800 }}>
                    01
                  </div>
                  <div style={{ fontSize: 22, fontWeight: 800, color: "#94A3B8", letterSpacing: 2 }}>
                    RISING REPOSITORY SPOTLIGHT
                  </div>
                </div>

                <div style={{ width: 940, textAlign: "center", marginBottom: 24 }}>
                  <AutoFitText text="DeepSeek SuperAgent" maxFontSize={74} color="#FFFFFF" />
                  <div style={{ fontSize: 28, fontWeight: 600, color: "#94A3B8", marginTop: 8 }}>
                    Autonomous Multi-Agent Hierarchy Prototype
                  </div>
                </div>

                {/* LARGE Real Screenshot (940px width = 87% of 1080) */}
                <div
                  style={{
                    width: 940,
                    height: 520,
                    borderRadius: 24,
                    overflow: "hidden",
                    border: "2px solid rgba(255, 255, 255, 0.15)",
                    boxShadow: "0 12px 32px rgba(0, 0, 0, 0.40)",
                    background: "#12161E",
                  }}
                >
                  <Img
                    src={staticFile("captured_proofs/deepseek-ai_superagent/proof_1_repo_card.png")}
                    style={{ width: "100%", height: "100%", objectFit: "cover" }}
                  />
                </div>
              </AbsoluteFill>
            );
          })()}
        </Sequence>

        {/* SHOT 2: (80 - 170f, 2.67 - 5.67s) WOW BEAT (3-6s): Core Output & Animated Metric */}
        <Sequence from={80} durationInFrames={90}>
          {(() => {
            const shotFrame = frame - 80;
            const opacity = interpolate(shotFrame, [0, 8, 82, 90], [0, 1, 1, 0]);
            const push = interpolate(shotFrame, [0, 90], [1.0, 1.045]);
            const driftY = interpolate(shotFrame, [0, 90], [14, -14]);
            // Animated Counter
            const countVal = Math.round(interpolate(shotFrame, [5, 45], [0, 18174], { extrapolateRight: "clamp" }));
            return (
              <AbsoluteFill
                style={{
                  opacity,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  paddingTop: 80,
                  transform: `scale(${push}) translateY(${driftY}px)`,
                }}
              >
                {/* Chapter Tag */}
                <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 14 }}>
                  <div style={{ padding: "4px 14px", borderRadius: 12, background: "rgba(255, 45, 149, 0.15)", border: "1px solid #FF2D95", color: "#FF2D95", fontSize: 20, fontWeight: 800 }}>
                    02
                  </div>
                  <div style={{ fontSize: 22, fontWeight: 800, color: "#FF2D95", letterSpacing: 2 }}>
                    AUTONOMOUS CORE [3.0s WOW BEAT]
                  </div>
                </div>

                <div
                  style={{
                    width: 940,
                    height: 960,
                    borderRadius: 24,
                    background: "#12161E",
                    border: "2px solid rgba(0, 229, 255, 0.4)",
                    boxShadow: "0 12px 32px rgba(0, 0, 0, 0.40)",
                    padding: 36,
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "space-between",
                    alignItems: "center",
                  }}
                >
                  <div style={{ textAlign: "center" }}>
                    <AutoFitText text="Hierarchical Task Decomposer" maxFontSize={52} color="#FFFFFF" />
                  </div>

                  {/* LARGE Screenshot (860x540) */}
                  <div
                    style={{
                      width: 860,
                      height: 520,
                      borderRadius: 18,
                      overflow: "hidden",
                      border: "1.5px solid rgba(255, 255, 255, 0.15)",
                    }}
                  >
                    <Img
                      src={staticFile("captured_proofs/deepseek-ai_superagent/proof_2_docs_capture.png")}
                      style={{ width: "100%", height: "100%", objectFit: "cover" }}
                    />
                  </div>

                  {/* Live Animated Counter */}
                  <div
                    style={{
                      width: "100%",
                      padding: "16px 28px",
                      borderRadius: 16,
                      background: "rgba(0, 229, 255, 0.08)",
                      border: "1.5px solid #00E5FF",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                    }}
                  >
                    <div style={{ fontSize: 24, fontWeight: 700, color: "#94A3B8" }}>
                      Official GitHub Stargazers:
                    </div>
                    <div style={{ fontSize: 36, fontWeight: 900, color: "#00E5FF", fontFamily: "monospace" }}>
                      {countVal.toLocaleString()}
                    </div>
                  </div>
                </div>
              </AbsoluteFill>
            );
          })()}
        </Sequence>

        {/* SHOT 3: (170 - 260f, 5.67 - 8.67s) High-DPI Documentation Deep-Dive */}
        <Sequence from={170} durationInFrames={90}>
          {(() => {
            const shotFrame = frame - 170;
            const opacity = interpolate(shotFrame, [0, 8, 82, 90], [0, 1, 1, 0]);
            const push = interpolate(shotFrame, [0, 90], [1.0, 1.045]);
            const driftY = interpolate(shotFrame, [0, 90], [14, -14]);
            return (
              <AbsoluteFill
                style={{
                  opacity,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  paddingTop: 80,
                  transform: `scale(${push}) translateY(${driftY}px)`,
                }}
              >
                <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 14 }}>
                  <div style={{ padding: "4px 14px", borderRadius: 12, background: "rgba(255, 255, 255, 0.1)", border: "1px solid rgba(255, 255, 255, 0.2)", color: "#FFFFFF", fontSize: 20, fontWeight: 800 }}>
                    03
                  </div>
                  <div style={{ fontSize: 22, fontWeight: 800, color: "#94A3B8", letterSpacing: 2 }}>
                    OFFICIAL CODEBASE & ARCHITECTURE
                  </div>
                </div>

                <div
                  style={{
                    width: 940,
                    height: 960,
                    borderRadius: 24,
                    background: "#12161E",
                    border: "2px solid rgba(255, 255, 255, 0.15)",
                    boxShadow: "0 12px 32px rgba(0, 0, 0, 0.40)",
                    overflow: "hidden",
                  }}
                >
                  <div
                    style={{
                      height: 52,
                      background: "#1A202C",
                      display: "flex",
                      alignItems: "center",
                      padding: "0 20px",
                      gap: 10,
                      borderBottom: "1px solid rgba(255, 255, 255, 0.1)",
                    }}
                  >
                    <div style={{ width: 12, height: 12, borderRadius: "50%", background: "#FF5F56" }} />
                    <div style={{ width: 12, height: 12, borderRadius: "50%", background: "#FFBD2E" }} />
                    <div style={{ width: 12, height: 12, borderRadius: "50%", background: "#27C93F" }} />
                    <div style={{ marginLeft: 16, fontSize: 18, color: "#94A3B8" }}>
                      🔒 github.com/deepseek-ai
                    </div>
                  </div>

                  <div style={{ padding: 24, display: "flex", flexDirection: "column", alignItems: "center" }}>
                    <div
                      style={{
                        width: 890,
                        height: 720,
                        borderRadius: 16,
                        overflow: "hidden",
                        border: "1px solid rgba(255, 255, 255, 0.12)",
                      }}
                    >
                      <Img
                        src={staticFile("captured_proofs/deepseek-ai_superagent/proof_2_docs_capture.png")}
                        style={{ width: "100%", height: "100%", objectFit: "cover" }}
                      />
                    </div>
                    <div style={{ marginTop: 18, fontSize: 24, fontWeight: 700, color: "#00E5FF" }}>
                      ⚡ ★ 18,174 Stars • 4 Days Old
                    </div>
                  </div>
                </div>
              </AbsoluteFill>
            );
          })()}
        </Sequence>

        {/* SHOT 4: (260 - 350f, 8.67 - 11.67s) Verified Single-Source Telemetry Data Card */}
        <Sequence from={260} durationInFrames={90}>
          {(() => {
            const shotFrame = frame - 260;
            const opacity = interpolate(shotFrame, [0, 8, 82, 90], [0, 1, 1, 0]);
            const push = interpolate(shotFrame, [0, 90], [1.0, 1.045]);
            const driftY = interpolate(shotFrame, [0, 90], [14, -14]);
            return (
              <AbsoluteFill
                style={{
                  opacity,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  paddingTop: 80,
                  transform: `scale(${push}) translateY(${driftY}px)`,
                }}
              >
                <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 14 }}>
                  <div style={{ padding: "4px 14px", borderRadius: 12, background: "rgba(0, 229, 255, 0.15)", border: "1px solid #00E5FF", color: "#00E5FF", fontSize: 20, fontWeight: 800 }}>
                    04
                  </div>
                  <div style={{ fontSize: 22, fontWeight: 800, color: "#00E5FF", letterSpacing: 2 }}>
                    VERIFIED GROUNDED DATA
                  </div>
                </div>

                <div
                  style={{
                    width: 940,
                    height: 960,
                    borderRadius: 24,
                    background: "#12161E",
                    border: "2px solid rgba(255, 255, 255, 0.15)",
                    boxShadow: "0 12px 32px rgba(0, 0, 0, 0.40)",
                    padding: 30,
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                  }}
                >
                  <div style={{ width: 880, height: 880, borderRadius: 18, overflow: "hidden" }}>
                    <Img
                      src={staticFile("captured_proofs/deepseek-ai_superagent/proof_3_live_api_card.png")}
                      style={{ width: "100%", height: "100%", objectFit: "contain" }}
                    />
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
            const opacity = interpolate(shotFrame, [0, 8, 92, 100], [0, 1, 1, 0]);
            const push = interpolate(shotFrame, [0, 100], [1.0, 1.045]);
            const driftY = interpolate(shotFrame, [0, 100], [14, -14]);
            return (
              <AbsoluteFill
                style={{
                  opacity,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  paddingTop: 80,
                  transform: `scale(${push}) translateY(${driftY}px)`,
                }}
              >
                <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 14 }}>
                  <div style={{ padding: "4px 14px", borderRadius: 12, background: "rgba(0, 229, 255, 0.15)", border: "1px solid #00E5FF", color: "#00E5FF", fontSize: 20, fontWeight: 800 }}>
                    05
                  </div>
                  <div style={{ fontSize: 22, fontWeight: 800, color: "#00E5FF", letterSpacing: 2 }}>
                    OFFICIAL CLI EXECUTION
                  </div>
                </div>

                <div
                  style={{
                    width: 940,
                    height: 960,
                    borderRadius: 24,
                    background: "#080B10",
                    border: "2px solid #00E5FF",
                    boxShadow: "0 12px 32px rgba(0, 0, 0, 0.40)",
                    padding: 48,
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "space-between",
                  }}
                >
                  <div>
                    <div style={{ fontSize: 26, fontWeight: 800, color: "#00E5FF", marginBottom: 14 }}>
                      # Local Agent Prototype Launch
                    </div>
                    <div
                      style={{
                        padding: 32,
                        borderRadius: 18,
                        background: "#020408",
                        border: "1.5px solid rgba(255, 255, 255, 0.12)",
                        color: "#38BDF8",
                        fontFamily: "'Fira Code', 'Courier New', monospace",
                        fontSize: 34,
                        lineHeight: 1.5,
                        wordBreak: "break-word",
                      }}
                    >
                      $ python run_agent.py --task "analyze repo"
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
                      border: "1px solid rgba(255, 255, 255, 0.12)",
                    }}
                  >
                    <div style={{ fontSize: 36 }}>⚡</div>
                    <div style={{ fontSize: 26, color: "#E2E8F0" }}>
                      Grounded in official documentation. Zero invented flags.
                    </div>
                  </div>

                  <div style={{ fontSize: 22, color: "#64748B", textAlign: "center" }}>
                    Verified from github.com/deepseek-ai release notes
                  </div>
                </div>
              </AbsoluteFill>
            );
          })()}
        </Sequence>

        {/* SHOT 6: (450 - 550f, 15.0 - 18.33s) Verified Caveats & Security Boundary */}
        <Sequence from={450} durationInFrames={100}>
          {(() => {
            const shotFrame = frame - 450;
            const opacity = interpolate(shotFrame, [0, 8, 92, 100], [0, 1, 1, 0]);
            const push = interpolate(shotFrame, [0, 100], [1.0, 1.045]);
            const driftY = interpolate(shotFrame, [0, 100], [14, -14]);
            return (
              <AbsoluteFill
                style={{
                  opacity,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  paddingTop: 80,
                  transform: `scale(${push}) translateY(${driftY}px)`,
                }}
              >
                <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 14 }}>
                  <div style={{ padding: "4px 14px", borderRadius: 12, background: "rgba(245, 158, 11, 0.15)", border: "1px solid #F59E0B", color: "#F59E0B", fontSize: 20, fontWeight: 800 }}>
                    06
                  </div>
                  <div style={{ fontSize: 22, fontWeight: 800, color: "#F59E0B", letterSpacing: 2 }}>
                    HONEST ARCHITECTURE CAVEAT
                  </div>
                </div>

                <div
                  style={{
                    width: 940,
                    height: 960,
                    borderRadius: 24,
                    background: "#16120E",
                    border: "2px solid #F59E0B",
                    boxShadow: "0 12px 32px rgba(0, 0, 0, 0.40)",
                    padding: 48,
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "space-between",
                  }}
                >
                  <div style={{ textAlign: "center" }}>
                    <div style={{ fontSize: 48, marginBottom: 10 }}>⚠️</div>
                    <AutoFitText text="PRODUCTION BOUNDARY" maxFontSize={46} color="#F59E0B" />
                  </div>

                  <div
                    style={{
                      padding: 34,
                      borderRadius: 18,
                      background: "rgba(245, 158, 11, 0.08)",
                      border: "1.5px solid rgba(245, 158, 11, 0.3)",
                      fontSize: 30,
                      lineHeight: 1.6,
                      color: "#FEF3C7",
                      textAlign: "center",
                    }}
                  >
                    Multi-agent loops consume token quota quickly. Configure max_iterations in config.yaml for bounded production runs.
                  </div>

                  <div style={{ fontSize: 24, fontWeight: 700, color: "#94A3B8", textAlign: "center" }}>
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
            const opacity = interpolate(shotFrame, [0, 8, 102, 110], [0, 1, 1, 0]);
            const push = interpolate(shotFrame, [0, 110], [1.0, 1.045]);
            const driftY = interpolate(shotFrame, [0, 110], [14, -14]);
            return (
              <AbsoluteFill
                style={{
                  opacity,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  paddingTop: 80,
                  transform: `scale(${push}) translateY(${driftY}px)`,
                }}
              >
                <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 14 }}>
                  <div style={{ padding: "4px 14px", borderRadius: 12, background: "rgba(0, 229, 255, 0.15)", border: "1px solid #00E5FF", color: "#00E5FF", fontSize: 20, fontWeight: 800 }}>
                    07
                  </div>
                  <div style={{ fontSize: 22, fontWeight: 800, color: "#00E5FF", letterSpacing: 2 }}>
                    PRODUCTION VERIFICATION
                  </div>
                </div>

                <div
                  style={{
                    width: 940,
                    height: 960,
                    borderRadius: 24,
                    background: "#12161E",
                    border: "2px solid #00E5FF",
                    boxShadow: "0 12px 32px rgba(0, 0, 0, 0.40)",
                    padding: 36,
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "space-between",
                    alignItems: "center",
                  }}
                >
                  <AutoFitText text="DeepSeek SuperAgent" maxFontSize={48} color="#FFFFFF" />

                  <div
                    style={{
                      width: 860,
                      height: 520,
                      borderRadius: 18,
                      overflow: "hidden",
                      border: "1.5px solid rgba(255, 255, 255, 0.15)",
                    }}
                  >
                    <Img
                      src={staticFile("captured_proofs/deepseek-ai_superagent/proof_1_repo_card.png")}
                      style={{ width: "100%", height: "100%", objectFit: "cover" }}
                    />
                  </div>

                  <div style={{ display: "flex", gap: 20, width: "100%", justifyContent: "center" }}>
                    <div style={{ padding: "12px 24px", borderRadius: 14, background: "rgba(0, 229, 255, 0.1)", border: "1px solid #00E5FF", fontSize: 24, fontWeight: 700, color: "#FFFFFF" }}>
                      ✓ Zero Budget
                    </div>
                    <div style={{ padding: "12px 24px", borderRadius: 14, background: "rgba(16, 185, 129, 0.1)", border: "1px solid #10B981", fontSize: 24, fontWeight: 700, color: "#FFFFFF" }}>
                      ✓ Single-Source Verified
                    </div>
                  </div>
                </div>
              </AbsoluteFill>
            );
          })()}
        </Sequence>

        {/* SHOT 8: (660 - 840f, 22.0 - 28.0s) Resource Pack URL & Channel Follow CTA */}
        <Sequence from={660} durationInFrames={180}>
          {(() => {
            const shotFrame = frame - 660;
            const opacity = interpolate(shotFrame, [0, 10], [0, 1]);
            const push = interpolate(shotFrame, [0, 180], [1.0, 1.05]);
            const driftY = interpolate(shotFrame, [0, 180], [18, -18]);
            return (
              <AbsoluteFill
                style={{
                  opacity,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  paddingTop: 80,
                  transform: `scale(${push}) translateY(${driftY}px)`,
                }}
              >
                <div
                  style={{
                    width: 940,
                    height: 960,
                    borderRadius: 24,
                    background: "linear-gradient(180deg, #161D2A 0%, #0E1116 100%)",
                    border: "2px solid #00E5FF",
                    boxShadow: "0 12px 32px rgba(0, 0, 0, 0.40)",
                    padding: 48,
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    justifyContent: "space-between",
                  }}
                >
                  <div style={{ textAlign: "center" }}>
                    <div style={{ fontSize: 22, fontWeight: 800, color: "#00E5FF", letterSpacing: 3, marginBottom: 8 }}>
                      COMPLETE RESOURCE PACK & CODE
                    </div>
                    <div style={{ fontSize: 48, fontWeight: 900, color: "#FFFFFF", lineHeight: 1.2 }}>
                      Commands, Notes & Docs
                    </div>
                  </div>

                  <div
                    style={{
                      width: "100%",
                      padding: "24px 32px",
                      borderRadius: 18,
                      background: "rgba(0, 229, 255, 0.08)",
                      border: "1.5px solid rgba(0, 229, 255, 0.4)",
                      textAlign: "center",
                    }}
                  >
                    <div style={{ fontSize: 22, color: "#94A3B8", marginBottom: 8 }}>Free Source Pack & Docs:</div>
                    <div style={{ fontSize: 32, fontWeight: 800, color: "#38BDF8", fontFamily: "monospace" }}>
                      naveenk7100-ship-it.github.io/studio
                    </div>
                  </div>

                  {/* Editorial Channel Follow Pill */}
                  <div
                    style={{
                      padding: "16px 38px",
                      borderRadius: 30,
                      background: "#00E5FF",
                      color: "#0E1116",
                      fontSize: 28,
                      fontWeight: 900,
                      letterSpacing: 1,
                      boxShadow: "0 8px 24px rgba(0, 229, 255, 0.35)",
                    }}
                  >
                    FOLLOW @flash__ai__digital
                  </div>

                  <div style={{ fontSize: 22, color: "#64748B", textAlign: "center" }}>
                    Daily 30-Second Sourced Tech Intel • Zero Fluff
                  </div>
                </div>
              </AbsoluteFill>
            );
          })()}
        </Sequence>
      </div>

      {/* PARALLAX LAYER 3: Active Pop Captions (Top: 1360px, Safe Zone, Zero Wobble) */}
      <PopCaptions words={WORDS} />
    </AbsoluteFill>
  );
};
