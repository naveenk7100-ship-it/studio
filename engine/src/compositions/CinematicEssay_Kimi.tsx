import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  Sequence,
  staticFile,
  Img,
} from "remotion";

const WORDS = [{"word": "Mama,", "start": 0.15, "end": 0.781}, {"word": "Moonshot", "start": 1.107, "end": 1.547}, {"word": "AI", "start": 1.547, "end": 1.891}, {"word": "official", "start": 1.891, "end": 2.905}, {"word": "ga", "start": 3.077, "end": 3.402}, {"word": "Kimi", "start": 3.402, "end": 3.862}, {"word": "K3.1", "start": 3.862, "end": 4.34}, {"word": "Pro", "start": 4.34, "end": 4.684}, {"word": "open", "start": 4.684, "end": 5.029}, {"word": "model", "start": 5.029, "end": 5.296}, {"word": "weights", "start": 5.296, "end": 5.526}, {"word": "release", "start": 5.526, "end": 5.794}, {"word": "chesaru.", "start": 5.794, "end": 6.215}, {"word": "Hacker", "start": 6.731, "end": 7.018}, {"word": "News", "start": 7.018, "end": 7.458}, {"word": "lo", "start": 7.458, "end": 8.396}, {"word": "532", "start": 8.396, "end": 9.104}, {"word": "points", "start": 9.104, "end": 9.314}, {"word": "tho", "start": 9.314, "end": 9.563}, {"word": "top", "start": 9.563, "end": 9.869}, {"word": "trending", "start": 9.869, "end": 10.137}, {"word": "lo", "start": 10.615, "end": 10.94}, {"word": "undi.", "start": 10.94, "end": 11.208}, {"word": "OpenAI", "start": 11.208, "end": 11.514}, {"word": "client", "start": 11.514, "end": 11.897}, {"word": "syntax", "start": 11.897, "end": 12.241}, {"word": "tho", "start": 12.241, "end": 12.566}, {"word": "reasoning", "start": 12.566, "end": 12.93}, {"word": "effort", "start": 12.93, "end": 13.389}, {"word": "max", "start": 13.389, "end": 13.848}, {"word": "configure", "start": 13.848, "end": 14.403}, {"word": "cheyochu.", "start": 14.766, "end": 14.814}, {"word": "2.8T", "start": 14.805, "end": 15.206}, {"word": "parameter", "start": 15.206, "end": 15.417}, {"word": "architecture", "start": 15.417, "end": 15.685}, {"word": "kabatti,", "start": 15.685, "end": 16.22}, {"word": "multi", "start": 16.22, "end": 16.871}, {"word": "node", "start": 17.33, "end": 17.502}, {"word": "GPU", "start": 17.502, "end": 17.808}, {"word": "cluster", "start": 17.808, "end": 18.153}, {"word": "avasaram.", "start": 18.153, "end": 18.478}, {"word": "Open", "start": 18.478, "end": 18.803}, {"word": "weights", "start": 19.281, "end": 19.454}, {"word": "Hugging", "start": 19.454, "end": 19.721}, {"word": "Face", "start": 19.721, "end": 20.047}, {"word": "lo", "start": 20.047, "end": 20.315}, {"word": "Kimi", "start": 20.315, "end": 20.544}, {"word": "model", "start": 20.544, "end": 20.831}, {"word": "license", "start": 20.831, "end": 21.061}, {"word": "tho", "start": 21.061, "end": 21.329}, {"word": "unnayi.", "start": 21.329, "end": 21.577}, {"word": "Official", "start": 21.577, "end": 21.673}, {"word": "model", "start": 21.673, "end": 21.826}, {"word": "card", "start": 22.247, "end": 22.553}, {"word": "link", "start": 22.553, "end": 22.916}, {"word": "bio", "start": 22.916, "end": 23.146}, {"word": "lo", "start": 23.146, "end": 23.337}, {"word": "check", "start": 23.337, "end": 23.835}, {"word": "cheyandi.", "start": 23.835, "end": 24.026}];

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

