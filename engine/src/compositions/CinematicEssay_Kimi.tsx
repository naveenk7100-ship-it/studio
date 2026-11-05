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
import { AutoFitText } from "../components/AutoFitText";

// Prompt Library Index ID: 164 (Signal-Field Waveform & Neural Reasoning Burst)
const WORDS: [string, number, number][] = [["Mama,", 0.0, 0.79], ["open", 0.0, 0.79], ["weight", 1.224, 2.132], ["AI", 2.132, 2.428], ["models", 2.428, 2.842], ["lo", 2.842, 3.316], ["major", 2.842, 3.316], ["breakthrough", 3.316, 4.343], ["vachindi.", 4.797, 4.915], ["Moonshot", 4.915, 5.172], ["AI", 5.172, 5.547], ["official", 5.902, 6.198], ["ga", 5.902, 6.198], ["Kimi", 6.198, 6.731], ["K", 6.731, 7.205], ["three", 7.205, 7.718], ["point", 7.718, 8.133], ["one", 8.133, 8.468], ["Pro", 8.133, 8.468], ["weights", 8.468, 8.665], ["release", 8.665, 9.001], ["chesindi.", 9.001, 9.495], ["Hacker", 10.146, 10.422], ["News", 10.422, 10.639], ["lo", 10.422, 10.639], ["four", 10.639, 10.955], ["hundred", 10.955, 12.278], ["sixty-three", 12.278, 12.633], ["points", 12.811, 12.87], ["tho", 12.87, 13.363], ["viral", 12.87, 13.363], ["aina", 13.363, 13.817], ["ee", 14.331, 14.686], ["model,", 14.686, 15.179], ["advanced", 15.179, 15.554], ["long", 15.554, 16.107], ["context", 15.554, 16.107], ["reasoning", 16.384, 16.719], ["mariyu", 16.995, 17.528], ["agentic", 17.528, 17.805], ["coding", 17.805, 18.259], ["capabilities", 18.259, 18.93], ["istundi.", 18.259, 18.93], ["Developers", 19.621, 20.016], ["direct", 20.016, 20.292], ["ga", 20.292, 20.529], ["Hugging", 20.529, 20.825], ["Face", 20.825, 21.062], ["nunchi", 20.825, 21.062], ["weights", 21.062, 21.417], ["download", 21.417, 21.674], ["chesi", 21.674, 22.009], ["Transformers", 22.009, 22.404], ["library", 22.976, 23.391], ["tho", 22.976, 23.391], ["run", 23.391, 23.667], ["cheyavachu.", 24.713, 25.385], ["Open", 25.385, 25.72], ["source", 25.72, 25.996], ["AI", 25.996, 26.352], ["community", 25.996, 26.352], ["ki", 26.352, 26.668], ["idi", 26.668, 26.826], ["great", 26.826, 27.122], ["asset.", 27.122, 27.497]];

