import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  Sequence,
  staticFile,
  Img,
} from "remotion";

const WORDS = [{"word": "Mama,", "start": 0.15, "end": 0.723}, {"word": "AI", "start": 1.001, "end": 1.331}, {"word": "generate", "start": 1.331, "end": 1.609}, {"word": "chesina", "start": 1.609, "end": 1.922}, {"word": "UI", "start": 1.922, "end": 2.235}, {"word": "chusi", "start": 2.235, "end": 2.651}, {"word": "chusi", "start": 2.651, "end": 2.86}, {"word": "bore", "start": 2.86, "end": 3.016}, {"word": "kottinda?", "start": 3.016, "end": 3.242}, {"word": "Idi", "start": 3.242, "end": 3.381}, {"word": "unslop,", "start": 3.381, "end": 3.972}, {"word": "Claude", "start": 4.302, "end": 4.892}, {"word": "Code", "start": 5.396, "end": 5.605}, {"word": "skill", "start": 5.605, "end": 5.778}, {"word": "for", "start": 5.778, "end": 6.004}, {"word": "interface", "start": 6.004, "end": 6.247}, {"word": "design.", "start": 6.247, "end": 6.647}, {"word": "Purple", "start": 6.647, "end": 7.064}, {"word": "gradients", "start": 7.064, "end": 7.759}, {"word": "mariyu", "start": 7.759, "end": 8.193}, {"word": "generic", "start": 8.332, "end": 8.453}, {"word": "AI", "start": 8.836, "end": 9.253}, {"word": "styling", "start": 9.253, "end": 9.496}, {"word": "ni", "start": 9.496, "end": 10.052}, {"word": "human", "start": 10.052, "end": 10.382}, {"word": "design", "start": 10.382, "end": 10.764}, {"word": "system", "start": 10.764, "end": 11.024}, {"word": "ga", "start": 11.024, "end": 11.068}, {"word": "marchutundi.", "start": 11.024, "end": 11.684}, {"word": "Git", "start": 11.684, "end": 12.449}, {"word": "clone", "start": 12.449, "end": 12.692}, {"word": "chesi", "start": 13.092, "end": 13.578}, {"word": "skills", "start": 13.578, "end": 13.63}, {"word": "folder", "start": 13.63, "end": 13.96}, {"word": "lo", "start": 13.96, "end": 14.464}, {"word": "petti,", "start": 14.464, "end": 14.916}, {"word": "Claude", "start": 14.916, "end": 15.159}, {"word": "Code", "start": 15.159, "end": 15.593}, {"word": "lo", "start": 15.593, "end": 15.801}, {"word": "slash", "start": 15.801, "end": 16.045}, {"word": "unslop", "start": 16.045, "end": 16.635}, {"word": "run", "start": 16.635, "end": 16.861}, {"word": "cheyandi.", "start": 17.434, "end": 17.834}, {"word": "GitHub", "start": 17.834, "end": 17.973}, {"word": "lo", "start": 17.973, "end": 18.129}, {"word": "9054", "start": 18.129, "end": 19.102}, {"word": "stars", "start": 19.102, "end": 19.276}, {"word": "vachayi,", "start": 19.276, "end": 19.484}, {"word": "CC", "start": 19.484, "end": 19.901}, {"word": "BY", "start": 19.901, "end": 20.457}, {"word": "4.0", "start": 20.457, "end": 20.77}, {"word": "license", "start": 20.77, "end": 21.204}, {"word": "tho.", "start": 21.343, "end": 22.055}, {"word": "Full", "start": 22.055, "end": 22.298}, {"word": "commands", "start": 22.298, "end": 22.576}, {"word": "mariyu", "start": 22.576, "end": 22.715}, {"word": "details", "start": 22.715, "end": 22.767}, {"word": "bio", "start": 22.767, "end": 23.254}, {"word": "link", "start": 23.254, "end": 23.445}, {"word": "lo", "start": 23.445, "end": 23.705}, {"word": "check", "start": 23.705, "end": 23.827}, {"word": "cheyandi.", "start": 23.827, "end": 24.018}];

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

