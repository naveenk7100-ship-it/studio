import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

export const FollowPill: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const enterScale = spring({
    frame,
    fps,
    config: { damping: 12, mass: 0.8, stiffness: 120 },
  });

  // Continuous micro-breathing drift so it never stays static > 1.5s
  const pulse = 1.0 + 0.03 * Math.sin(frame * 0.15);
  const totalScale = enterScale * pulse;

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        transform: `scale(${totalScale})`,
        zIndex: 50,
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 16,
          padding: "24px 56px",
          borderRadius: 60,
          background: "linear-gradient(135deg, #00f0ff 0%, #ff007f 100%)",
          boxShadow: `0 0 ${40 + 10 * Math.sin(frame * 0.2)}px rgba(0, 240, 255, 0.6)`,
        }}
      >
        <span
          style={{
            fontFamily: "'Inter', sans-serif",
            fontWeight: 800,
            fontSize: 54,
            color: "#ffffff",
            letterSpacing: 1.0,
          }}
        >
          FOLLOW @flash__ai__digital
        </span>
      </div>
      <span
        style={{
          marginTop: 20,
          fontFamily: "'Inter', sans-serif",
          fontWeight: 600,
          fontSize: 36,
          color: "#8892b0",
        }}
      >
        Daily AI &amp; Code Reels • Zero Hype
      </span>
    </div>
  );
};
