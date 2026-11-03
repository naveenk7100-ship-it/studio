import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

interface StarCounterProps {
  targetStars: number;
  durationFrames?: number;
}

export const StarCounter: React.FC<StarCounterProps> = ({
  targetStars,
  durationFrames = 30,
}) => {
  const frame = useCurrentFrame();

  const count = Math.round(
    interpolate(frame, [0, durationFrames], [0, targetStars], {
      extrapolateRight: "clamp",
    })
  );

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: 12,
        padding: "12px 28px",
        borderRadius: 24,
        background: "rgba(255, 215, 0, 0.12)",
        border: "1.5px solid rgba(255, 215, 0, 0.5)",
      }}
    >
      <span style={{ fontSize: 38, color: "#ffd700" }}>★</span>
      <span
        style={{
          fontFamily: "'Courier New', monospace",
          fontWeight: 800,
          fontSize: 44,
          color: "#ffd700",
        }}
      >
        {count.toLocaleString()}
      </span>
      <span
        style={{
          fontFamily: "'Inter', sans-serif",
          fontWeight: 600,
          fontSize: 26,
          color: "#8892b0",
          marginLeft: 8,
        }}
      >
        stars
      </span>
    </div>
  );
};
