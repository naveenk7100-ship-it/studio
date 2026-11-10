import React from "react";
import { useCurrentFrame } from "remotion";

export const BackgroundRig: React.FC<{
  primaryColor?: string;
  secondaryColor?: string;
  gridId?: string;
  children?: React.ReactNode;
}> = ({
  primaryColor = "#00F0FF",
  secondaryColor = "rgba(168, 85, 247, 0.4)",
  gridId = "techGrid",
  children,
}) => {
  const frame = useCurrentFrame();

  // Dynamic light sweeps
  const lightX = 360 + Math.sin(frame * 0.05) * 220;
  const lightY = 640 + Math.cos(frame * 0.04) * 260;

  // Active laser scanline traversing top to bottom
  const scanY = (frame * 12) % 1280;

  // 24 animated background telemetry particles
  const particles = React.useMemo(() => {
    return Array.from({ length: 24 }).map((_, i) => ({
      baseX: (i * 31 + 17) % 700 + 10,
      baseY: (i * 53 + 29) % 1240 + 20,
      speed: 1.5 + (i % 5) * 0.8,
      size: 4 + (i % 3) * 2,
      opacity: 0.45 + (i % 4) * 0.15,
      phase: i * 0.4,
    }));
  }, []);

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        overflow: "hidden",
        background:
          "linear-gradient(180deg, #061120 0%, #0c2445 28%, #164070 58%, #091c33 85%, #030a14 100%)",
      }}
    >
      {/* Dynamic Multi-stop Radial Lighting Sweeps */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: `
            radial-gradient(circle 750px at ${lightX}px ${lightY}px, rgba(0, 240, 255, 0.28) 0%, transparent 68%),
            radial-gradient(circle 650px at ${720 - lightX}px ${1280 - lightY}px, ${secondaryColor} 0%, transparent 65%)
          `,
          pointerEvents: "none",
        }}
      />

      {/* High-Contrast Technical Drafting Grid */}
      <svg
        width="100%"
        height="100%"
        style={{
          position: "absolute",
          inset: 0,
          opacity: 0.75,
          pointerEvents: "none",
        }}
      >
        <defs>
          <pattern
            id={gridId}
            width="24"
            height="24"
            patternUnits="userSpaceOnUse"
          >
            <path
              d="M 24 0 L 0 0 0 24"
              fill="none"
              stroke={primaryColor}
              strokeWidth="1.5"
              opacity="0.65"
            />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill={`url(#${gridId})`} />
      </svg>

      {/* Floating Animated Telemetry Particles */}
      {particles.map((p, idx) => {
        const py = (p.baseY + frame * p.speed) % 1280;
        const px = p.baseX + Math.sin(frame * 0.05 + p.phase) * 16;
        return (
          <div
            key={idx}
            style={{
              position: "absolute",
              left: px,
              top: py,
              width: p.size,
              height: p.size,
              borderRadius: "50%",
              backgroundColor: primaryColor,
              opacity: p.opacity,
              boxShadow: `0 0 8px ${primaryColor}`,
              pointerEvents: "none",
            }}
          />
        );
      })}

      {/* Continuous Active Laser Scanline */}
      <div
        style={{
          position: "absolute",
          top: scanY,
          left: 0,
          right: 0,
          height: 4,
          background: `linear-gradient(90deg, transparent 0%, ${primaryColor} 50%, transparent 100%)`,
          boxShadow: `0 0 20px ${primaryColor}`,
          opacity: 0.85,
          zIndex: 4,
          pointerEvents: "none",
        }}
      />

      {/* Children content */}
      <div style={{ position: "absolute", inset: 0, zIndex: 10 }}>
        {children}
      </div>
    </div>
  );
};
