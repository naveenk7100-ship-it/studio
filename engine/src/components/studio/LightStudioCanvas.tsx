import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

export interface LightStudioCanvasProps {
  primaryAccent?: string;
  secondaryAccent?: string;
  gridId?: string;
  children: React.ReactNode;
}

export const LightStudioCanvas: React.FC<LightStudioCanvasProps> = ({
  primaryAccent = "#00F0FF",
  secondaryAccent = "rgba(0, 240, 255, 0.25)",
  gridId = "studioDarkCanvas",
  children,
}) => {
  const frame = useCurrentFrame();

  // Moving ambient studio lighting & scanline
  const scanY = (frame * 12) % 1280;
  const radarRot = frame * 2.2;
  const spotX = interpolate(frame % 180, [0, 90, 180], [35, 65, 35]);
  const spotY = interpolate(frame % 180, [0, 90, 180], [25, 45, 25]);

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        backgroundColor: "#020617",
        background: `
          radial-gradient(circle at ${spotX}% ${spotY}%, rgba(0, 240, 255, 0.22) 0%, transparent 60%),
          linear-gradient(180deg, #020617 0%, #0B192C 22%, #1E3A5F 50%, #0B192C 78%, #020617 100%)
        `,
        overflow: "hidden",
        fontFamily: "'Inter', -apple-system, sans-serif",
      }}
    >
      {/* LAYER 1: Technical Blueprint Drafting Grid Matrix */}
      <svg
        style={{
          position: "absolute",
          inset: 0,
          width: "100%",
          height: "100%",
          pointerEvents: "none",
          opacity: 0.40,
        }}
      >
        <defs>
          <pattern
            id={gridId}
            width="36"
            height="36"
            patternUnits="userSpaceOnUse"
          >
            <path
              d="M 36 0 L 0 0 0 36"
              fill="none"
              stroke="#00F0FF"
              strokeWidth="1.2"
              strokeOpacity="0.25"
            />
            <circle cx="18" cy="18" r="1.2" fill="#00F0FF" opacity="0.30" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill={`url(#${gridId})`} />
      </svg>

      {/* LAYER 2: Ambient Rotating Luminous Conic Sweep */}
      <div
        style={{
          position: "absolute",
          top: "40%",
          left: "50%",
          width: 800,
          height: 800,
          transform: `translate(-50%, -50%) rotate(${radarRot}deg)`,
          borderRadius: "50%",
          background: `
            conic-gradient(from 0deg, rgba(0, 240, 255, 0.10) 0deg, rgba(56, 189, 248, 0.06) 120deg, transparent 240deg, rgba(0, 240, 255, 0.10) 360deg)
          `,
          filter: "blur(32px)",
          pointerEvents: "none",
        }}
      />

      {/* LAYER 3: Active Studio Laser Scanline (Controlled luminance < 90 so captions never false-flag) */}
      <div
        style={{
          position: "absolute",
          top: scanY,
          left: 0,
          right: 0,
          height: 3,
          background: "linear-gradient(90deg, transparent 0%, rgba(0, 240, 255, 0.45) 50%, transparent 100%)",
          boxShadow: "0 0 12px rgba(0, 240, 255, 0.35)",
          pointerEvents: "none",
          zIndex: 5,
        }}
      />

      {/* LAYER 4: Studio Header Telemetry */}
      <div
        style={{
          position: "absolute",
          top: 32,
          left: 45,
          right: 45,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 11,
          fontWeight: 700,
          color: "rgba(255, 255, 255, 0.6)",
          letterSpacing: "1px",
          pointerEvents: "none",
          zIndex: 6,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
          <div
            style={{
              width: 7,
              height: 7,
              borderRadius: "50%",
              backgroundColor: primaryAccent,
              boxShadow: `0 0 8px ${primaryAccent}`,
            }}
          />
          <span style={{ color: primaryAccent }}>FLASH STUDIO // ENGINE 3.0</span>
        </div>
        <div>REAL TELEMETRY • ZERO MOCK</div>
      </div>

      {/* LAYER 5: Content Children */}
      <div style={{ position: "absolute", inset: 0, zIndex: 10 }}>
        {children}
      </div>
    </div>
  );
};
