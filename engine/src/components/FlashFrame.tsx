import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

interface FlashFrameProps {
  triggerFrames: number[];
  flashDurationFrames?: number;
}

export const FlashFrame: React.FC<FlashFrameProps> = ({
  triggerFrames,
  flashDurationFrames = 2,
}) => {
  const frame = useCurrentFrame();

  let maxOpacity = 0;
  for (const trigger of triggerFrames) {
    if (frame >= trigger && frame < trigger + flashDurationFrames) {
      const rel = frame - trigger;
      const op = interpolate(rel, [0, flashDurationFrames], [0.85, 0], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      });
      if (op > maxOpacity) maxOpacity = op;
    }
  }

  if (maxOpacity <= 0.01) return null;

  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        backgroundColor: "#ffffff",
        opacity: maxOpacity,
        pointerEvents: "none",
        zIndex: 998,
        mixBlendMode: "screen",
      }}
    />
  );
};
