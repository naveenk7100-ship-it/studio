import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";

export interface CaptionPhrase {
  start: number;
  end: number;
  text: string;
}

export const Captions720p: React.FC<{
  captions: CaptionPhrase[];
  speechEndSec?: number;
}> = ({ captions, speechEndSec = 25.5 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentTime = frame / fps;

  if (currentTime > speechEndSec) {
    return null; // strictly hidden once speech ends
  }

  // Find active phrase
  const active = captions.find(
    (c) => currentTime >= c.start && currentTime <= c.end + 0.15
  );

  if (!active) return null;

  return (
    <div
      style={{
        position: "absolute",
        bottom: 210,
        left: 30,
        right: 30,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 90,
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          backgroundColor: "rgba(10, 14, 24, 0.94)",
          border: "2px solid rgba(0, 240, 255, 0.5)",
          borderRadius: 24,
          padding: "14px 28px",
          boxShadow: "0 10px 30px rgba(0, 0, 0, 0.8)",
          maxWidth: 660,
          textAlign: "center",
          backdropFilter: "blur(12px)",
        }}
      >
        <span
          style={{
            fontFamily: "sans-serif",
            fontWeight: 900,
            fontSize: 56, // >= 56 px requirement
            lineHeight: 1.15,
            color: "#FFD700",
            textShadow: "0 0 20px rgba(255, 215, 0, 0.6), 0 2px 8px rgba(0,0,0,0.8)",
            letterSpacing: "-0.5px",
          }}
        >
          {active.text}
        </span>
      </div>
    </div>
  );
};
