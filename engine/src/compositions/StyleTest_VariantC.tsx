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

export const StyleTest_VariantC: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const currentTime = frame / fps;

  // 12-Second Narrative Shots (360 frames @ 30fps)
  // Shot 1: Frames 0 - 96 (0.00s - 3.20s) Wide Museum Vitrine Exhibition
  // Shot 2: Frames 96 - 195 (3.20s - 6.50s) Exploded Museum Vitrine View (Wow Beat: Floating Precision Artifact)
  // Shot 3: Frames 195 - 306 (6.50s - 10.20s) Precision Terminal & Dynamic Vector Calibration
  // Shot 4: Frames 306 - 360 (10.20s - 12.00s) End Card Payoff: Museum Gallery Pedestal Lockup

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
      ? interpolate(shotRel, [0, 96], [-16, 14])
      : shot === 2
      ? interpolate(shotRel, [0, 99], [14, -18])
      : shot === 3
      ? interpolate(shotRel, [0, 111], [-10, 12])
      : interpolate(shotRel, [0, 54], [-12, 8]);

  const camRotX =
    shot === 1
      ? interpolate(shotRel, [0, 96], [12, 3])
      : shot === 2
      ? interpolate(shotRel, [0, 99], [4, 16])
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

  // Soft directional studio key light position & laser bar
  const sweepAngle = (frame * 0.08);
  const keyLightX = 540 + Math.sin(sweepAngle) * 500;
  const keyLightY = 960 + Math.cos(sweepAngle * 0.7) * 450;
  const laserY = (frame * 12) % 1920;

  // Exploded View Spring Physics for Shot 2
  const explodeSpring = spring({
    frame: shotRel,
    fps,
    config: { damping: 12, stiffness: 90, mass: 0.8 },
  });
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
        backgroundColor: "#E2E8F0",
        fontFamily: "'Inter', -apple-system, sans-serif",
        color: "#0F172A",
        overflow: "hidden",
      }}
    >
      {/* ============================================================== */}
      {/* DEPTH LAYER 1: LUMINOUS MUSEUM GALLERY ENVIRONMENT             */}
      {/* ============================================================== */}
      <AbsoluteFill style={{ pointerEvents: "none" }}>
        {/* Luminous Gallery Studio Wall Multi-stop Radial Gradient */}
        <div
          style={{
            position: "absolute",
            inset: 0,
            background: `radial-gradient(circle 950px at ${keyLightX}px ${keyLightY}px, #FFFFFF 0%, #E2E8F0 50%, #CBD5E1 95%)`,
          }}
        />

        {/* Directional Studio Key Light Shaft */}
        <div
          style={{
            position: "absolute",
            width: 1500,
            height: 1000,
            top: -200,
            left: -150 + Math.sin(frame * 0.05) * 100,
            background: "linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(203, 213, 225, 0.0) 70%)",
            transform: `rotate(${-20 + Math.sin(frame * 0.04) * 8}deg)`,
            filter: "blur(40px)",
          }}
        />

        {/* Dynamic Scanning Emerald Precision Laser Bar */}
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            top: laserY,
            height: 3,
            background: "linear-gradient(90deg, transparent 0%, rgba(5, 150, 105, 0.8) 50%, transparent 100%)",
            boxShadow: "0 0 12px #059669",
            opacity: 0.55,
          }}
        />

        {/* Architectural Precision Dots & Measurement Grid with Crosshairs */}
        <svg
          width="100%"
          height="100%"
          style={{
            position: "absolute",
            inset: 0,
            opacity: 0.45,
          }}
        >
          <defs>
            <pattern
              id="museumGrid"
              width="60"
              height="60"
              patternUnits="userSpaceOnUse"
            >
              <circle cx="30" cy="30" r="2.5" fill="#334155" />
              <path
                d="M 60 0 L 0 0 0 60"
                fill="none"
                stroke="rgba(100, 116, 139, 0.45)"
                strokeWidth="1.2"
              />
              <path
                d="M 30 25 L 30 35 M 25 30 L 35 30"
                stroke="rgba(5, 150, 105, 0.85)"
                strokeWidth="1.3"
              />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#museumGrid)" />
        </svg>

        {/* Continuous Active Telemetry Columns along borders */}
        <div
          style={{
            position: "absolute",
            top: 280,
            left: 20,
            fontFamily: "'Courier New', monospace",
            fontSize: 16,
            color: "#475569",
            lineHeight: 1.8,
            letterSpacing: 2,
            fontWeight: 700,
          }}
        >
          <div>GALLERY: 04</div>
          <div>ROT_Y: {camRotY.toFixed(1)}°</div>
          <div>ROT_X: {camRotX.toFixed(1)}°</div>
          <div>ZOOM: {camScale.toFixed(2)}x</div>
          <div>SPECIMEN: ANATOMY</div>
          <div>CAD ENGINE: ACTIVE</div>
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
            color: "#475569",
            lineHeight: 1.8,
            letterSpacing: 2,
            fontWeight: 700,
          }}
        >
          <div>SPEC: RAPTOR 2</div>
          <div>EXHIBIT: 3D SVG</div>
          <div>CHAMBER: 300 BAR</div>
          <div>THRUST: 230 TF</div>
          <div>CLAUDE SKILL</div>
          <div>STARS: 25,676</div>
          <div>MIT LICENSE</div>
        </div>

        {/* Ambient Floor Shadow */}
        <div
          style={{
            position: "absolute",
            bottom: -60,
            left: "5%",
            right: "5%",
            height: 220,
            borderRadius: "50%",
            background: "radial-gradient(ellipse at center, rgba(15, 23, 42, 0.25) 0%, rgba(226, 232, 240, 0.0) 70%)",
            filter: "blur(35px)",
          }}
        />
      </AbsoluteFill>

      {/* ============================================================== */}
      {/* DEPTH LAYER 2: 3D FROSTED ACRYLIC VITRINE PEDESTAL (>=60% AREA)*/}
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
          {/* SHOT 1: WIDE VITRINE DISPLAY */}
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
                  borderRadius: 28,
                  background: "linear-gradient(180deg, rgba(255, 255, 255, 0.96) 0%, rgba(241, 245, 249, 0.92) 100%)",
                  border: "2.5px solid rgba(255, 255, 255, 0.95)",
                  boxShadow: "0 30px 80px rgba(15, 23, 42, 0.16), 0 0 20px rgba(5, 150, 105, 0.12)",
                  backdropFilter: "blur(20px)",
                  position: "relative",
                  overflow: "hidden",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  padding: 24,
                }}
              >
                {/* Plaque Header */}
                <div
                  style={{
                    width: "100%",
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    borderBottom: "1.5px solid rgba(15, 23, 42, 0.12)",
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
                        backgroundColor: "#059669",
                        boxShadow: "0 0 10px #059669",
                      }}
                    />
                    <span
                      style={{
                        fontSize: 30,
                        color: "#0F172A",
                        fontWeight: 900,
                        letterSpacing: 1.5,
                      }}
                    >
                      RAPTOR 2 // SPECIMEN NO. 01
                    </span>
                  </div>
                  <span
                    style={{
                      fontFamily: "'Courier New', monospace",
                      fontSize: 24,
                      color: "#475569",
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
                    backgroundColor: "#F8FAFC",
                    border: "1.5px solid rgba(15, 23, 42, 0.10)",
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

                  {/* Caliper Brackets */}
                  <div
                    style={{
                      position: "absolute",
                      left: 20,
                      top: 40,
                      borderLeft: "2.5px solid #059669",
                      borderTop: "2.5px solid #059669",
                      borderBottom: "2.5px solid #059669",
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
                        color: "#059669",
                        fontWeight: 800,
                      }}
                    >
                      DIMENSION: 3,120 mm
                    </span>
                  </div>

                  {/* Plaque */}
                  <div
                    style={{
                      position: "absolute",
                      right: 24,
                      bottom: 24,
                      backgroundColor: "rgba(255, 255, 255, 0.98)",
                      border: "1.5px solid #059669",
                      borderRadius: 12,
                      padding: "10px 22px",
                      fontFamily: "'Courier New', monospace",
                      fontSize: 24,
                      color: "#0F172A",
                      display: "flex",
                      gap: 20,
                      boxShadow: "0 8px 20px rgba(15, 23, 42, 0.12)",
                    }}
                  >
                    <span>THRUST: <b style={{ color: "#059669" }}>230 tf</b></span>
                    <span>PROPELLANT: <b style={{ color: "#059669" }}>CH4+LOX</b></span>
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
                    color: "#475569",
                    fontWeight: 700,
                  }}
                >
                  <span>MUSEUM ARTIFACT: ISOMETRIC CAD</span>
                  <span>AUTONOMOUS ENGINE VIEW</span>
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
                    filter: "drop-shadow(0 25px 50px rgba(15, 23, 42, 0.18))",
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
                      filter: "drop-shadow(0 30px 60px rgba(15, 23, 42, 0.22))",
                    }}
                  />
                </div>

                {/* Precision Emerald Connecting Lines */}
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
                    stroke="#059669"
                    strokeWidth="3"
                    strokeDasharray="6 4"
                  />
                  <circle cx="280" cy={240 + manifoldY} r="6" fill="#059669" />
                  <circle cx="100" cy="200" r="6" fill="#059669" />

                  <line
                    x1="700"
                    y1="510"
                    x2="880"
                    y2="470"
                    stroke="#059669"
                    strokeWidth="3"
                    strokeDasharray="6 4"
                  />
                  <circle cx="700" cy="510" r="6" fill="#059669" />
                  <circle cx="880" cy="470" r="6" fill="#059669" />

                  <line
                    x1="480"
                    y1={740 + nozzleY}
                    x2="820"
                    y2="840"
                    stroke="#059669"
                    strokeWidth="3"
                    strokeDasharray="6 4"
                  />
                  <circle cx="480" cy={740 + nozzleY} r="6" fill="#059669" />
                  <circle cx="820" cy="840" r="6" fill="#059669" />
                </svg>

                {/* Vitrine Labels */}
                <div
                  style={{
                    position: "absolute",
                    left: 20,
                    top: 160,
                    transform: "translateZ(110px)",
                    backgroundColor: "rgba(255, 255, 255, 0.98)",
                    border: "2px solid #059669",
                    borderRadius: 12,
                    padding: "12px 24px",
                    boxShadow: "0 10px 35px rgba(15, 23, 42, 0.16)",
                  }}
                >
                  <div style={{ fontFamily: "'Inter', sans-serif", fontSize: 26, fontWeight: 900, color: "#0F172A" }}>
                    INJECTOR ASSEMBLY
                  </div>
                  <div style={{ fontSize: 20, color: "#059669", fontWeight: 700 }}>
                    PRESSURE: 300 BAR
                  </div>
                </div>

                <div
                  style={{
                    position: "absolute",
                    right: 20,
                    top: 430,
                    transform: "translateZ(110px)",
                    backgroundColor: "rgba(255, 255, 255, 0.98)",
                    border: "2px solid #059669",
                    borderRadius: 12,
                    padding: "12px 24px",
                    boxShadow: "0 10px 35px rgba(15, 23, 42, 0.16)",
                  }}
                >
                  <div style={{ fontFamily: "'Inter', sans-serif", fontSize: 26, fontWeight: 900, color: "#0F172A" }}>
                    DUAL TURBOPUMP
                  </div>
                  <div style={{ fontSize: 20, color: "#059669", fontWeight: 700 }}>
                    100,000 RPM DRIVE
                  </div>
                </div>

                <div
                  style={{
                    position: "absolute",
                    right: 40,
                    bottom: 180,
                    transform: "translateZ(110px)",
                    backgroundColor: "rgba(255, 255, 255, 0.98)",
                    border: "2px solid #059669",
                    borderRadius: 12,
                    padding: "12px 24px",
                    boxShadow: "0 10px 35px rgba(15, 23, 42, 0.16)",
                  }}
                >
                  <div style={{ fontFamily: "'Inter', sans-serif", fontSize: 26, fontWeight: 900, color: "#0F172A" }}>
                    REGENERATIVE NOZZLE
                  </div>
                  <div style={{ fontSize: 20, color: "#059669", fontWeight: 700 }}>
                    COPPER INCONEL
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
              {/* Terminal Vitrine Card */}
              <div
                style={{
                  width: 1000,
                  borderRadius: 24,
                  backgroundColor: "rgba(255, 255, 255, 0.98)",
                  border: "2.5px solid #059669",
                  boxShadow: "0 25px 60px rgba(15, 23, 42, 0.16)",
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
                  <div style={{ fontFamily: "'Courier New', monospace", fontSize: 24, color: "#059669", fontWeight: 800 }}>
                    CLAUDE CODE // TERMINAL SKILL
                  </div>
                </div>

                <div
                  style={{
                    fontFamily: "'Courier New', monospace",
                    fontSize: 48,
                    fontWeight: 800,
                    color: "#0F172A",
                    display: "flex",
                    alignItems: "center",
                    flexWrap: "wrap",
                    minHeight: 60,
                  }}
                >
                  <span style={{ color: "#059669", marginRight: 16 }}>$</span>
                  <span>{commandDisplay}</span>
                  <span
                    style={{
                      display: "inline-block",
                      width: 14,
                      height: 48,
                      backgroundColor: "#059669",
                      marginLeft: 8,
                      opacity: Math.sin(frame * 0.4) > 0 ? 1 : 0,
                    }}
                  />
                </div>
              </div>

              {/* Museum Vector Visualizer */}
              <div
                style={{
                  width: 1000,
                  height: 720,
                  borderRadius: 24,
                  backgroundColor: "rgba(255, 255, 255, 0.94)",
                  border: "2px solid rgba(15, 23, 42, 0.12)",
                  boxShadow: "0 25px 60px rgba(15, 23, 42, 0.10)",
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
                    backgroundColor: "rgba(5, 150, 105, 0.15)",
                    border: "2px solid #059669",
                    borderRadius: 30,
                    padding: "12px 36px",
                    fontFamily: "'Courier New', monospace",
                    fontSize: 26,
                    color: "#059669",
                    fontWeight: 800,
                  }}
                >
                  AUTONOMOUS SVG 3D GENERATOR
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
                  background: "linear-gradient(180deg, #FFFFFF 0%, #F1F5F9 100%)",
                  border: "2.5px solid #059669",
                  boxShadow: "0 35px 90px rgba(15, 23, 42, 0.20), 0 0 60px rgba(5, 150, 105, 0.20)",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  padding: "50px 40px",
                  position: "relative",
                  overflow: "hidden",
                }}
              >
                {/* Active Rotating Ring */}
                <div
                  style={{
                    position: "absolute",
                    width: 750,
                    height: 750,
                    borderRadius: "50%",
                    border: "2.5px solid rgba(5, 150, 105, 0.45)",
                    transform: `scale(${1.0 + ((frame * 3) % 60) / 30})`,
                    opacity: 1.0 - ((frame * 3) % 60) / 60,
                    pointerEvents: "none",
                  }}
                />

                {/* Brand Logo with 3D Motion */}
                <div
                  style={{
                    width: 170,
                    height: 170,
                    borderRadius: 36,
                    overflow: "hidden",
                    border: "3.5px solid #059669",
                    boxShadow: "0 0 50px rgba(5, 150, 105, 0.4)",
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
                    color: "#0F172A",
                    lineHeight: 1.0,
                    marginBottom: 16,
                  }}
                >
                  FLASH<span style={{ color: "#059669" }}>.Ai</span>
                </div>

                <div
                  style={{
                    fontSize: 42,
                    fontWeight: 700,
                    color: "#334155",
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
                    borderRadius: 22,
                    backgroundColor: "rgba(5, 150, 105, 0.08)",
                    border: "1.5px solid rgba(5, 150, 105, 0.35)",
                    width: "90%",
                    textAlign: "center",
                  }}
                >
                  <div
                    style={{
                      fontFamily: "'Courier New', monospace",
                      fontSize: 34,
                      fontWeight: 800,
                      color: "#059669",
                    }}
                  >
                    Ryan (@wheresryan22) • MIT License
                  </div>
                  <div
                    style={{
                      fontFamily: "'Courier New', monospace",
                      fontSize: 28,
                      color: "#0F172A",
                      fontWeight: 700,
                    }}
                  >
                    github.com/wheresryan22/anatomy
                  </div>
                </div>

                {/* Footer Telemetry */}
                <div
                  style={{
                    marginTop: 32,
                    display: "flex",
                    gap: 30,
                    fontFamily: "'Courier New', monospace",
                    fontSize: 22,
                    color: "#475569",
                    fontWeight: 700,
                  }}
                >
                  <span>STARS: <b>25,676</b></span>
                  <span>LICENSE: <b>MIT</b></span>
                  <span>MUSEUM: <b>EXHIBIT 01</b></span>
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
              border: "2px solid #059669",
              boxShadow: "0 0 25px rgba(5, 150, 105, 0.4)",
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
              color: "#0F172A",
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
              color: "#059669",
              letterSpacing: 1.5,
              backgroundColor: "rgba(255, 255, 255, 0.98)",
              padding: "10px 20px",
              borderRadius: 12,
              border: "1.5px solid rgba(5, 150, 105, 0.35)",
              boxShadow: "0 6px 16px rgba(15, 23, 42, 0.10)",
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
                fontSize: 92,
                fontWeight: 900,
                color: "#0F172A",
                letterSpacing: -1.5,
                lineHeight: 1.05,
              }}
            >
              TECHNICAL <span style={{ color: "#059669" }}>BLUEPRINT</span>
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
                color: "#0F172A",
                letterSpacing: -1.5,
                lineHeight: 1.05,
              }}
            >
              EXPLODED <span style={{ color: "#059669" }}>ASSEMBLY</span>
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
                color: "#0F172A",
                letterSpacing: -1.5,
                lineHeight: 1.05,
              }}
            >
              AUTONOMOUS <span style={{ color: "#059669" }}>3D ENGINE</span>
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
                    fontSize: 60,
                    fontWeight: 800,
                    color: isActive ? "#FFFFFF" : "#0F172A",
                    backgroundColor: isActive ? "#059669" : "rgba(255, 255, 255, 0.95)",
                    transform: isActive ? "scale(1.12)" : "scale(1.0)",
                    transition: "transform 0.08s ease-out",
                    padding: "10px 22px",
                    borderRadius: 14,
                    border: isActive
                      ? "2.5px solid #047857"
                      : "1px solid rgba(15, 23, 42, 0.15)",
                    boxShadow: isActive
                      ? "0 8px 25px rgba(5, 150, 105, 0.45)"
                      : "0 4px 15px rgba(15, 23, 42, 0.10)",
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
