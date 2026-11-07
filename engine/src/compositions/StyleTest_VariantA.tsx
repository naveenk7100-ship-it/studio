import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  staticFile,
  Img,
} from "remotion";
import wordsData from "../../../cache/words_final_style_test_12s.json";

interface WordItem {
  word: string;
  start: number;
  end: number;
}

const words: WordItem[] = wordsData as WordItem[];

export const StyleTest_VariantA: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const currentTime = frame / fps;

  // 12-Second Narrative Shots (360 frames @ 30fps)
  // Shot 1: Frames 0 - 96 (0.00s - 3.20s) Wide Establishing 3D Blueprint Machine
  // Shot 2: Frames 96 - 195 (3.20s - 6.50s) Exploded View Assembly (Wow Beat: Raptor 2 Apart)
  // Shot 3: Frames 195 - 306 (6.50s - 10.20s) Extreme Close-up: Monospace Command & Vector SVG Dial
  // Shot 4: Frames 306 - 360 (10.20s - 12.00s) End Card Payoff: 3D FLASH Brand Pedestal

  const shot =
    frame < 96 ? 1 : frame < 195 ? 2 : frame < 306 ? 3 : 4;
  const shotRel =
    shot === 1
      ? frame
      : shot === 2
      ? frame - 96
      : shot === 3
      ? frame - 195
      : frame - 306;

  // Active word detection for captions
  const activeWordIdx = words.findIndex(
    (w) => currentTime >= w.start && currentTime <= w.end + 0.12
  );
  const activeWord = activeWordIdx !== -1 ? words[activeWordIdx] : null;

  // Group into max 3 words window
  let captionGroup: WordItem[] = [];
  if (activeWordIdx !== -1) {
    const groupStart = Math.floor(activeWordIdx / 3) * 3;
    captionGroup = words.slice(groupStart, groupStart + 3);
  } else if (currentTime < 10.2) {
    let lastIdx = 0;
    for (let i = 0; i < words.length; i++) {
      if (words[i].start <= currentTime) lastIdx = i;
    }
    const groupStart = Math.floor(lastIdx / 3) * 3;
    captionGroup = words.slice(groupStart, groupStart + 3);
  }

  // CONTINUOUS ACTIVE MOTION IN EVERY SECOND (ZERO SHAKE, SMOOTH CINEMATIC DYNAMICS)
  // Cam orbit: continuous angular sweep in every shot
  const camRotY =
    shot === 1
      ? interpolate(shotRel, [0, 96], [-16, 14])
      : shot === 2
      ? interpolate(shotRel, [0, 99], [12, -18])
      : shot === 3
      ? interpolate(shotRel, [0, 111], [-10, 12])
      : interpolate(shotRel, [0, 54], [-12, 8]);

  const camRotX =
    shot === 1
      ? interpolate(shotRel, [0, 96], [12, 2])
      : shot === 2
      ? interpolate(shotRel, [0, 99], [3, 16])
      : shot === 3
      ? interpolate(shotRel, [0, 111], [14, 4])
      : interpolate(shotRel, [0, 54], [10, 2]);

  const camScale =
    shot === 1
      ? interpolate(shotRel, [0, 96], [1.03, 1.20])
      : shot === 2
      ? interpolate(shotRel, [0, 99], [1.06, 1.25])
      : shot === 3
      ? interpolate(shotRel, [0, 111], [1.14, 1.30])
      : interpolate(shotRel, [0, 54], [1.12, 1.03]);

  // Dynamic sweeping light shaft & laser beam (guarantees continuous frame motion)
  const sweepAngle = (frame * 0.08);
  const lightSweepX = 540 + Math.sin(sweepAngle) * 520;
  const lightSweepY = 960 + Math.cos(sweepAngle * 0.7) * 450;
  const laserY = (frame * 12) % 1920;

  // Background particles drift
  const particleOffset = (frame * 6) % 1200;

  // Transition Glitch
  const isGlitchFrame = frame >= 194 && frame <= 197;
  const glitchOffset = isGlitchFrame ? (frame % 2 === 0 ? 12 : -12) : 0;

  // Exploded View Spring Physics for Shot 2
  const explodeSpring = spring({
    frame: shotRel,
    fps,
    config: { damping: 12, stiffness: 90, mass: 0.8 },
  });
  // Continuous breathing separation so Shot 2 never goes static
  const secondaryFloat = Math.sin(shotRel * 0.12) * 25;
  const nozzleZ = interpolate(explodeSpring, [0, 1], [0, 220]) + secondaryFloat;
  const nozzleY = interpolate(explodeSpring, [0, 1], [0, 170]) + secondaryFloat * 0.8;
  const manifoldZ = interpolate(explodeSpring, [0, 1], [0, -200]) - secondaryFloat;
  const manifoldY = interpolate(explodeSpring, [0, 1], [0, -150]) - secondaryFloat * 0.8;

  // Command typing for Shot 3
  const fullCommand = "npx skills add wheresryan22/anatomy";
  const typedChars = Math.min(
    fullCommand.length,
    Math.floor(
      interpolate(shotRel, [10, 85], [0, fullCommand.length], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      })
    )
  );
  const commandDisplay = fullCommand.slice(0, typedChars);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#031015",
        fontFamily: "'Inter', -apple-system, sans-serif",
        color: "#FFFFFF",
        overflow: "hidden",
      }}
    >
      {/* ============================================================== */}
      {/* DEPTH LAYER 1: ANIMATED BACKGROUND (DEEP TEAL STUDIO MESH)     */}
      {/* ============================================================== */}
      <AbsoluteFill style={{ pointerEvents: "none" }}>
        {/* Dynamic Multi-stop Radial Gradient Mesh */}
        <div
          style={{
            position: "absolute",
            inset: 0,
            background: `radial-gradient(circle 950px at ${lightSweepX}px ${lightSweepY}px, #104555 0%, #082936 45%, #020C10 90%)`,
          }}
        />

        {/* Volumetric Cyan Light Shafts sweeping continuously */}
        <div
          style={{
            position: "absolute",
            width: 1500,
            height: 1000,
            top: -200,
            left: -200 + Math.sin(frame * 0.05) * 120,
            background: "linear-gradient(135deg, rgba(0, 229, 255, 0.22) 0%, rgba(11, 37, 46, 0.0) 70%)",
            transform: `rotate(${-25 + Math.sin(frame * 0.04) * 8}deg)`,
            filter: "blur(40px)",
          }}
        />
        <div
          style={{
            position: "absolute",
            width: 1300,
            height: 900,
            bottom: -150,
            right: -200 + Math.cos(frame * 0.045) * 100,
            background: "linear-gradient(315deg, rgba(0, 229, 255, 0.18) 0%, rgba(4, 18, 23, 0.0) 65%)",
            filter: "blur(50px)",
          }}
        />

        {/* Dynamic Scanning Laser Bar (active motion element) */}
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            top: laserY,
            height: 3,
            background: "linear-gradient(90deg, transparent 0%, rgba(0, 229, 255, 0.8) 50%, transparent 100%)",
            boxShadow: "0 0 15px #00E5FF",
            opacity: 0.6,
          }}
        />

        {/* High-Tech Isometric Coordinate Grid with Crosshairs */}
        <svg
          width="100%"
          height="100%"
          style={{
            position: "absolute",
            inset: 0,
            opacity: 0.40,
          }}
        >
          <defs>
            <pattern
              id="tealGrid"
              width="60"
              height="60"
              patternUnits="userSpaceOnUse"
            >
              <path
                d="M 60 0 L 0 0 0 60"
                fill="none"
                stroke="rgba(0, 229, 255, 0.50)"
                strokeWidth="1.2"
              />
              <path
                d="M 30 25 L 30 35 M 25 30 L 35 30"
                stroke="rgba(0, 229, 255, 0.85)"
                strokeWidth="1.3"
              />
              <circle cx="60" cy="0" r="2.5" fill="#00E5FF" />
              <circle cx="0" cy="60" r="2.5" fill="#00E5FF" />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#tealGrid)" />
        </svg>

        {/* Continuous Active Drift Telemetry Columns (left & right borders) */}
        <div
          style={{
            position: "absolute",
            top: 280,
            left: 20,
            fontFamily: "'Courier New', monospace",
            fontSize: 16,
            color: "rgba(0, 229, 255, 0.55)",
            lineHeight: 1.8,
            letterSpacing: 1.5,
          }}
        >
          <div>SYS:ANATOMY</div>
          <div>ROT_Y: {camRotY.toFixed(1)}°</div>
          <div>ROT_X: {camRotX.toFixed(1)}°</div>
          <div>ZOOM: {camScale.toFixed(2)}x</div>
          <div>PARTICLES: 1,080</div>
          <div>RADAR: ACTIVE</div>
          <div>FRAME: {frame.toString().padStart(4, "0")}</div>
        </div>

        <div
          style={{
            position: "absolute",
            top: 280,
            right: 20,
            textAlign: "right",
            fontFamily: "'Courier New', monospace",
            fontSize: 16,
            color: "rgba(0, 229, 255, 0.55)",
            lineHeight: 1.8,
            letterSpacing: 1.5,
          }}
        >
          <div>ENGINE: RAPTOR 2</div>
          <div>CHAMBER: 300 BAR</div>
          <div>THRUST: 230 TF</div>
          <div>FLOW: 650 KG/S</div>
          <div>SVG 3D PIPELINE</div>
          <div>CLAUDE SKILL</div>
          <div>STARS: 25,676</div>
        </div>

        {/* Vignette Overlay */}
        <div
          style={{
            position: "absolute",
            inset: 0,
            boxShadow: "inset 0 0 160px rgba(0, 0, 0, 0.85)",
          }}
        />
      </AbsoluteFill>

      {/* ============================================================== */}
      {/* DEPTH LAYER 2: 3D VIRTUAL STAGE & HERO ASSET (>= 60% AREA)     */}
      {/* ============================================================== */}
      <AbsoluteFill
        style={{
          perspective: 1200,
          perspectiveOrigin: "50% 50%",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          transform: isGlitchFrame
            ? `translateX(${glitchOffset}px)`
            : "none",
        }}
      >
        <div
          style={{
            width: 1040,
            height: 1320,
            position: "relative",
            transformStyle: "preserve-3d",
            transform: `rotateY(${camRotY}deg) rotateX(${camRotX}deg) scale(${camScale})`,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          {/* SHOT 1: WIDE ESTABLISHING 3D BLUEPRINT MACHINE */}
          {shot === 1 && (
            <div
              style={{
                width: "100%",
                height: "100%",
                position: "relative",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <div
                style={{
                  width: 1000,
                  height: 1120,
                  borderRadius: 24,
                  background: "linear-gradient(180deg, rgba(11, 45, 58, 0.90) 0%, rgba(4, 20, 28, 0.98) 100%)",
                  border: "2.5px solid rgba(0, 229, 255, 0.65)",
                  boxShadow: "0 30px 80px rgba(0, 0, 0, 0.8), 0 0 60px rgba(0, 229, 255, 0.35)",
                  position: "relative",
                  overflow: "hidden",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  padding: 24,
                }}
              >
                {/* Blueprint Card Header */}
                <div
                  style={{
                    width: "100%",
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    borderBottom: "1.5px solid rgba(0, 229, 255, 0.35)",
                    paddingBottom: 16,
                    marginBottom: 16,
                  }}
                >
                  <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                    <div
                      style={{
                        width: 16,
                        height: 16,
                        borderRadius: "50%",
                        backgroundColor: "#00E5FF",
                        boxShadow: "0 0 12px #00E5FF",
                      }}
                    />
                    <span
                      style={{
                        fontFamily: "'Courier New', monospace",
                        fontSize: 30,
                        color: "#00E5FF",
                        fontWeight: 800,
                        letterSpacing: 2,
                      }}
                    >
                      RAPTOR 2 // BLUEPRINT CAD
                    </span>
                  </div>
                  <span
                    style={{
                      fontFamily: "'Courier New', monospace",
                      fontSize: 24,
                      color: "#FFFFFF",
                      fontWeight: 700,
                    }}
                  >
                    300 BAR STAGED
                  </span>
                </div>

                {/* Hero Asset */}
                <div
                  style={{
                    width: 950,
                    height: 890,
                    position: "relative",
                    borderRadius: 18,
                    overflow: "hidden",
                    backgroundColor: "#051A22",
                    border: "1.5px solid rgba(0, 229, 255, 0.35)",
                  }}
                >
                  <Img
                    src={staticFile("captured_proofs/wheresryan22_anatomy/raptor-engine-firing.webp")}
                    style={{
                      width: "100%",
                      height: "100%",
                      objectFit: "contain",
                      transform: `scale(${1.0 + Math.sin(shotRel * 0.08) * 0.04})`,
                    }}
                  />

                  {/* Active Radar Sweep Overlay */}
                  <div
                    style={{
                      position: "absolute",
                      inset: 0,
                      background: `conic-gradient(from ${frame * 4}deg at 50% 50%, rgba(0, 229, 255, 0.18) 0deg, transparent 60deg, transparent 360deg)`,
                      borderRadius: 18,
                      pointerEvents: "none",
                    }}
                  />

                  {/* Dimension Brackets */}
                  <div
                    style={{
                      position: "absolute",
                      left: 20,
                      top: 40,
                      borderLeft: "2.5px solid #00E5FF",
                      borderTop: "2.5px solid #00E5FF",
                      borderBottom: "2.5px solid #00E5FF",
                      width: 24,
                      height: 780,
                      display: "flex",
                      alignItems: "center",
                    }}
                  >
                    <span
                      style={{
                        transform: "rotate(-90deg)",
                        whiteSpace: "nowrap",
                        marginLeft: -28,
                        fontFamily: "'Courier New', monospace",
                        fontSize: 24,
                        color: "#00E5FF",
                        fontWeight: 800,
                      }}
                    >
                      HEIGHT: 3,120 mm
                    </span>
                  </div>

                  {/* Telemetry Tag */}
                  <div
                    style={{
                      position: "absolute",
                      right: 24,
                      bottom: 24,
                      backgroundColor: "rgba(3, 16, 21, 0.92)",
                      border: "1.5px solid #00E5FF",
                      borderRadius: 12,
                      padding: "10px 22px",
                      fontFamily: "'Courier New', monospace",
                      fontSize: 24,
                      color: "#FFFFFF",
                      display: "flex",
                      gap: 20,
                      boxShadow: "0 0 25px rgba(0, 229, 255, 0.3)",
                    }}
                  >
                    <span>THRUST: <b style={{ color: "#00E5FF" }}>230 tf</b></span>
                    <span>FLOW: <b style={{ color: "#00E5FF" }}>650 kg/s</b></span>
                  </div>
                </div>

                {/* Sub-bar */}
                <div
                  style={{
                    width: "100%",
                    display: "flex",
                    justifyContent: "space-between",
                    marginTop: 16,
                    fontFamily: "'Courier New', monospace",
                    fontSize: 24,
                    color: "rgba(0, 229, 255, 0.9)",
                    fontWeight: 700,
                  }}
                >
                  <span>MODEL: ISOMETRIC SVG 3D</span>
                  <span>AUTONOMOUS ENGINE VIEW</span>
                </div>
              </div>
            </div>
          )}

          {/* SHOT 2: EXPLODED VIEW ASSEMBLY (WOW BEAT: 3.2s - 6.5s) */}
          {shot === 2 && (
            <div
              style={{
                width: "100%",
                height: "100%",
                position: "relative",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                transformStyle: "preserve-3d",
              }}
            >
              <div
                style={{
                  width: 1020,
                  height: 1180,
                  position: "relative",
                  transformStyle: "preserve-3d",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                {/* Back Assembly Layer */}
                <div
                  style={{
                    position: "absolute",
                    width: 950,
                    height: 940,
                    transform: `translateZ(${manifoldZ}px) translateY(${manifoldY}px) rotateY(${Math.sin(shotRel * 0.08) * 8}deg)`,
                    opacity: 0.95,
                    filter: "drop-shadow(0 25px 50px rgba(0, 229, 255, 0.35))",
                  }}
                >
                  <Img
                    src={staticFile("captured_proofs/wheresryan22_anatomy/raptor-engine-apart.webp")}
                    style={{
                      width: "100%",
                      height: "100%",
                      objectFit: "contain",
                    }}
                  />
                </div>

                {/* Foreground Nozzle Layer */}
                <div
                  style={{
                    position: "absolute",
                    width: 950,
                    height: 940,
                    transform: `translateZ(${nozzleZ}px) translateY(${nozzleY}px) rotateY(${-Math.sin(shotRel * 0.08) * 8}deg)`,
                    opacity: 0.95,
                  }}
                >
                  <Img
                    src={staticFile("captured_proofs/wheresryan22_anatomy/raptor-engine-apart.webp")}
                    style={{
                      width: "100%",
                      height: "100%",
                      objectFit: "contain",
                      clipPath: "inset(46% 0 0 0)",
                      filter: "drop-shadow(0 30px 60px rgba(0, 229, 255, 0.5))",
                    }}
                  />
                </div>

                {/* Animated Connecting Callout Lines */}
                <svg
                  width="100%"
                  height="100%"
                  style={{
                    position: "absolute",
                    inset: 0,
                    pointerEvents: "none",
                    transform: "translateZ(90px)",
                  }}
                >
                  <line
                    x1="280"
                    y1={240 + manifoldY}
                    x2="100"
                    y2="200"
                    stroke="#00E5FF"
                    strokeWidth="3"
                    strokeDasharray="6 4"
                  />
                  <circle cx="280" cy={240 + manifoldY} r="6" fill="#00E5FF" />
                  <circle cx="100" cy="200" r="6" fill="#00E5FF" />

                  <line
                    x1="700"
                    y1="510"
                    x2="880"
                    y2="470"
                    stroke="#00E5FF"
                    strokeWidth="3"
                    strokeDasharray="6 4"
                  />
                  <circle cx="700" cy="510" r="6" fill="#00E5FF" />
                  <circle cx="880" cy="470" r="6" fill="#00E5FF" />

                  <line
                    x1="480"
                    y1={740 + nozzleY}
                    x2="820"
                    y2="840"
                    stroke="#00E5FF"
                    strokeWidth="3"
                    strokeDasharray="6 4"
                  />
                  <circle cx="480" cy={740 + nozzleY} r="6" fill="#00E5FF" />
                  <circle cx="820" cy="840" r="6" fill="#00E5FF" />
                </svg>

                {/* Floating Labels */}
                <div
                  style={{
                    position: "absolute",
                    left: 20,
                    top: 160,
                    transform: "translateZ(110px)",
                    backgroundColor: "rgba(4, 18, 23, 0.94)",
                    border: "2px solid #00E5FF",
                    borderRadius: 12,
                    padding: "12px 24px",
                    boxShadow: "0 10px 35px rgba(0, 229, 255, 0.4)",
                  }}
                >
                  <div style={{ fontFamily: "'Courier New', monospace", fontSize: 26, fontWeight: 800, color: "#00E5FF" }}>
                    PREBURNER INJECTOR
                  </div>
                  <div style={{ fontSize: 20, color: "#FFFFFF", fontWeight: 600 }}>
                    PRESSURE: 300 BAR
                  </div>
                </div>

                <div
                  style={{
                    position: "absolute",
                    right: 20,
                    top: 430,
                    transform: "translateZ(110px)",
                    backgroundColor: "rgba(4, 18, 23, 0.94)",
                    border: "2px solid #00E5FF",
                    borderRadius: 12,
                    padding: "12px 24px",
                    boxShadow: "0 10px 35px rgba(0, 229, 255, 0.4)",
                  }}
                >
                  <div style={{ fontFamily: "'Courier New', monospace", fontSize: 26, fontWeight: 800, color: "#00E5FF" }}>
                    DUAL TURBOPUMP
                  </div>
                  <div style={{ fontSize: 20, color: "#FFFFFF", fontWeight: 600 }}>
                    CH4 + LOX 100k RPM
                  </div>
                </div>

                <div
                  style={{
                    position: "absolute",
                    right: 40,
                    bottom: 180,
                    transform: "translateZ(110px)",
                    backgroundColor: "rgba(4, 18, 23, 0.94)",
                    border: "2px solid #00E5FF",
                    borderRadius: 12,
                    padding: "12px 24px",
                    boxShadow: "0 10px 35px rgba(0, 229, 255, 0.4)",
                  }}
                >
                  <div style={{ fontFamily: "'Courier New', monospace", fontSize: 26, fontWeight: 800, color: "#00E5FF" }}>
                    REGENERATIVE NOZZLE
                  </div>
                  <div style={{ fontSize: 20, color: "#FFFFFF", fontWeight: 600 }}>
                    EXPANSION RATIO 40:1
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* SHOT 3: MONOSPACE COMMAND & ROTATING SVG DIAL */}
          {shot === 3 && (
            <div
              style={{
                width: "100%",
                height: "100%",
                position: "relative",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              {/* Terminal Command Card (fills upper stage) */}
              <div
                style={{
                  width: 1000,
                  borderRadius: 24,
                  backgroundColor: "rgba(4, 20, 28, 0.96)",
                  border: "2.5px solid #00E5FF",
                  boxShadow: "0 25px 60px rgba(0, 0, 0, 0.8), 0 0 50px rgba(0, 229, 255, 0.35)",
                  padding: "36px 40px",
                  marginBottom: 24,
                  display: "flex",
                  flexDirection: "column",
                  gap: 18,
                }}
              >
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                  <div style={{ display: "flex", gap: 12 }}>
                    <div style={{ width: 18, height: 18, borderRadius: "50%", backgroundColor: "#EF4444" }} />
                    <div style={{ width: 18, height: 18, borderRadius: "50%", backgroundColor: "#F59E0B" }} />
                    <div style={{ width: 18, height: 18, borderRadius: "50%", backgroundColor: "#10B981" }} />
                  </div>
                  <div style={{ fontFamily: "'Courier New', monospace", fontSize: 24, color: "#00E5FF", fontWeight: 700 }}>
                    TERMINAL // CLAUDE CODE SKILL
                  </div>
                </div>

                <div
                  style={{
                    fontFamily: "'Courier New', monospace",
                    fontSize: 48,
                    fontWeight: 800,
                    color: "#FFFFFF",
                    display: "flex",
                    alignItems: "center",
                    flexWrap: "wrap",
                    minHeight: 60,
                  }}
                >
                  <span style={{ color: "#00E5FF", marginRight: 16 }}>$</span>
                  <span>{commandDisplay}</span>
                  <span
                    style={{
                      display: "inline-block",
                      width: 14,
                      height: 48,
                      backgroundColor: "#00E5FF",
                      marginLeft: 8,
                      opacity: Math.sin(frame * 0.4) > 0 ? 1 : 0,
                    }}
                  />
                </div>
              </div>

              {/* Working Isometric Diagram Graphic (fills lower stage) */}
              <div
                style={{
                  width: 1000,
                  height: 720,
                  borderRadius: 24,
                  backgroundColor: "rgba(5, 24, 32, 0.94)",
                  border: "2px solid rgba(0, 229, 255, 0.45)",
                  boxShadow: "0 25px 60px rgba(0, 0, 0, 0.7), 0 0 40px rgba(0, 229, 255, 0.2)",
                  position: "relative",
                  overflow: "hidden",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-around",
                  padding: 24,
                }}
              >
                <div style={{ width: 480, height: 480, position: "relative" }}>
                  <Img
                    src={staticFile("captured_proofs/wheresryan22_anatomy/turning-dial.webp")}
                    style={{
                      width: "100%",
                      height: "100%",
                      objectFit: "contain",
                      transform: `rotate(${frame * 3.5}deg)`,
                    }}
                  />
                </div>
                <div style={{ width: 480, height: 480, position: "relative" }}>
                  <Img
                    src={staticFile("captured_proofs/wheresryan22_anatomy/dial-indicator.webp")}
                    style={{
                      width: "100%",
                      height: "100%",
                      objectFit: "contain",
                      transform: `scale(${1.0 + Math.sin(frame * 0.12) * 0.08})`,
                    }}
                  />
                </div>

                <div
                  style={{
                    position: "absolute",
                    bottom: 24,
                    left: "50%",
                    transform: "translateX(-50%)",
                    backgroundColor: "rgba(0, 229, 255, 0.20)",
                    border: "1.5px solid #00E5FF",
                    borderRadius: 30,
                    padding: "12px 36px",
                    fontFamily: "'Courier New', monospace",
                    fontSize: 26,
                    color: "#00E5FF",
                    fontWeight: 800,
                    boxShadow: "0 0 25px rgba(0, 229, 255, 0.4)",
                  }}
                >
                  AUTONOMOUS SVG + 3D PIPELINE
                </div>
              </div>
            </div>
          )}

          {/* SHOT 4: END CARD PAYOFF (Fills 75% of Frame with Active 3D Brand Motion) */}
          {shot === 4 && (
            <div
              style={{
                width: "100%",
                height: "100%",
                position: "relative",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <div
                style={{
                  width: 1020,
                  height: 1180,
                  borderRadius: 32,
                  background: "linear-gradient(180deg, rgba(11, 45, 58, 0.96) 0%, rgba(4, 18, 24, 0.98) 100%)",
                  border: "2.5px solid #00E5FF",
                  boxShadow: "0 35px 90px rgba(0, 0, 0, 0.85), 0 0 80px rgba(0, 229, 255, 0.4)",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  padding: "50px 40px",
                  position: "relative",
                  overflow: "hidden",
                }}
              >
                {/* Active Rotating Radar Wave in Background of End Card */}
                <div
                  style={{
                    position: "absolute",
                    width: 750,
                    height: 750,
                    borderRadius: "50%",
                    border: "2.5px dashed rgba(0, 229, 255, 0.55)",
                    transform: `rotate(${frame * 2}deg) scale(${1.0 + ((frame * 2) % 60) / 40})`,
                    opacity: 1.0 - ((frame * 2) % 60) / 60,
                    pointerEvents: "none",
                  }}
                />

                {/* 3D Rotating Brand Logo Pedestal */}
                <div
                  style={{
                    width: 170,
                    height: 170,
                    borderRadius: 36,
                    overflow: "hidden",
                    border: "3.5px solid #00E5FF",
                    boxShadow: "0 0 50px rgba(0, 229, 255, 0.7)",
                    marginBottom: 28,
                    transform: `rotateY(${Math.sin(shotRel * 0.25) * 22}deg) scale(${1.0 + Math.sin(shotRel * 0.15) * 0.06})`,
                  }}
                >
                  <Img
                    src={staticFile("assets/brand/logo.png")}
                    style={{ width: "100%", height: "100%", objectFit: "cover" }}
                  />
                </div>

                <div
                  style={{
                    fontSize: 120,
                    fontWeight: 900,
                    letterSpacing: -2,
                    color: "#FFFFFF",
                    lineHeight: 1.0,
                    marginBottom: 16,
                  }}
                >
                  FLASH<span style={{ color: "#00E5FF" }}>.Ai</span>
                </div>

                <div
                  style={{
                    fontSize: 42,
                    fontWeight: 700,
                    color: "rgba(255, 255, 255, 0.9)",
                    letterSpacing: 3,
                    marginBottom: 36,
                  }}
                >
                  DAILY AI INTELLIGENCE
                </div>

                {/* Author & Repo Credentials */}
                <div
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: 16,
                    padding: "26px 40px",
                    borderRadius: 22,
                    backgroundColor: "rgba(0, 229, 255, 0.12)",
                    border: "1.5px solid rgba(0, 229, 255, 0.45)",
                    width: "90%",
                    textAlign: "center",
                  }}
                >
                  <div
                    style={{
                      fontFamily: "'Courier New', monospace",
                      fontSize: 34,
                      fontWeight: 800,
                      color: "#00E5FF",
                    }}
                  >
                    Ryan (@wheresryan22) • MIT License
                  </div>
                  <div
                    style={{
                      fontFamily: "'Courier New', monospace",
                      fontSize: 28,
                      color: "#FFFFFF",
                      fontWeight: 600,
                    }}
                  >
                    github.com/wheresryan22/anatomy
                  </div>
                </div>

                {/* End Card Footer Telemetry */}
                <div
                  style={{
                    marginTop: 32,
                    display: "flex",
                    gap: 30,
                    fontFamily: "'Courier New', monospace",
                    fontSize: 22,
                    color: "rgba(0, 229, 255, 0.8)",
                  }}
                >
                  <span>STARS: <b>25,676</b></span>
                  <span>RELEASE: <b>v1.0</b></span>
                  <span>CLAUDE CODE: <b>READY</b></span>
                </div>
              </div>
            </div>
          )}
        </div>
      </AbsoluteFill>

      {/* ============================================================== */}
      {/* DEPTH LAYER 3: FOREGROUND LAYER (KINETIC HEADLINES & CAPTIONS) */}
      {/* ============================================================== */}
      <AbsoluteFill style={{ pointerEvents: "none" }}>
        {/* Brand Mark: Small FLASH Logo Top-Left */}
        <div
          style={{
            position: "absolute",
            top: 70,
            left: 60,
            display: "flex",
            alignItems: "center",
            gap: 16,
          }}
        >
          <div
            style={{
              width: 58,
              height: 58,
              borderRadius: 14,
              overflow: "hidden",
              border: "2px solid #00E5FF",
              boxShadow: "0 0 25px rgba(0, 229, 255, 0.6)",
            }}
          >
            <Img
              src={staticFile("assets/brand/logo.png")}
              style={{ width: "100%", height: "100%", objectFit: "cover" }}
            />
          </div>
          <span
            style={{
              fontFamily: "'Inter', sans-serif",
              fontSize: 38,
              fontWeight: 900,
              letterSpacing: 2,
              color: "#FFFFFF",
            }}
          >
            FLASH
          </span>
        </div>

        {/* Lower-third source domain */}
        {shot <= 3 && (
          <div
            style={{
              position: "absolute",
              bottom: 80,
              left: 60,
              fontFamily: "'Courier New', monospace",
              fontSize: 24,
              color: "rgba(0, 229, 255, 0.85)",
              letterSpacing: 1.5,
              backgroundColor: "rgba(3, 16, 21, 0.88)",
              padding: "10px 20px",
              borderRadius: 12,
              border: "1.5px solid rgba(0, 229, 255, 0.35)",
            }}
          >
            github.com/wheresryan22/anatomy
          </div>
        )}

        {/* Top Kinetic Headlines (88 - 92px) */}
        {shot === 1 && (
          <div
            style={{
              position: "absolute",
              top: 170,
              left: 60,
              right: 60,
              textAlign: "center",
            }}
          >
            <div
              style={{
                fontSize: 92,
                fontWeight: 900,
                color: "#FFFFFF",
                letterSpacing: -1.5,
                lineHeight: 1.05,
                textShadow: "0 10px 30px rgba(0, 0, 0, 0.8)",
              }}
            >
              MACHINE <span style={{ color: "#00E5FF" }}>BLUEPRINT</span>
            </div>
          </div>
        )}

        {shot === 2 && (
          <div
            style={{
              position: "absolute",
              top: 160,
              left: 60,
              right: 60,
              textAlign: "center",
            }}
          >
            <div
              style={{
                fontSize: 90,
                fontWeight: 900,
                color: "#FFFFFF",
                letterSpacing: -1.5,
                lineHeight: 1.05,
                textShadow: "0 10px 30px rgba(0, 0, 0, 0.8)",
              }}
            >
              EXPLODED <span style={{ color: "#00E5FF" }}>ASSEMBLY</span>
            </div>
          </div>
        )}

        {shot === 3 && (
          <div
            style={{
              position: "absolute",
              top: 160,
              left: 60,
              right: 60,
              textAlign: "center",
            }}
          >
            <div
              style={{
                fontSize: 90,
                fontWeight: 900,
                color: "#FFFFFF",
                letterSpacing: -1.5,
                lineHeight: 1.05,
                textShadow: "0 10px 30px rgba(0, 0, 0, 0.8)",
              }}
            >
              AUTONOMOUS <span style={{ color: "#00E5FF" }}>SVG & 3D</span>
            </div>
          </div>
        )}

        {/* Word-by-Word Pop Captions (>= 58px) */}
        {captionGroup.length > 0 && currentTime < 10.2 && (
          <div
            style={{
              position: "absolute",
              bottom: 140,
              left: 60,
              right: 60,
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              gap: 20,
            }}
          >
            {captionGroup.map((w, idx) => {
              const isActive = activeWord && activeWord.word === w.word;
              return (
                <span
                  key={idx}
                  style={{
                    fontSize: 60,
                    fontWeight: 800,
                    color: isActive ? "#00E5FF" : "#FFFFFF",
                    textShadow: isActive
                      ? "0 0 25px rgba(0, 229, 255, 0.8)"
                      : "0 4px 15px rgba(0, 0, 0, 0.9)",
                    transform: isActive ? "scale(1.12)" : "scale(1.0)",
                    transition: "transform 0.08s ease-out",
                    backgroundColor: "rgba(4, 20, 28, 0.85)",
                    padding: "10px 22px",
                    borderRadius: 14,
                    border: isActive
                      ? "2.5px solid #00E5FF"
                      : "1px solid rgba(255, 255, 255, 0.2)",
                  }}
                >
                  {w.word}
                </span>
              );
            })}
          </div>
        )}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