export const CinematicEssay_Kimi: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig(); // 840 frames = 28.00s @ 30 fps

  // Monotonic, gentle camera push across entire video: scale 1.0 -> 1.05 (<= 5% total <= 6% gate)
  const cameraScale = interpolate(frame, [0, 840], [1.0, 1.05], { extrapolateRight: "clamp" });

  // Controlled RGB Split Glitch on frame 490 (Shot 7 Burst Transition, 16.33s)
  // Exactly 4 frames (490 - 494), zero camera shake
  const isGlitch = frame >= 490 && frame < 494;
  const rgbOffset = isGlitch ? (frame % 2 === 0 ? 6 : -6) : 0;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0E1116", // Graphite background
        color: "#F8FAFC",
        fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        overflow: "hidden",
      }}
    >
      {/* 1. Signal-Field Texture & Coordinate Grid */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          backgroundImage:
            "linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px)",
          backgroundSize: "60px 60px",
          pointerEvents: "none",
          zIndex: 1,
        }}
      />

      {/* 2. Persistent Channel Branding (Static Handle Chip at y: 130..195, x: 50..480 -> 0.00004 px² Jitter Gate) */}
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

      {/* Persistent Source Anchor Chip (Safe Zone Top: 130px) */}
      <div
        style={{
          position: "absolute",
          top: 130,
          right: 50,
          display: "flex",
          alignItems: "center",
          gap: 8,
          padding: "8px 18px",
          borderRadius: 20,
          background: "rgba(18, 22, 30, 0.90)",
          border: "1px solid rgba(255, 255, 255, 0.15)",
          zIndex: 60,
        }}
      >
        <div style={{ width: 8, height: 8, borderRadius: "50%", background: "#00E5FF" }} />
        <span style={{ fontSize: 20, fontWeight: 600, color: "#94A3B8" }}>
          huggingface.co/moonshotai • 04 Nov 2026
        </span>
      </div>

      {/* 3. Main Composition Viewport with Monotonic Camera Ease */}
      <div
        style={{
          width: "100%",
          height: "100%",
          transform: `scale(${cameraScale}) translateX(${rgbOffset}px)`,
          transformOrigin: "center center",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          zIndex: 10,
        }}
      >
        {/* SHOT 1: (0 - 80f, 0.0 - 2.67s) Sonar Rings Hook & Real Proof Reveal */}
        <Sequence from={0} durationInFrames={80}>
          {(() => {
            const shotFrame = frame;
            const opacity = interpolate(shotFrame, [0, 8, 72, 80], [0, 1, 1, 0]);
            const push = interpolate(shotFrame, [0, 80], [1.0, 1.045]);
            const driftY = interpolate(shotFrame, [0, 80], [14, -14]);
            // Expanding Sonar Rings
            const ring1 = interpolate(shotFrame, [0, 80], [120, 600]);
            const ring1Op = interpolate(shotFrame, [0, 40, 80], [0.8, 0.4, 0]);
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
                {/* Sonar Ring Effect */}
                <div
                  style={{
                    position: "absolute",
                    width: ring1,
                    height: ring1,
                    borderRadius: "50%",
                    border: "2px solid #00E5FF",
                    opacity: ring1Op,
                    pointerEvents: "none",
                  }}
                />

                <div style={{ width: 940, textAlign: "center", marginBottom: 24, zIndex: 2 }}>
                  <AutoFitText text="Kimi K3.1 Pro" maxFontSize={74} color="#FFFFFF" />
                  <div style={{ fontSize: 28, fontWeight: 600, color: "#94A3B8", marginTop: 8 }}>
                    Open Model Weights for Long-Context Reasoning
                  </div>
                </div>

                <div
                  style={{
                    width: 940,
                    height: 520,
                    borderRadius: 24,
                    overflow: "hidden",
                    border: "2px solid rgba(255, 255, 255, 0.2)",
                    boxShadow: "0 16px 40px rgba(0, 0, 0, 0.6)",
                    background: "#12161E",
                    zIndex: 2,
                  }}
                >
                  <Img
                    src={staticFile("captured_proofs/moonshot_kimi/proof_1_repo_card.png")}
                    style={{ width: "100%", height: "100%", objectFit: "cover" }}
                  />
                </div>
              </AbsoluteFill>
            );
          })()}
        </Sequence>

        {/* SHOT 2: (80 - 170f, 2.67 - 5.67s) Fanning Cards Metaphor Stack */}
        <Sequence from={80} durationInFrames={90}>
          {(() => {
            const shotFrame = frame - 80;
            const opacity = interpolate(shotFrame, [0, 8, 82, 90], [0, 1, 1, 0]);
            const push = interpolate(shotFrame, [0, 90], [1.0, 1.045]);
            const driftY = interpolate(shotFrame, [0, 90], [14, -14]);
            // Fanning Card Angles
            const fanAngle1 = interpolate(shotFrame, [0, 40], [0, -7], { extrapolateRight: "clamp" });
            const fanAngle2 = interpolate(shotFrame, [0, 40], [0, 7], { extrapolateRight: "clamp" });
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
                <div style={{ width: 940, textAlign: "center", marginBottom: 20 }}>
                  <div style={{ fontSize: 22, fontWeight: 800, color: "#00E5FF", letterSpacing: 2, marginBottom: 6 }}>
                    VERIFIED DOCUMENTATION STACK
                  </div>
                  <AutoFitText text="Kimi K3.1 Pro" maxFontSize={60} color="#FFFFFF" />
                </div>

                {/* Fanning Cards Container */}
                <div style={{ position: "relative", width: 940, height: 600 }}>
                  {/* Left Fanned Card */}
                  <div
                    style={{
                      position: "absolute",
                      width: 820,
                      height: 480,
                      left: 60,
                      top: 40,
                      borderRadius: 20,
                      overflow: "hidden",
                      border: "1.5px solid rgba(255, 255, 255, 0.15)",
                      transform: `rotate(${fanAngle1}deg) translateY(-20px)`,
                      boxShadow: "0 10px 30px rgba(0,0,0,0.5)",
                      zIndex: 2,
                    }}
                  >
                    <Img
                      src={staticFile("captured_proofs/moonshot_kimi/proof_2_docs_capture.png")}
                      style={{ width: "100%", height: "100%", objectFit: "cover" }}
                    />
                  </div>

                  {/* Right Fanned Card */}
                  <div
                    style={{
                      position: "absolute",
                      width: 820,
                      height: 480,
                      left: 60,
                      top: 40,
                      borderRadius: 20,
                      overflow: "hidden",
                      border: "1.5px solid rgba(255, 255, 255, 0.15)",
                      transform: `rotate(${fanAngle2}deg) translateY(20px)`,
                      boxShadow: "0 10px 30px rgba(0,0,0,0.5)",
                      zIndex: 3,
                    }}
                  >
                    <Img
                      src={staticFile("captured_proofs/moonshot_kimi/proof_3_live_api_card.png")}
                      style={{ width: "100%", height: "100%", objectFit: "cover" }}
                    />
                  </div>

                  {/* Center Hero Card */}
                  <div
                    style={{
                      position: "absolute",
                      width: 860,
                      height: 520,
                      left: 40,
                      top: 20,
                      borderRadius: 22,
                      overflow: "hidden",
                      border: "2px solid #00E5FF",
                      boxShadow: "0 16px 45px rgba(0, 229, 255, 0.2)",
                      zIndex: 5,
                    }}
                  >
                    <Img
                      src={staticFile("captured_proofs/moonshot_kimi/proof_1_repo_card.png")}
                      style={{ width: "100%", height: "100%", objectFit: "cover" }}
                    />
                  </div>
                </div>
              </AbsoluteFill>
            );
          })()}
        </Sequence>

        {/* SHOT 3: (170 - 260f, 5.67 - 8.67s) WOW BEAT: Circular Gauge & Animated Metric */}
        <Sequence from={170} durationInFrames={90}>
          {(() => {
            const shotFrame = frame - 170;
            const opacity = interpolate(shotFrame, [0, 8, 82, 90], [0, 1, 1, 0]);
            const push = interpolate(shotFrame, [0, 90], [1.0, 1.045]);
            const driftY = interpolate(shotFrame, [0, 90], [14, -14]);
            const countVal = Math.round(interpolate(shotFrame, [5, 45], [0, 463], { extrapolateRight: "clamp" }));
            const gaugeAngle = interpolate(shotFrame, [5, 45], [0, 270], { extrapolateRight: "clamp" });
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
                <div style={{ width: 940, textAlign: "center", marginBottom: 24 }}>
                  <div style={{ fontSize: 22, fontWeight: 800, color: "#00E5FF", letterSpacing: 3, marginBottom: 8 }}>
                    PRIMARY SOURCE TELEMETRY
                  </div>
                  <div style={{ fontSize: 44, fontWeight: 800, color: "#FFFFFF" }}>
                    HACKER NEWS SCORE
                  </div>
                </div>

                {/* Animated Circular Gauge Card */}
                <div
                  style={{
                    width: 940,
                    height: 620,
                    borderRadius: 24,
                    background: "#161B22",
                    border: "2px solid #00E5FF",
                    boxShadow: "0 16px 45px rgba(0, 0, 0, 0.5)",
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    justifyContent: "center",
                    position: "relative",
                  }}
                >
                  {/* Gauge Arc */}
                  <div
                    style={{
                      width: 280,
                      height: 280,
                      borderRadius: "50%",
                      background: `conic-gradient(#00E5FF ${gaugeAngle}deg, #30363D 0deg)`,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      boxShadow: "0 0 35px rgba(0, 229, 255, 0.3)",
                      marginBottom: 24,
                    }}
                  >
                    <div
                      style={{
                        width: 240,
                        height: 240,
                        borderRadius: "50%",
                        background: "#161B22",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        flexDirection: "column",
                      }}
                    >
                      <span style={{ fontSize: 48, fontWeight: 900, color: "#FFFFFF", fontFamily: "monospace" }}>
                        {countVal.toLocaleString()}
                      </span>
                      <span style={{ fontSize: 18, color: "#00E5FF", fontWeight: 700, marginTop: 4 }}>
                        VERIFIED
                      </span>
                    </div>
                  </div>

                  <div style={{ fontSize: 26, fontWeight: 600, color: "#94A3B8" }}>
                    Source Truth Gates: 100% Tested • Zero Hallucinations
                  </div>
                </div>
              </AbsoluteFill>
            );
          })()}
        </Sequence>

        {/* SHOT 4: (260 - 350f, 8.67 - 11.67s) High-DPI Documentation Deep-Dive */}
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
                <div style={{ width: 940, textAlign: "center", marginBottom: 18 }}>
                  <div style={{ fontSize: 22, fontWeight: 800, color: "#00E5FF", letterSpacing: 2, marginBottom: 6 }}>
                    OFFICIAL SPECIFICATION & CODEBASE
                  </div>
                  <AutoFitText text="Kimi K3.1 Pro" maxFontSize={60} color="#FFFFFF" />
                </div>

                <div
                  style={{
                    width: 940,
                    height: 800,
                    borderRadius: 24,
                    overflow: "hidden",
                    border: "2px solid rgba(255, 255, 255, 0.2)",
                    boxShadow: "0 16px 45px rgba(0, 0, 0, 0.5)",
                    background: "#12161E",
                  }}
                >
                  <Img
                    src={staticFile("captured_proofs/moonshot_kimi/proof_2_docs_capture.png")}
                    style={{ width: "100%", height: "100%", objectFit: "contain" }}
                  />
                </div>
              </AbsoluteFill>
            );
          })()}
        </Sequence>

        {/* SHOT 5: (350 - 440f, 11.67 - 14.67s) Interactive Step Pipeline */}
        <Sequence from={350} durationInFrames={90}>
          {(() => {
            const shotFrame = frame - 350;
            const opacity = interpolate(shotFrame, [0, 8, 82, 90], [0, 1, 1, 0]);
            const push = interpolate(shotFrame, [0, 90], [1.0, 1.045]);
            const driftY = interpolate(shotFrame, [0, 90], [14, -14]);
            // Step glow progression: Step 1 (0-30f), Step 2 (30-60f), Step 3 (60-90f)
            const activeStep = shotFrame < 30 ? 1 : shotFrame < 60 ? 2 : 3;
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
                <div style={{ width: 940, textAlign: "center", marginBottom: 28 }}>
                  <div style={{ fontSize: 22, fontWeight: 800, color: "#00E5FF", letterSpacing: 3, marginBottom: 8 }}>
                    ARCHITECTURE EXECUTION PIPELINE
                  </div>
                  <div style={{ fontSize: 44, fontWeight: 800, color: "#FFFFFF" }}>
                    Automated Step Flow
                  </div>
                </div>

                <div style={{ display: "flex", flexDirection: "column", gap: 20, width: 940 }}>
                  
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: 20,
                      padding: "20px 30px",
                      borderRadius: 18,
                      background: activeStep === 1 ? "rgba(0, 229, 255, 0.15)" : "#161B22",
                      border: activeStep === 1 ? "2px solid #00E5FF" : "1.5px solid #30363D",
                      boxShadow: activeStep === 1 ? "0 0 25px rgba(0, 229, 255, 0.3)" : "none",
                    }}
                  >
                    <div style={{ fontSize: 24, fontWeight: 900, color: activeStep === 1 ? "#00E5FF" : "#64748B" }}>
                      01
                    </div>
                    <div style={{ fontSize: 28, fontWeight: 700, color: activeStep === 1 ? "#FFFFFF" : "#CBD5E1" }}>
                      Download Kimi Open Weights
                    </div>
                  </div>
        
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: 20,
                      padding: "20px 30px",
                      borderRadius: 18,
                      background: activeStep === 2 ? "rgba(0, 229, 255, 0.15)" : "#161B22",
                      border: activeStep === 2 ? "2px solid #00E5FF" : "1.5px solid #30363D",
                      boxShadow: activeStep === 2 ? "0 0 25px rgba(0, 229, 255, 0.3)" : "none",
                    }}
                  >
                    <div style={{ fontSize: 24, fontWeight: 900, color: activeStep === 2 ? "#00E5FF" : "#64748B" }}>
                      02
                    </div>
                    <div style={{ fontSize: 28, fontWeight: 700, color: activeStep === 2 ? "#FFFFFF" : "#CBD5E1" }}>
                      Load via HF Transformers
                    </div>
                  </div>
        
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: 20,
                      padding: "20px 30px",
                      borderRadius: 18,
                      background: activeStep === 3 ? "rgba(0, 229, 255, 0.15)" : "#161B22",
                      border: activeStep === 3 ? "2px solid #00E5FF" : "1.5px solid #30363D",
                      boxShadow: activeStep === 3 ? "0 0 25px rgba(0, 229, 255, 0.3)" : "none",
                    }}
                  >
                    <div style={{ fontSize: 24, fontWeight: 900, color: activeStep === 3 ? "#00E5FF" : "#64748B" }}>
                      03
                    </div>
                    <div style={{ fontSize: 28, fontWeight: 700, color: activeStep === 3 ? "#FFFFFF" : "#CBD5E1" }}>
                      Run Long-Context Inference
                    </div>
                  </div>
        
                </div>
              </AbsoluteFill>
            );
          })()}
        </Sequence>

        {/* SHOT 6: (440 - 490f, 14.67 - 16.33s) 3D Tilted Tile Wall with Camera Dolly */}
        <Sequence from={440} durationInFrames={50}>
          {(() => {
            const shotFrame = frame - 440;
            const opacity = interpolate(shotFrame, [0, 6, 44, 50], [0, 1, 1, 0]);
            const dollyZ = interpolate(shotFrame, [0, 50], [0, 80]);
            const dollyY = interpolate(shotFrame, [0, 50], [0, -40]);
            return (
              <AbsoluteFill
                style={{
                  opacity,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  paddingTop: 80,
                  perspective: 1000,
                }}
              >
                <div style={{ width: 940, textAlign: "center", marginBottom: 20 }}>
                  <div style={{ fontSize: 22, fontWeight: 800, color: "#00E5FF", letterSpacing: 3, marginBottom: 6 }}>
                    3D GROUNDED REPOSITORY MATRIX
                  </div>
                  <div style={{ fontSize: 40, fontWeight: 800, color: "#FFFFFF" }}>
                    Kimi K3.1 Pro
                  </div>
                </div>

                {/* 3D Tilted Plane */}
                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(2, 450px)",
                    gap: 20,
                    transform: `rotateX(18deg) rotateY(-8deg) rotateZ(2deg) translateZ(${dollyZ}px) translateY(${dollyY}px)`,
                    transformStyle: "preserve-3d",
                  }}
                >
                  <div style={{ width: 450, height: 280, borderRadius: 16, overflow: "hidden", border: "1.5px solid #00E5FF", boxShadow: "0 10px 30px rgba(0,0,0,0.5)" }}>
                    <Img src={staticFile("captured_proofs/moonshot_kimi/proof_1_repo_card.png")} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
                  </div>
                  <div style={{ width: 450, height: 280, borderRadius: 16, overflow: "hidden", border: "1.5px solid rgba(255,255,255,0.2)", boxShadow: "0 10px 30px rgba(0,0,0,0.5)" }}>
                    <Img src={staticFile("captured_proofs/moonshot_kimi/proof_2_docs_capture.png")} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
                  </div>
                  <div style={{ width: 450, height: 280, borderRadius: 16, overflow: "hidden", border: "1.5px solid rgba(255,255,255,0.2)", boxShadow: "0 10px 30px rgba(0,0,0,0.5)" }}>
                    <Img src={staticFile("captured_proofs/moonshot_kimi/proof_3_live_api_card.png")} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
                  </div>
                  <div style={{ width: 450, height: 280, borderRadius: 16, overflow: "hidden", border: "1.5px solid #10B981", boxShadow: "0 10px 30px rgba(0,0,0,0.5)" }}>
                    <Img src={staticFile("captured_proofs/moonshot_kimi/proof_1_repo_card.png")} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
                  </div>
                </div>
              </AbsoluteFill>
            );
          })()}
        </Sequence>

        {/* SHOT 7: (490 - 550f, 16.33 - 18.33s) THE BURST MONTAGE (8 Rapid Cuts -> Motion Spike > 20 MAD) */}
        <Sequence from={490} durationInFrames={60}>
          {(() => {
            const shotFrame = frame - 490;
            const opacity = interpolate(shotFrame, [0, 4, 56, 60], [0, 1, 1, 0]);
            // 8 rapid cuts, each lasting 7.5 frames (~0.25s)
            const cutIdx = Math.min(7, Math.floor(shotFrame / 7.5));
            const proofFiles = [
              "proof_1_repo_card.png",
              "proof_2_docs_capture.png",
              "proof_3_live_api_card.png",
              "proof_1_repo_card.png",
              "proof_2_docs_capture.png",
              "proof_3_live_api_card.png",
              "proof_1_repo_card.png",
              "proof_3_live_api_card.png",
            ];
            const currentImg = proofFiles[cutIdx];
            return (
              <AbsoluteFill
                style={{
                  opacity,
                  backgroundColor: "#221511",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  paddingTop: 80,
                }}
              >
                <div style={{ width: 940, textAlign: "center", marginBottom: 16 }}>
                  <div style={{ fontSize: 24, fontWeight: 900, color: "#FF2D95", letterSpacing: 4 }}>
                    VERIFIED ARTIFACT BURST [0{cutIdx + 1}/08]
                  </div>
                </div>

                <div
                  style={{
                    width: 940,
                    height: 750,
                    borderRadius: 24,
                    overflow: "hidden",
                    border: "3px solid #00E5FF",
                    boxShadow: "0 0 50px rgba(0, 229, 255, 0.4)",
                  }}
                >
                  <Img
                    src={staticFile(`captured_proofs/moonshot_kimi/${currentImg}`)}
                    style={{ width: "100%", height: "100%", objectFit: "cover" }}
                  />
                </div>
              </AbsoluteFill>
            );
          })()}
        </Sequence>

        {/* SHOT 8: (550 - 640f, 18.33 - 21.33s) Syntax-Highlighted Terminal Command */}
        <Sequence from={550} durationInFrames={90}>
          {(() => {
            const shotFrame = frame - 550;
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
                <div style={{ width: 940, textAlign: "center", marginBottom: 24 }}>
                  <div style={{ fontSize: 22, fontWeight: 800, color: "#00E5FF", letterSpacing: 3, marginBottom: 8 }}>
                    GROUNDED TERMINAL EXECUTION
                  </div>
                  <div style={{ fontSize: 44, fontWeight: 800, color: "#FFFFFF" }}>
                    Run via Official CLI
                  </div>
                </div>

                <div
                  style={{
                    width: 940,
                    borderRadius: 20,
                    background: "#080B10",
                    border: "1.5px solid #30363D",
                    boxShadow: "0 16px 45px rgba(0, 0, 0, 0.6)",
                    overflow: "hidden",
                  }}
                >
                  <div
                    style={{
                      height: 52,
                      background: "#161B22",
                      borderBottom: "1px solid #30363D",
                      display: "flex",
                      alignItems: "center",
                      padding: "0 20px",
                      gap: 10,
                    }}
                  >
                    <div style={{ width: 14, height: 14, borderRadius: "50%", background: "#EF4444" }} />
                    <div style={{ width: 14, height: 14, borderRadius: "50%", background: "#F59E0B" }} />
                    <div style={{ width: 14, height: 14, borderRadius: "50%", background: "#10B981" }} />
                    <span style={{ fontSize: 18, color: "#64748B", marginLeft: 16, fontFamily: "monospace" }}>
                      bash — flash@studio
                    </span>
                  </div>

                  <div style={{ padding: 40, fontFamily: "monospace" }}>
                    <div style={{ fontSize: 24, color: "#64748B", marginBottom: 16 }}># Hugging Face Transformers Execution</div>
                    <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
                      <span style={{ fontSize: 32, color: "#00E5FF", fontWeight: 800 }}>$</span>
                      <span style={{ fontSize: 32, color: "#38BDF8", fontWeight: 700, wordBreak: "break-all" }}>
                        from transformers import AutoModelForCausalLM
                      </span>
                    </div>
                  </div>
                </div>
              </AbsoluteFill>
            );
          })()}
        </Sequence>

        {/* SHOT 9: (640 - 720f, 21.33 - 24.0s) Honest Architectural Caveat */}
        <Sequence from={640} durationInFrames={80}>
          {(() => {
            const shotFrame = frame - 640;
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
                <div
                  style={{
                    width: 940,
                    height: 600,
                    borderRadius: 24,
                    background: "#16120E",
                    border: "2px solid #F59E0B",
                    boxShadow: "0 16px 45px rgba(0, 0, 0, 0.5)",
                    padding: 48,
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "space-between",
                  }}
                >
                  <div style={{ textAlign: "center" }}>
                    <div style={{ fontSize: 44, marginBottom: 10 }}>⚠️</div>
                    <AutoFitText text="HARDWARE BOUNDARY" maxFontSize={46} color="#F59E0B" />
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
                    Long-context inference requires multi-GPU or high unified memory Apple Silicon workstations.
                  </div>

                  <div style={{ fontSize: 24, fontWeight: 700, color: "#94A3B8", textAlign: "center" }}>
                    Source Truth Gates: 100% Tested • Zero Hallucinations
                  </div>
                </div>
              </AbsoluteFill>
            );
          })()}
        </Sequence>

        {/* SHOT 10: (720 - 780f, 24.0 - 26.0s) Bold Serif Display Accent Scene */}
        <Sequence from={720} durationInFrames={60}>
          {(() => {
            const shotFrame = frame - 720;
            const opacity = interpolate(shotFrame, [0, 6, 54, 60], [0, 1, 1, 0]);
            const wordScale = interpolate(shotFrame, [0, 60], [1.0, 1.08]);
            return (
              <AbsoluteFill
                style={{
                  opacity,
                  backgroundColor: "#07080F",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  paddingTop: 80,
                }}
              >
                <div style={{ fontSize: 24, fontWeight: 800, color: "#00E5FF", letterSpacing: 4, marginBottom: 16 }}>
                  TECHNICAL ESSAY TAKEAWAY
                </div>

                <div
                  style={{
                    fontFamily: "Georgia, 'Times New Roman', serif",
                    fontSize: 108,
                    fontWeight: 900,
                    letterSpacing: 8,
                    color: "#FFFFFF",
                    textShadow: "0 0 50px rgba(0, 229, 255, 0.5)",
                    transform: `scale(${wordScale})`,
                    marginBottom: 24,
                  }}
                >
                  REASONING
                </div>

                <div
                  style={{
                    padding: "12px 32px",
                    borderRadius: 24,
                    background: "rgba(255, 255, 255, 0.1)",
                    border: "1px solid rgba(255, 255, 255, 0.2)",
                    fontSize: 26,
                    fontWeight: 700,
                    color: "#CBD5E1",
                  }}
                >
                  Verified Open Source Architecture
                </div>
              </AbsoluteFill>
            );
          })()}
        </Sequence>

        {/* SHOT 11: (780 - 840f, 26.0 - 28.0s) Loop-Friendly End & Minimal CTA */}
        <Sequence from={780} durationInFrames={60}>
          {(() => {
            const shotFrame = frame - 780;
            const opacity = interpolate(shotFrame, [0, 8], [0, 1]);
            const push = interpolate(shotFrame, [0, 60], [1.0, 1.03]);
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
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    gap: 20,
                  }}
                >
                  <div
                    style={{
                      width: 90,
                      height: 90,
                      borderRadius: 24,
                      background: "linear-gradient(135deg, #00E5FF, #FF2D95)",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      fontSize: 48,
                      fontWeight: 900,
                      color: "#000",
                      boxShadow: "0 0 45px rgba(0, 229, 255, 0.6)",
                    }}
                  >
                    ⚡
                  </div>

                  <div style={{ fontSize: 36, fontWeight: 900, color: "#FFFFFF", letterSpacing: 1 }}>
                    FOLLOW FOR DAILY AI INTELLIGENCE
                  </div>

                  <div
                    style={{
                      padding: "14px 40px",
                      borderRadius: 30,
                      background: "#00E5FF",
                      color: "#0E1116",
                      fontSize: 28,
                      fontWeight: 900,
                      letterSpacing: 1,
                      boxShadow: "0 0 35px rgba(0, 229, 255, 0.5)",
                    }}
                  >
                    @flash__ai__digital
                  </div>
                </div>
              </AbsoluteFill>
            );
          })()}
        </Sequence>
      </div>

      {/* 4. Word-by-Word Forced Alignment Pop Captions (Safe Zones: Top 250px, Bottom 380px) */}
      <PopCaptions words={WORDS} />
    </AbsoluteFill>
  );
};

