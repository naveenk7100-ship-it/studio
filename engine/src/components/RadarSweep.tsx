import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

export const RadarSweep: React.FC = () => {
  const frame = useCurrentFrame();
  const rotation = interpolate(frame % 90, [0, 90], [0, 360]);

  return (
    <div
      style={{
        position: "absolute",
        top: 360,
        left: 40,
        width: 1000,
        height: 1000,
        borderRadius: "50%",
        border: "1px solid rgba(0, 240, 255, 0.2)",
        overflow: "hidden",
        pointerEvents: "none",
        zIndex: 10,
      }}
    >
      {/* Concentric rings */}
      <div
        style={{
          position: "absolute",
          top: "15%",
          left: "15%",
          width: "70%",
          height: "70%",
          borderRadius: "50%",
          border: "1px dashed rgba(0, 240, 255, 0.15)",
        }}
      />
      <div
        style={{
          position: "absolute",
          top: "35%",
          left: "35%",
          width: "30%",
          height: "30%",
          borderRadius: "50%",
          border: "1px solid rgba(255, 0, 127, 0.2)",
        }}
      />
      {/* Rotating sweep cone */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          transform: `rotate(${rotation}deg)`,
          background:
            "conic-gradient(from 0deg, rgba(0, 240, 255, 0.35) 0deg, rgba(0, 240, 255, 0) 55deg, transparent 360deg)",
        }}
      />
    </div>
  );
};