export const CinematicEssay_Unslop: React.FC = () => {
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
                  src={staticFile("captured_proofs/heydamir_unslop/proof_1_repo_card.png")}
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
                github.com/heydamir/unslop • 29 Oct 2026
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
                  color: "#00E5FF",
                  letterSpacing: 4,
                  marginBottom: 16,
                  textShadow: "0 0 35px rgba(0, 229, 255, 0.4)",
                  zIndex: 2,
                }}
              >
                PRECISION
              </div>

              <div style={{ width: 920, textAlign: "center", marginBottom: 28, zIndex: 2 }}>
                <AutoFitText text="heydamir / unslop" maxFontSize={64} color="#FFFFFF" />
                <div style={{ fontSize: 30, fontWeight: 600, color: "#94A3B8", marginTop: 12 }}>
                  Vibecoded UI De-Slopper & Human Styler
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
                  src={staticFile("captured_proofs/heydamir_unslop/proof_2_docs_capture.png")}
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
                <AutoFitText text="heydamir / unslop" maxFontSize={58} color="#FFFFFF" />
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
                    src={staticFile("captured_proofs/heydamir_unslop/proof_1_repo_card.png")}
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
                    src={staticFile("captured_proofs/heydamir_unslop/proof_3_live_api_card.png")}
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
                    src={staticFile("captured_proofs/heydamir_unslop/proof_2_docs_capture.png")}
                    style={{ width: "100%", height: "100%", objectFit: "contain" }}
                  />
                </div>
              </div>

              <div style={{ fontSize: 22, fontWeight: 600, color: "#94A3B8", marginTop: 16 }}>
                Created by Damir Sokolovsky (@heydamir) · CC BY 4.0
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
                <AutoFitText text="heydamir / unslop" maxFontSize={56} color="#FFFFFF" />
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
                    Audit UI slop and hierarchy
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
                    Generate human design tokens
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
                    Apply redline layout pass
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
            "captured_proofs/heydamir_unslop/proof_1_repo_card.png",
            "captured_proofs/heydamir_unslop/proof_2_docs_capture.png",
            "captured_proofs/heydamir_unslop/proof_3_live_api_card.png",
            "captured_proofs/heydamir_unslop/proof_1_repo_card.png",
            "captured_proofs/heydamir_unslop/proof_2_docs_capture.png",
            "captured_proofs/heydamir_unslop/proof_3_live_api_card.png",
            "captured_proofs/heydamir_unslop/proof_1_repo_card.png",
            "captured_proofs/heydamir_unslop/proof_2_docs_capture.png",
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
            interpolate(shotFrame, [0, 50], [Math.floor(9054 * 0.75), 9054], {
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
                  GITHUB STARS
                </div>
                <div style={{ fontSize: 84, fontWeight: 900, color: "#FFFFFF", marginBottom: 20 }}>
                  {counterVal.toLocaleString()}
                </div>
                <div style={{ fontSize: 26, fontWeight: 600, color: "#94A3B8", marginBottom: 30 }}>
                  github.com/heydamir/unslop • 29 Oct 2026
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
                    src={staticFile("captured_proofs/heydamir_unslop/proof_1_repo_card.png")}
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
                  # Claude Code Execution Commands
                </div>
                <AutoFitText text="heydamir / unslop" maxFontSize={54} color="#FFFFFF" />
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
                  git clone https://github.com/heydamir/unslop
                </div>
        
                <div style={{ fontSize: 30, fontFamily: "consola, monospace", color: "#38BDF8", fontWeight: 700 }}>
                  cp -r unslop/skills/unslop ~/.claude/skills/
                </div>
        
                <div style={{ fontSize: 30, fontFamily: "consola, monospace", color: "#38BDF8", fontWeight: 700 }}>
                  /unslop this dashboard
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
                Transforms UI tokens, contrast ratios and typography; does not rewrite business backend logic.
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
