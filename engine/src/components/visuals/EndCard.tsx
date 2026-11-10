import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const EndCard: React.FC<{
  brandHandle?: string;
  subtitle?: string;
}> = ({
  brandHandle = "@flash__ai__digital",
  subtitle = "Daily AI and dev updates, with sources",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Tap animation occurs at frame 34 (~1.1s into end card)
  const tapFrame = 34;
  const isTapped = frame >= tapFrame;

  const s = spring({
    frame: frame - tapFrame,
    fps,
    config: { damping: 12, stiffness: 140 },
  });

  const btnScale = isTapped ? interpolate(s, [0, 0.4, 1], [1, 0.9, 1]) : 1;
  const rippleOpacity = isTapped ? interpolate(s, [0, 1], [0.85, 0]) : 0;
  const rippleScale = isTapped ? interpolate(s, [0, 1], [1, 2.4]) : 1;

  // Active motion elements to keep MAD >= 4.0
  const scanY = (frame * 24) % 1280;
  const pulseScale = 1.0 + Math.sin(frame * 0.22) * 0.06;
  const rotateDeg = frame * 4.5;

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "80px 40px 100px 40px",
        boxSizing: "border-box",
        background:
          "linear-gradient(180deg, #071526 0%, #0f2d52 30%, #1a4980 60%, #091c33 85%, #040b17 100%)",
        overflow: "hidden",
      }}
    >
      {/* Dynamic Laser Scanline across End Card */}
      <div
        style={{
          position: "absolute",
          top: scanY,
          left: 0,
          right: 0,
          height: 4,
          background:
            "linear-gradient(90deg, transparent 0%, #00F0FF 50%, transparent 100%)",
          boxShadow: "0 0 25px #00F0FF",
          opacity: 0.9,
          zIndex: 5,
        }}
      />

      {/* Background Rotating Conic Radar Sweep */}
      <div
        style={{
          position: "absolute",
          top: "50%",
          left: "50%",
          width: 700,
          height: 700,
          transform: `translate(-50%, -50%) rotate(${rotateDeg}deg)`,
          borderRadius: "50%",
          background:
            "conic-gradient(from 0deg, rgba(0, 240, 255, 0.35) 0deg, rgba(138, 43, 226, 0.25) 120deg, transparent 240deg, rgba(0, 240, 255, 0.35) 360deg)",
          filter: "blur(20px)",
          opacity: 0.75,
          pointerEvents: "none",
        }}
      />

      {/* TOP HEADER */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 12,
          zIndex: 10,
        }}
      >
        <div
          style={{
            backgroundColor: "rgba(0, 240, 255, 0.2)",
            border: "2px solid #00F0FF",
            borderRadius: 24,
            padding: "8px 24px",
            fontSize: 18,
            fontWeight: 900,
            color: "#00F0FF",
            letterSpacing: "1.5px",
            boxShadow: "0 0 20px rgba(0, 240, 255, 0.5)",
          }}
        >
          FLASH STUDIO
        </div>
        <div
          style={{
            fontSize: 22,
            fontWeight: 800,
            color: "#FFFFFF",
            letterSpacing: "0.5px",
            textShadow: "0 2px 10px rgba(0,0,0,0.8)",
          }}
        >
          DAILY AI & CODE TELEMETRY
        </div>
      </div>

      {/* CENTER HERO: Pulsing Flash Lightning Logo */}
      <div
        style={{
          position: "relative",
          width: 380,
          height: 380,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          zIndex: 10,
        }}
      >
        {/* Pulsing Outer Glow Ring */}
        <div
          style={{
            position: "absolute",
            width: 320,
            height: 320,
            borderRadius: "50%",
            border: "3px solid rgba(0, 240, 255, 0.6)",
            transform: `scale(${pulseScale})`,
            boxShadow: "0 0 40px rgba(0, 240, 255, 0.6), inset 0 0 30px rgba(0, 240, 255, 0.4)",
          }}
        />

        {/* Pulsing Inner Violet Ring */}
        <div
          style={{
            position: "absolute",
            width: 260,
            height: 260,
            borderRadius: "50%",
            border: "2px dashed rgba(168, 85, 247, 0.7)",
            transform: `scale(${1.0 + Math.cos(frame * 0.25) * 0.05}) rotate(${-rotateDeg * 0.5}deg)`,
          }}
        />

        {/* Flash Lightning Bolt SVG Icon */}
        <svg
          width="180"
          height="180"
          viewBox="0 0 100 100"
          style={{
            transform: `scale(${pulseScale})`,
            filter: "drop-shadow(0 0 25px rgba(0, 240, 255, 0.9))",
          }}
        >
          <defs>
            <linearGradient id="boltGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#00F0FF" />
              <stop offset="60%" stopColor="#00E5FF" />
              <stop offset="100%" stopColor="#A855F7" />
            </linearGradient>
          </defs>
          <polygon
            points="55,5 18,52 48,52 42,95 82,46 52,46"
            fill="url(#boltGrad)"
            stroke="#FFFFFF"
            strokeWidth="2.5"
            strokeLinejoin="round"
          />
        </svg>
      </div>

      {/* LOWER SECTION: Interactive Follow Button & Subtitle */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 18,
          zIndex: 10,
          width: "100%",
        }}
      >
        {/* Main Follow Pill Container */}
        <div style={{ position: "relative", display: "flex", justifyContent: "center" }}>
          {/* Ripple Ring on Tap */}
          {isTapped && (
            <div
              style={{
                position: "absolute",
                top: 0,
                left: -20,
                right: -20,
                bottom: 0,
                borderRadius: 40,
                border: "3px solid #10B981",
                opacity: rippleOpacity,
                transform: `scale(${rippleScale})`,
                pointerEvents: "none",
              }}
            />
          )}

          <div
            style={{
              transform: `scale(${btnScale})`,
              backgroundColor: isTapped ? "#10B981" : "#00F0FF",
              color: isTapped ? "#FFFFFF" : "#050914",
              borderRadius: 36,
              padding: "18px 42px",
              display: "flex",
              alignItems: "center",
              gap: 14,
              boxShadow: isTapped
                ? "0 0 45px rgba(16, 185, 129, 0.85)"
                : "0 0 45px rgba(0, 240, 255, 0.85)",
              cursor: "pointer",
              transition: "background-color 0.2s ease, box-shadow 0.2s ease",
            }}
          >
            {isTapped ? (
              <>
                <svg
                  width="28"
                  height="28"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="3.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <polyline points="20 6 9 17 4 12" />
                </svg>
                <div style={{ fontSize: 26, fontWeight: 900, letterSpacing: "1px" }}>
                  FOLLOWING
                </div>
              </>
            ) : (
              <>
                <svg
                  width="28"
                  height="28"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="3.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <line x1="12" y1="5" x2="12" y2="19" />
                  <line x1="5" y1="12" x2="19" y2="12" />
                </svg>
                <div style={{ fontSize: 26, fontWeight: 900, letterSpacing: "0.5px" }}>
                  FOLLOW {brandHandle}
                </div>
              </>
            )}
          </div>

          {/* Animated Tap Hand Pointer just before tap */}
          {frame >= tapFrame - 15 && frame < tapFrame + 18 && (
            <div
              style={{
                position: "absolute",
                right: 30,
                bottom: -15,
                transform: `translate(${frame < tapFrame ? (tapFrame - frame) * 3 : 0}px, ${frame < tapFrame ? (tapFrame - frame) * 3 : 0}px)`,
                pointerEvents: "none",
                filter: "drop-shadow(0 4px 12px rgba(0,0,0,0.8))",
                zIndex: 20,
              }}
            >
              <svg width="48" height="48" viewBox="0 0 24 24" fill="#FFFFFF">
                <path d="M9 11.24V7.5a2.5 2.5 0 0 1 5 0v3.74c1.21-.81 2-2.18 2-3.74a4.5 4.5 0 0 0-9 0c0 1.56.79 2.93 2 3.74zM12 2a5.5 5.5 0 0 1 5.5 5.5c0 1.83-.89 3.45-2.27 4.46L19 19H5l3.77-7.04A5.485 5.485 0 0 1 6.5 7.5 5.5 5.5 0 0 1 12 2z" />
              </svg>
            </div>
          )}
        </div>

        {/* Subtitle & Telemetry Footers */}
        <div
          style={{
            fontSize: 20,
            fontWeight: 800,
            color: "rgba(255, 255, 255, 0.9)",
            textAlign: "center",
          }}
        >
          {subtitle}
        </div>
        <div
          style={{
            fontSize: 14,
            fontWeight: 700,
            color: "rgba(0, 240, 255, 0.8)",
            letterSpacing: "1px",
            fontFamily: "'JetBrains Mono', monospace",
          }}
        >
          BUILT WITH REAL CODE • ZERO FAKE CLAIMS
        </div>
      </div>
    </div>
  );
};