export const CinematicEssay_Kimi: React.FC = () => {
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
                  src={staticFile("captured_proofs/moonshot_kimi/proof_1_repo_card.png")}
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
                huggingface.co/moonshotai/Kimi-K3.1-Pro • 04 Nov 2026
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
                  color: "#7C4DFF",
                  letterSpacing: 4,
                  marginBottom: 16,
                  textShadow: "0 0 35px rgba(0, 229, 255, 0.4)",
                  zIndex: 2,
                }}
              >
                REASONING
              </div>

              <div style={{ width: 920, textAlign: "center", marginBottom: 28, zIndex: 2 }}>
                <AutoFitText text="Moonshot AI Kimi K3.1 Pro" maxFontSize={64} color="#FFFFFF" />
                <div style={{ fontSize: 30, fontWeight: 600, color: "#94A3B8", marginTop: 12 }}>
                  Open Weights & Reasoning Control
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
                  src={staticFile("captured_proofs/moonshot_kimi/proof_2_docs_capture.png")}
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
                <AutoFitText text="Moonshot AI Kimi K3.1 Pro" maxFontSize={58} color="#FFFFFF" />
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
                    src={staticFile("captured_proofs/moonshot_kimi/proof_1_repo_card.png")}
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
                    src={staticFile("captured_proofs/moonshot_kimi/proof_3_live_api_card.png")}
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
                    src={staticFile("captured_proofs/moonshot_kimi/proof_2_docs_capture.png")}
                    style={{ width: "100%", height: "100%", objectFit: "contain" }}
                  />
                </div>
              </div>

              <div style={{ fontSize: 22, fontWeight: 600, color: "#94A3B8", marginTop: 16 }}>
                Moonshot AI · Kimi K3.1 Pro Model License
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
                <AutoFitText text="Moonshot AI Kimi K3.1 Pro" maxFontSize={56} color="#FFFFFF" />
              </div>

              <div style={{ display: "flex", flexDirection: "column", gap: 20, width: 940 }}>
                
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 24,
                    padding: "24px 32px",
                    borderRadius: 18,
                    background: activeStep === 1 ? "rgba(0, 229, 255, 0.15)" : "#161B22",
                    border: activeStep === 1 ? "2px solid #00E5FF" : "1.5px solid #30363D",
                    boxShadow: activeStep === 1 ? "0 0 25px rgba(0, 229, 255, 0.3)" : "none",
                  }}
                >
                  <div style={{ fontSize: 28, fontWeight: 900, color: activeStep === 1 ? "#00E5FF" : "#64748B" }}>
                    01
                  </div>
                  <div style={{ fontSize: 32, fontWeight: 700, color: activeStep === 1 ? "#FFFFFF" : "#CBD5E1" }}>
                    Download open model weights
                  </div>
                </div>
        
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 24,
                    padding: "24px 32px",
                    borderRadius: 18,
                    background: activeStep === 2 ? "rgba(0, 229, 255, 0.15)" : "#161B22",
                    border: activeStep === 2 ? "2px solid #00E5FF" : "1.5px solid #30363D",
                    boxShadow: activeStep === 2 ? "0 0 25px rgba(0, 229, 255, 0.3)" : "none",
                  }}
                >
                  <div style={{ fontSize: 28, fontWeight: 900, color: activeStep === 2 ? "#00E5FF" : "#64748B" }}>
                    02
                  </div>
                  <div style={{ fontSize: 32, fontWeight: 700, color: activeStep === 2 ? "#FFFFFF" : "#CBD5E1" }}>
                    Configure reasoning effort
                  </div>
                </div>
        
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 24,
                    padding: "24px 32px",
                    borderRadius: 18,
                    background: activeStep === 3 ? "rgba(0, 229, 255, 0.15)" : "#161B22",
                    border: activeStep === 3 ? "2px solid #00E5FF" : "1.5px solid #30363D",
                    boxShadow: activeStep === 3 ? "0 0 25px rgba(0, 229, 255, 0.3)" : "none",
                  }}
                >
                  <div style={{ fontSize: 28, fontWeight: 900, color: activeStep === 3 ? "#00E5FF" : "#64748B" }}>
                    03
                  </div>
                  <div style={{ fontSize: 32, fontWeight: 700, color: activeStep === 3 ? "#FFFFFF" : "#CBD5E1" }}>
                    Execute client completion call
                  </div>
                </div>
        
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
            "captured_proofs/moonshot_kimi/proof_1_repo_card.png",
            "captured_proofs/moonshot_kimi/proof_2_docs_capture.png",
            "captured_proofs/moonshot_kimi/proof_3_live_api_card.png",
            "captured_proofs/moonshot_kimi/proof_1_repo_card.png",
            "captured_proofs/moonshot_kimi/proof_2_docs_capture.png",
            "captured_proofs/moonshot_kimi/proof_3_live_api_card.png",
            "captured_proofs/moonshot_kimi/proof_1_repo_card.png",
            "captured_proofs/moonshot_kimi/proof_2_docs_capture.png",
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
            interpolate(shotFrame, [0, 50], [Math.floor(532 * 0.75), 532], {
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
                  HACKER NEWS SCORE
                </div>
                <div style={{ fontSize: 84, fontWeight: 900, color: "#FFFFFF", marginBottom: 20 }}>
                  {counterVal.toLocaleString()}
                </div>
                <div style={{ fontSize: 26, fontWeight: 600, color: "#94A3B8", marginBottom: 30 }}>
                  huggingface.co/moonshotai/Kimi-K3.1-Pro • 04 Nov 2026
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
                    src={staticFile("captured_proofs/moonshot_kimi/proof_1_repo_card.png")}
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
                  # Official Model Card Client Usage
                </div>
                <AutoFitText text="Moonshot AI Kimi K3.1 Pro" maxFontSize={54} color="#FFFFFF" />
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
                
                <div style={{ fontSize: 30, fontFamily: "consola, monospace", color: "#38BDF8", fontWeight: 700 }}>
                  response = client.chat.completions.create(
                </div>
        
                <div style={{ fontSize: 30, fontFamily: "consola, monospace", color: "#38BDF8", fontWeight: 700 }}>
                      model='kimi-k3.1-pro',
                </div>
        
                <div style={{ fontSize: 30, fontFamily: "consola, monospace", color: "#38BDF8", fontWeight: 700 }}>
                      reasoning_effort='max'
                </div>
        
                <div style={{ fontSize: 30, fontFamily: "consola, monospace", color: "#38BDF8", fontWeight: 700 }}>
                  )
                </div>
        
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
                Requires multi-node GPU cluster (8x 80GB VRAM) for unquantized local inference (~2.8T MoE parameters).
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
                            {/* FLASH Official Brand Logo */}
              <div
                style={{
                  width: 140,
                  height: 140,
                  borderRadius: "50%",
                  overflow: "hidden",
                  border: "3px solid #00E5FF",
                  boxShadow: "0 0 35px rgba(0, 229, 255, 0.5), 0 0 50px rgba(255, 45, 149, 0.3)",
                  marginBottom: 20,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  background: "#07090E",
                }}
              >
                <Img
                  src={staticFile("assets/brand/logo.png")}
                  style={{ width: "100%", height: "100%", objectFit: "cover" }}
                />
              </div>

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
                    src={staticFile("assets/brand/profile.png")}
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
