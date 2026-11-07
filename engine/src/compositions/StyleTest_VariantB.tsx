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

export const StyleTest_VariantB: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const currentTime = frame / fps;

  // 12-Second Narrative Shots (360 frames @ 30fps)
  // Shot 1: Frames 0 - 96 (0.00s - 3.20s) Wide 3D Drafting Board / Blueprint Assembly
  // Shot 2: Frames 96 - 195 (3.20s - 6.50s) Exploded Drafting View (Wow Beat: Raptor 2 Deconstruction)
  // Shot 3: Frames 195 - 306 (6.50s - 10.20s) Technical Spec Close-up: Monospace Command & Vector Caliper
  // Shot 4: Frames 306 - 360 (10.20s - 12.00s) End Card Payoff: Architectural Blueprint Lockup

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
  const camRotY =
    shot === 1
      ? interpolate(shotRel, [0, 96], [-15, 12])
      : shot === 2
      ? interpolate(shotRel, [0, 99], [12, -16])
      : shot === 3
      ? interpolate(shotRel, [0, 111], [-9, 11])
      : interpolate(shotRel, [0, 54], [-9, 5]);

  const camRotX =
    shot === 1
      ? interpolate(shotRel, [0, 96], [12, 3])
      : shot === 2
      ? interpolate(shotRel, [0, 99], [4, 15])
      : shot === 3
      ? interpolate(shotRel, [0, 111], [14, 5])
      : interpolate(shotRel, [0, 54], [9, 2]);

  const camScale =
    shot === 1
      ? interpolate(shotRel, [0, 96], [1.02, 1.18])
      : shot === 2
      ? interpolate(shotRel, [0, 99], [1.06, 1.23])
      : shot === 3
      ? interpolate(shotRel, [0, 111], [1.13, 1.29])
      : interpolate(shotRel, [0, 54], [1.10, 1.02]);

  // Drafting Light Drift & Laser Bar
  const sweepAngle = (frame * 0.08);
  const draftLightX = 540 + Math.sin(sweepAngle) * 500;
  const draftLightY = 960 + Math.cos(sweepAngle * 0.7) * 450;
  const laserY = (frame * 12) % 1920;

  // Exploded View Spring Physics for Shot 2
  const explodeSpring = spring({
    frame: shotRel,
    fps,
    config: { damping: 12, stiffness: 90, mass: 0.8 },
  });
  const secondaryFloat = Math.sin(shotRel * 0.12) * 25;
  const nozzleZ = interpolate(explodeSpring, [0, 1], [0, 230]) + secondaryFloat;
  const nozzleY = interpolate(explodeSpring, [0, 1], [0, 180]) + secondaryFloat * 0.8;
  const manifoldZ = interpolate(explodeSpring, [0, 1], [0, -210]) - secondaryFloat;
  const manifoldY = interpolate(explodeSpring, [0, 1], [0, -160]) - secondaryFloat * 0.8;

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
        backgroundColor: "#08162A",
        fontFamily: "'Courier New', Courier, monospace",
        color: "#F8FAFC",
        overflow: "hidden",
      }}
    >
      {/* ============================================================== */}
      {/* DEPTH LAYER 1: ANIMATED BLUEPRINT DRAFTING BOARD CANVAS        */}
      {/* ============================================================== */}
      <AbsoluteFill style={{ pointerEvents: "none" }}>
        {/* Dynamic Multi-stop Radial Gradient Mesh */}
        <div
          style={{
            position: "absolute",
            inset: 0,
            background: `radial-gradient(circle 950px at ${draftLightX}px ${draftLightY}px, #10335C 0%, #081B34 50%, #030B17 95%)`,
          }}
        />

        {/* Sepia Drafting Lamp Illumination Glow */}
        <div
          style={{
            position: "absolute",
            width: 1500,
            height: 1000,
            top: -200,
            right: -200 + Math.sin(frame * 0.05) * 120,
            background: "radial-gradient(ellipse at center, rgba(226, 184, 120, 0.22) 0%, rgba(8, 22, 42, 0.0) 70%)",
            filter: "blur(50px)",
          }}
        />

        {/* Dynamic Scanning Laser Bar */}
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            top: laserY,
            height: 3,
            background: "linear-gradient(90deg, transparent 0%, rgba(226, 184, 120, 0.9) 50%, transparent 100%)",
            boxShadow: "0 0 15px #E2B878",
            opacity: 0.65,
          }}
        />

        {/* Millimeter Blueprint Drafting Grid with Crosshairs */}
        <svg
          width="100%"
          height="100%"
          style={{
            position: "absolute",
            inset: 0,
            opacity: 0.35,
          }}
        >
          <defs>
            <pattern
              id="blueprintGrid"
              width="70"
              height="70"
              patternUnits="userSpaceOnUse"
            >
              <path
                d="M 70 0 L 0 0 0 70"
                fill="none"
                stroke="rgba(56, 189, 248, 0.4)"
                strokeWidth="1.2"
              />
              <path
                d="M 35 30 L 35 40 M 30 35 L 40 35"
                stroke="rgba(226, 184, 120, 0.7)"
                strokeWidth="1.2"
              />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#blueprintGrid)" />
        </svg>

        {/* Continuous Active Telemetry Columns along borders */}
        <div
          style={{
            position: "absolute",
            top: 280,
            left: 20,
            fontSize: 16,
            color: "rgba(226, 184, 120, 0.65)",
            lineHeight: 1.8,
            letterSpacing: 2,
          }}
        >
          <div>DWG: ANATOMY-REV2</div>
          <div>ROT_Y: {camRotY.toFixed(1)}°</div>
          <div>ROT_X: {camRotX.toFixed(1)}°</div>
          <div>ZOOM: {camScale.toFixed(2)}x</div>
          <div>DRAFT: 3D-SVG</div>
          <div>SCALE: 1:15</div>
          <div>FRAME: {frame.toString().padStart(4, "0")}</div>
        </div>

        <div
          style={{
            position: "absolute",
            top: 280,
            right: 20,
            textAlign: "right",
            fontSize: 16,
            color: "rgba(226, 184, 120, 0.65)",
            lineHeight: 1.8,
            letterSpacing: 2,
          }}
        >
          <div>SPEC: RAPTOR 2</div>
          <div>STAGED: FULL-FLOW</div>
          <div>CHAMBER: 300 BAR</div>
          <div>EXPANSION: 40:1</div>
          <div>CLAUDE SKILL</div>
          <div>STARS: 25,676</div>
          <div>CAD ENGINE</div>
        </div>

        {/* Vignette */}
        <div
          style={{
            position: "absolute",
            inset: 0,
            boxShadow: "inset 0 0 180px rgba(2, 6, 12, 0.85)",
          }}
        />
      </AbsoluteFill>

      {/* ============================================================== */}
      {/* DEPTH LAYER 2: 3D DRAFTING BOARD HERO ASSET (>= 60% AREA)      */}
      {/* ============================================================== */}
      <AbsoluteFill
        style={{
          perspective: 1200,
          perspectiveOrigin: "50% 50%",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
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
          {/* SHOT 1: WIDE DRAFTING BOARD CAD ASSEMBLY */}
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
                  borderRadius: 22,
                  background: "linear-gradient(180deg, rgba(16, 44, 82, 0.94) 0%, rgba(8, 22, 42, 0.98) 100%)",
                  border: "2.5px solid rgba(226, 184, 120, 0.7)",
                  boxShadow: "0 30px 80px rgba(0, 0, 0, 0.8), 0 0 55px rgba(226, 184, 120, 0.3)",
                  position: "relative",
                  overflow: "hidden",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  padding: 24,
                }}
              >
                {/* Header */}
                <div
                  style={{
                    width: "100%",
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    borderBottom: "1.5px solid rgba(226, 184, 120, 0.5)",
                    paddingBottom: 16,
                    marginBottom: 16,
                  }}
                >
                  <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                    <div
                      style={{
                        width: 16,
                        height: 16,
                        backgroundColor: "#E2B878",
                        transform: "rotate(45deg)",
                        boxShadow: "0 0 12px #E2B878",
                      }}
                    />
                    <span
                      style={{
                        fontSize: 30,
                        color: "#E2B878",
                        fontWeight: 800,
                        letterSpacing: 2,
                      }}
                    >
                      DRAFTING SPEC: RAPTOR 2
                    </span>
                  </div>
                  <span style={{ fontSize: 24, color: "#FFFFFF", fontWeight: 700 }}>
                    ISOMETRIC PROJECTION
                  </span>
                </div>

                {/* Hero Asset */}
                <div
                  style={{
                    width: 950,
                    height: 890,
                    position: "relative",
                    borderRadius: 16,
                    overflow: "hidden",
                    backgroundColor: "#061528",
                    border: "1.5px solid rgba(56, 189, 248, 0.4)",
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

                  {/* Drafting Compass Caliper Overlay */}
                  <div
                    style={{
                      position: "absolute",
                      left: 20,
                      top: 40,
                      borderLeft: "2.5px solid #E2B878",
                      borderTop: "2.5px solid #E2B878",
                      borderBottom: "2.5px solid #E2B878",
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
                        fontSize: 24,
                        color: "#E2B878",
                        fontWeight: 800,
                      }}
                    >
                      NOMINAL LENGTH: 3,120 mm
                    </span>
                  </div>

                  {/* Blueprint Stamp */}
                  <div
                    style={{
                      position: "absolute",
                      right: 24,
                      bottom: 24,
                      backgroundColor: "rgba(8, 22, 42, 0.94)",
                      border: "2px solid #E2B878",
                      borderRadius: 10,
                      padding: "10px 22px",
                      fontSize: 24,
                      color: "#F8FAFC",
                      display: "flex",
                      gap: 20,
                      boxShadow: "0 0 25px rgba(226, 184, 120, 0.35)",
                    }}
                  >
                    <span>COMBUSTION: <b style={{ color: "#E2B878" }}>FULL-FLOW</b></span>
                    <span>THRUST: <b style={{ color: "#E2B878" }}>230 tf</b></span>
                  </div>
                </div>

                {/* Sub-bar */}
                <div
                  style={{
                    width: "100%",
                    display: "flex",
                    justifyContent: "space-between",
                    marginTop: 16,
                    fontSize: 24,
                    color: "rgba(226, 184, 120, 0.9)",
                    fontWeight: 700,
                  }}
                >
                  <span>ENGINEERING BLUEPRINT [AUTONOMOUS]</span>
                  <span>CLAUDE CODE SKILL</span>
                </div>
              </div>
            </div>
          )}

          {/* SHOT 2: EXPLODED VIEW ASSEMBLY (WOW BEAT) */}
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
                    filter: "drop-shadow(0 25px 50px rgba(226, 184, 120, 0.35))",
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
                      filter: "drop-shadow(0 30px 60px rgba(226, 184, 120, 0.45))",
                    }}
                  />
                </div>

                {/* Architectural Drafting Callout Lines */}
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
                    stroke="#E2B878"
                    strokeWidth="3"
                    strokeDasharray="6 4"
                  />
                  <circle cx="280" cy={240 + manifoldY} r="6" fill="#E2B878" />
                  <circle cx="100" cy="200" r="6" fill="#E2B878" />

                  <line
                    x1="700"
                    y1="510"
                    x2="880"
                    y2="470"
                    stroke="#E2B878"
                    strokeWidth="3"
                    strokeDasharray="6 4"
                  />
                  <circle cx="700" cy="510" r="6" fill="#E2B878" />
                  <circle cx="880" cy="470" r="6" fill="#E2B878" />

                  <line
                    x1="480"
                    y1={740 + nozzleY}
                    x2="820"
                    y2="840"
                    stroke="#E2B878"
                    strokeWidth="3"
                    strokeDasharray="6 4"
                  />
                  <circle cx="480" cy={740 + nozzleY} r="6" fill="#E2B878" />
                  <circle cx="820" cy="840" r="6" fill="#E2B878" />
                </svg>

                {/* Drafting Callout Cards */}
                <div
                  style={{
                    position: "absolute",
                    left: 20,
                    top: 160,
                    transform: "translateZ(110px)",
                    backgroundColor: "rgba(8, 22, 42, 0.95)",
                    border: "2px solid #E2B878",
                    borderRadius: 12,
                    padding: "12px 24px",
                    boxShadow: "0 10px 35px rgba(0, 0, 0, 0.7)",
                  }}
                >
                  <div style={{ fontSize: 26, fontWeight: 800, color: "#E2B878" }}>
                    [PART-01] INJECTOR DOME
                  </div>
                  <div style={{ fontSize: 20, color: "#FFFFFF", fontWeight: 600 }}>
                    STAGED PRESSURE: 300 BAR
                  </div>
                </div>

                <div
                  style={{
                    position: "absolute",
                    right: 20,
                    top: 430,
                    transform: "translateZ(110px)",
                    backgroundColor: "rgba(8, 22, 42, 0.95)",
                    border: "2px solid #E2B878",
                    borderRadius: 12,
                    padding: "12px 24px",
                    boxShadow: "0 10px 35px rgba(0, 0, 0, 0.7)",
                  }}
                >
                  <div style={{ fontSize: 26, fontWeight: 800, color: "#E2B878" }}>
                    [PART-02] DUAL TURBOPUMP
                  </div>
                  <div style={{ fontSize: 20, color: "#FFFFFF", fontWeight: 600 }}>
                    SYNCHRONOUS ROTOR
                  </div>
                </div>

                <div
                  style={{
                    position: "absolute",
                    right: 40,
                    bottom: 180,
                    transform: "translateZ(110px)",
                    backgroundColor: "rgba(8, 22, 42, 0.95)",
                    border: "2px solid #E2B878",
                    borderRadius: 12,
                    padding: "12px 24px",
                    boxShadow: "0 10px 35px rgba(0, 0, 0, 0.7)",
                  }}
                >
                  <div style={{ fontSize: 26, fontWeight: 800, color: "#E2B878" }}>
                    [PART-03] REGEN NOZZLE
                  </div>
                  <div style={{ fontSize: 20, color: "#FFFFFF", fontWeight: 600 }}>
                    MILLING CHANNELS: 1,080
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* SHOT 3: MONOSPACE COMMAND & ROTATING VECTOR DIAL */}
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
              {/* Terminal Blueprint Card */}
              <div
                style={{
                  width: 1000,
                  borderRadius: 22,
                  backgroundColor: "rgba(8, 24, 46, 0.96)",
                  border: "2.5px solid #E2B878",
                  boxShadow: "0 25px 60px rgba(0, 0, 0, 0.8), 0 0 50px rgba(226, 184, 120, 0.35)",
                  padding: "36px 40px",
                  marginBottom: 24,
                  display: "flex",
                  flexDirection: "column",
                  gap: 18,
                }}
              >
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                  <span style={{ fontSize: 26, color: "#E2B878", fontWeight: 800 }}>
                    // SKILL INSTALLATION COMMAND
                  </span>
                  <span style={{ fontSize: 22, color: "#FFFFFF", fontWeight: 600 }}>
                    SHELL: BASH
                  </span>
                </div>

                <div
                  style={{
                    fontSize: 48,
                    fontWeight: 800,
                    color: "#FFFFFF",
                    display: "flex",
                    alignItems: "center",
                    flexWrap: "wrap",
                    minHeight: 60,
                  }}
                >
                  <span style={{ color: "#E2B878", marginRight: 16 }}>&gt;</span>
                  <span>{commandDisplay}</span>
                  <span
                    style={{
                      display: "inline-block",
                      width: 14,
                      height: 48,
                      backgroundColor: "#E2B878",
                      marginLeft: 8,
                      opacity: Math.sin(frame * 0.4) > 0 ? 1 : 0,
                    }}
                  />
                </div>
              </div>

              {/* Vector Blueprint Visualizer */}
              <div
                style={{
                  width: 1000,
                  height: 720,
                  borderRadius: 22,
                  backgroundColor: "rgba(10, 30, 58, 0.94)",
                  border: "2px solid rgba(226, 184, 120, 0.5)",
                  boxShadow: "0 25px 60px rgba(0, 0, 0, 0.7), 0 0 40px rgba(226, 184, 120, 0.2)",
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
                      filter: "sepia(0.6) hue-rotate(180deg)",
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
                      filter: "sepia(0.6) hue-rotate(180deg)",
                    }}
                  />
                </div>

                <div
                  style={{
                    position: "absolute",
                    bottom: 24,
                    left: "50%",
                    transform: "translateX(-50%)",
                    backgroundColor: "rgba(8, 22, 42, 0.94)",
                    border: "2px solid #E2B878",
                    borderRadius: 30,
                    padding: "12px 36px",
                    fontSize: 26,
                    color: "#E2B878",
                    fontWeight: 800,
                    boxShadow: "0 0 25px rgba(226, 184, 120, 0.4)",
                  }}
                >
                  AUTONOMOUS CAD & ISOMETRIC SVG
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
                  borderRadius: 30,
                  background: "linear-gradient(180deg, rgba(16, 44, 82, 0.96) 0%, rgba(8, 22, 42, 0.98) 100%)",
                  border: "2.5px solid #E2B878",
                  boxShadow: "0 35px 90px rgba(0, 0, 0, 0.85), 0 0 80px rgba(226, 184, 120, 0.35)",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  padding: "50px 40px",
                  position: "relative",
                  overflow: "hidden",
                }}
              >
                {/* Active Rotating Blueprint Ring */}
                <div
                  style={{
                    position: "absolute",
                    width: 700,
                    height: 700,
                    borderRadius: "50%",
                    border: "2px dashed rgba(226, 184, 120, 0.4)",
                    transform: `rotate(${frame * 2}deg) scale(${1.0 + ((frame * 2) % 60) / 40})`,
                    opacity: 1.0 - ((frame * 2) % 60) / 60,
                    pointerEvents: "none",
                  }}
                />

                {/* Brand Logo with 3D Motion */}
                <div
                  style={{
                    width: 170,
                    height: 170,
                    borderRadius: 32,
                    overflow: "hidden",
                    border: "3.5px solid #E2B878",
                    boxShadow: "0 0 50px rgba(226, 184, 120, 0.6)",
                    marginBottom: 28,
                    transform: `rotateY(${Math.sin(shotRel * 0.15) * 16}deg) scale(${1.0 + Math.sin(shotRel * 0.1) * 0.04})`,
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
                  FLASH<span style={{ color: "#E2B878" }}>.Ai</span>
                </div>

                <div
                  style={{
                    fontSize: 42,
                    fontWeight: 700,
                    color: "rgba(248, 250, 252, 0.9)",
                    letterSpacing: 3,
                    marginBottom: 36,
                  }}
                >
                  DAILY AI INTELLIGENCE
                </div>

                <div
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: 16,
                    padding: "26px 40px",
                    borderRadius: 20,
                    backgroundColor: "rgba(226, 184, 120, 0.12)",
                    border: "1.5px solid rgba(226, 184, 120, 0.45)",
                    width: "90%",
                    textAlign: "center",
                  }}
                >
                  <div style={{ fontSize: 34, fontWeight: 800, color: "#E2B878" }}>
                    Ryan (@wheresryan22) • MIT License
                  </div>
                  <div style={{ fontSize: 28, color: "#FFFFFF", fontWeight: 600 }}>
                    github.com/wheresryan22/anatomy
                  </div>
                </div>

                {/* Footer Telemetry */}
                <div
                  style={{
                    marginTop: 32,
                    display: "flex",
                    gap: 30,
                    fontSize: 22,
                    color: "rgba(226, 184, 120, 0.85)",
                  }}
                >
                  <span>STARS: <b>25,676</b></span>
                  <span>LICENSE: <b>MIT</b></span>
                  <span>VERIFIED: <b>RAW API</b></span>
                </div>
              </div>
            </div>
          )}
        </div>
      </AbsoluteFill>

      {/* ============================================================== */}
      {/* DEPTH LAYER 3: FOREGROUND KINETIC HEADLINES & CAPTIONS         */}
      {/* ============================================================== */}
      <AbsoluteFill style={{ pointerEvents: "none" }}>
        {/* FLASH Logo Mark Top-Left */}
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
              border: "2px solid #E2B878",
              boxShadow: "0 0 25px rgba(226, 184, 120, 0.55)",
            }}
          >
            <Img
              src={staticFile("assets/brand/logo.png")}
              style={{ width: "100%", height: "100%", objectFit: "cover" }}
            />
          </div>
          <span
            style={{
              fontSize: 38,
              fontWeight: 900,
              letterSpacing: 2,
              color: "#F8FAFC",
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
              fontSize: 24,
              color: "rgba(226, 184, 120, 0.9)",
              letterSpacing: 1.5,
              backgroundColor: "rgba(8, 22, 42, 0.90)",
              padding: "10px 20px",
              borderRadius: 10,
              border: "1.5px solid rgba(226, 184, 120, 0.4)",
            }}
          >
            github.com/wheresryan22/anatomy
          </div>
        )}

        {/* Top Kinetic Headlines */}
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
                fontSize: 90,
                fontWeight: 900,
                color: "#FFFFFF",
                letterSpacing: -1.5,
                lineHeight: 1.05,
                textShadow: "0 10px 30px rgba(0, 0, 0, 0.8)",
              }}
            >
              BLUEPRINT <span style={{ color: "#E2B878" }}>DRAFTING</span>
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
                fontSize: 88,
                fontWeight: 900,
                color: "#FFFFFF",
                letterSpacing: -1.5,
                lineHeight: 1.05,
                textShadow: "0 10px 30px rgba(0, 0, 0, 0.8)",
              }}
            >
              DECONSTRUCTED <span style={{ color: "#E2B878" }}>VIEW</span>
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
                fontSize: 88,
                fontWeight: 900,
                color: "#FFFFFF",
                letterSpacing: -1.5,
                lineHeight: 1.05,
                textShadow: "0 10px 30px rgba(0, 0, 0, 0.8)",
              }}
            >
              ISOMETRIC <span style={{ color: "#E2B878" }}>DIAGRAMS</span>
            </div>
          </div>
        )}

        {/* Word-by-Word Pop Captions */}
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
                    fontSize: 58,
                    fontWeight: 800,
                    color: isActive ? "#E2B878" : "#F8FAFC",
                    textShadow: isActive
                      ? "0 0 25px rgba(226, 184, 120, 0.8)"
                      : "0 4px 15px rgba(0, 0, 0, 0.9)",
                    transform: isActive ? "scale(1.12)" : "scale(1.0)",
                    transition: "transform 0.08s ease-out",
                    backgroundColor: "rgba(8, 22, 42, 0.90)",
                    padding: "10px 22px",
                    borderRadius: 12,
                    border: isActive
                      ? "2.5px solid #E2B878"
                      : "1px solid rgba(226, 184, 120, 0.3)",
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