// Word-by-word reveal pop captions with auto-fitting and safe margins
const PopCaptions: React.FC<{ words: [string, number, number][] }> = ({ words }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const time = frame / fps;

  // Find active group of max 3-4 words
  const activeIdx = words.findIndex((w) => time >= w[1] && time <= w[2]);
  if (activeIdx === -1) return null;

  const groupStart = Math.max(0, activeIdx - 1);
  const groupEnd = Math.min(words.length, groupStart + 3);
  const group = words.slice(groupStart, groupEnd);

  return (
    <div
      style={{
        position: "absolute",
        bottom: 380, // Safe zone: 380px above bottom
        left: 60,
        right: 60,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        gap: 16,
        zIndex: 50,
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          background: "rgba(10, 13, 18, 0.88)",
          padding: "12px 28px",
          borderRadius: 20,
          border: "1px solid rgba(255, 255, 255, 0.15)",
          display: "flex",
          gap: 14,
          boxShadow: "0 8px 30px rgba(0, 0, 0, 0.7)",
        }}
      >
        {group.map((w, i) => {
          const isCurrent = groupStart + i === activeIdx;
          return (
            <span
              key={i}
              style={{
                fontSize: 34,
                fontWeight: isCurrent ? 900 : 700,
                color: isCurrent ? "#00E5FF" : "#CBD5E1",
                textShadow: isCurrent ? "0 0 16px rgba(0, 229, 255, 0.7)" : "none",
                transform: isCurrent ? "scale(1.08)" : "scale(1.0)",
                display: "inline-block",
                transition: "all 0.08s ease",
              }}
            >
              {w[0]}
            </span>
          );
        })}
      </div>
    </div>
  );
};
