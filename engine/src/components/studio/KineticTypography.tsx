import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export interface KineticTypographyProps {
  kicker?: string;
  prefix?: string;
  focalText?: string;
  suffix?: string;
  kickerColor?: string;
  focalColor?: string;
  align?: "center" | "left";
  maxWidth?: number;
}

export const KineticTypography: React.FC<KineticTypographyProps> = ({
  kicker,
  prefix,
  focalText = "Headline Text",
  suffix,
  kickerColor = "#0284C7",
  focalColor = "#0F172A",
  align = "center",
  maxWidth = 640,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 120 },
  });

  const underlineWidth = interpolate(entrance, [0, 1], [0, 100]);
  const opacity = interpolate(entrance, [0, 1], [0, 1]);
  const translateY = interpolate(entrance, [0, 1], [15, 0]);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: align === "center" ? "center" : "flex-start",
        textAlign: align,
        maxWidth,
        opacity,
        transform: `translateY(${translateY}px)`,
        marginBottom: 18,
        boxSizing: "border-box",
      }}
    >
      {/* Category Kicker Pill */}
      {kicker && (
        <div
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 6,
            backgroundColor: "rgba(255, 255, 255, 0.95)",
            border: `1.5px solid ${kickerColor}`,
            borderRadius: 20,
            padding: "5px 16px",
            fontSize: 13,
            fontWeight: 800,
            color: kickerColor,
            letterSpacing: "0.8px",
            fontFamily: "'JetBrains Mono', monospace",
            marginBottom: 10,
            boxShadow: "0 2px 8px rgba(0, 0, 0, 0.04)",
          }}
        >
          <span style={{ fontSize: 9 }}>●</span>
          <span>{kicker}</span>
        </div>
      )}

      {/* Main Dual-Tier Editorial Headline */}
      <div
        style={{
          fontFamily: "'Plus Jakarta Sans', 'Inter', sans-serif",
          lineHeight: 1.15,
          color: "#0F172A",
          display: "flex",
          flexDirection: "column",
          alignItems: align === "center" ? "center" : "flex-start",
        }}
      >
        {prefix && (
          <span
            style={{
              fontSize: 22,
              fontWeight: 600,
              color: "#64748B",
              marginBottom: 4,
            }}
          >
            {prefix}
          </span>
        )}

        <div style={{ position: "relative", display: "inline-block" }}>
          <span
            style={{
              fontSize: 46,
              fontWeight: 900,
              color: focalColor,
              letterSpacing: "-0.8px",
            }}
          >
            {focalText}
          </span>

          {/* Kinetic Underline Sweep */}
          <div
            style={{
              position: "absolute",
              bottom: -4,
              left: 0,
              width: `${underlineWidth}%`,
              height: 4,
              borderRadius: 2,
              backgroundColor: kickerColor,
              opacity: 0.85,
            }}
          />
        </div>

        {suffix && (
          <span
            style={{
              fontSize: 18,
              fontWeight: 600,
              color: "#64748B",
              marginTop: 6,
            }}
          >
            {suffix}
          </span>
        )}
      </div>
    </div>
  );
};
