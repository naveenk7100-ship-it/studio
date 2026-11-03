import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

interface BoltStrikeProps {
  startFrame: number;
  durationInFrames?: number;
}

export const BoltStrike: React.FC<BoltStrikeProps> = ({
  startFrame,
  durationInFrames = 6,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const relFrame = frame - startFrame;
  if (relFrame < 0 || relFrame > durationInFrames) {
    return null;
  }

  const progress = interpolate(relFrame, [0, durationInFrames], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Dynamic lightning path slicing from top-left to bottom-right
  const xOffset = interpolate(progress, [0, 1], [-200, 1280]);
  const opacity = interpolate(progress, [0, 0.3, 0.7, 1], [0, 1, 1, 0]);

  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        pointerEvents: "none",
        zIndex: 999,
        opacity,
      }}
    >
      <svg
        width="1080"
        height="1920"
        viewBox="0 0 1080 1920"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        style={{
          filter: "drop-shadow(0 0 25px #00f0ff) drop-shadow(0 0 45px #ff007f)",
        }}
      >
        <path
          d={`M ${xOffset} 0 L ${xOffset + 220} 600 L ${xOffset + 80} 640 L ${xOffset + 380} 1280 L ${xOffset + 240} 1320 L ${xOffset + 500} 1920`}
          stroke="#ffffff"
          strokeWidth="14"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d={`M ${xOffset} 0 L ${xOffset + 220} 600 L ${xOffset + 80} 640 L ${xOffset + 380} 1280 L ${xOffset + 240} 1320 L ${xOffset + 500} 1920`}
          stroke="#00f0ff"
          strokeWidth="32"
          strokeOpacity="0.8"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    </div>
  );
};
