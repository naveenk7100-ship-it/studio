import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

export const EmbeddingSpace: React.FC<{
  title?: string;
  subtitle?: string;
  highlightWord?: string;
}> = ({
  title = "STEP 2: VECTOR EMBEDDINGS",
  subtitle = "Tokens mapped to high-dimensional semantic coordinates",
  highlightWord = "think",
}) => {
  const frame = useCurrentFrame();

  // Dynamic 3D rotation
  const rotY = (frame * 0.9) % 360;
  const rotX = 22 + Math.sin(frame / 30) * 8;

  // Words with 3D positions in simulated vector space
  const clusters = [
    // Cluster A: Query/Thought
    { word: "think", x: 40, y: -50, z: 60, cluster: "Cognition", color: "#00F0FF" },
    { word: "reason", x: 65, y: -30, z: 75, cluster: "Cognition", color: "#00F0FF" },
    { word: "logic", x: 20, y: -70, z: 45, cluster: "Cognition", color: "#00F0FF" },
    { word: "ponder", x: 80, y: -60, z: 90, cluster: "Cognition", color: "#00F0FF" },
    // Cluster B: Action/Language
    { word: "write", x: -90, y: 40, z: -40, cluster: "Language", color: "#FF9E00" },
    { word: "speak", x: -110, y: 60, z: -20, cluster: "Language", color: "#FF9E00" },
    { word: "answer", x: -70, y: 30, z: -60, cluster: "Language", color: "#FF9E00" },
    // Cluster C: Computation
    { word: "compute", x: -30, y: -110, z: -70, cluster: "Compute", color: "#A78BFA" },
    { word: "calculate", x: -10, y: -130, z: -50, cluster: "Compute", color: "#A78BFA" },
    { word: "matrix", x: -45, y: -90, z: -90, cluster: "Compute", color: "#A78BFA" },
  ];

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        position: "relative",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        perspective: 1100,
        overflow: "hidden",
      }}
    >
      {/* Background Radial Gradient Mesh */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: "radial-gradient(circle at 50% 50%, rgba(0, 240, 255, 0.12) 0%, rgba(10, 14, 24, 0.98) 75%)",
          zIndex: 0,
        }}
      />

      {/* Header Container */}
      <div
        style={{
          position: "absolute",
          top: 130,
          left: 40,
          right: 40,
          zIndex: 10,
          textAlign: "center",
        }}
      >
        <div
          style={{
            fontSize: 24,
            fontWeight: 800,
            letterSpacing: "4px",
            color: "#00F0FF",
            textTransform: "uppercase",
            marginBottom: 8,
            textShadow: "0 0 20px rgba(0, 240, 255, 0.6)",
          }}
        >
          {title}
        </div>
        <div
          style={{
            fontSize: 42,
            fontWeight: 900,
            lineHeight: 1.15,
            color: "#FFFFFF",
            maxWidth: 640,
            margin: "0 auto",
            textShadow: "0 4px 24px rgba(0,0,0,0.8)",
          }}
        >
          {subtitle}
        </div>
      </div>

      {/* 3D Point Cloud Canvas */}
      <div
        style={{
          width: 500,
          height: 500,
          position: "relative",
          marginTop: 80,
          transform: `rotateX(${rotX}deg) rotateY(${rotY}deg)`,
          transformStyle: "preserve-3d",
          zIndex: 5,
        }}
      >
        {/* 3D Coordinate Axis Guides */}
        <div
          style={{
            position: "absolute",
            left: 250,
            top: 50,
            bottom: 50,
            width: 2,
            backgroundColor: "rgba(0, 240, 255, 0.3)",
            transform: "translateZ(0px)",
          }}
        />
        <div
          style={{
            position: "absolute",
            top: 250,
            left: 50,
            right: 50,
            height: 2,
            backgroundColor: "rgba(255, 158, 0, 0.3)",
            transform: "translateZ(0px)",
          }}
        />

        {/* Vector Points */}
        {clusters.map((pt, i) => {
          const isTarget = pt.word === highlightWord;
          const pulse = isTarget ? 1 + Math.sin(frame / 6) * 0.15 : 1;

          return (
            <div
              key={i}
              style={{
                position: "absolute",
                left: 250 + pt.x,
                top: 250 + pt.y,
                transform: `translate3d(-50%, -50%, ${pt.z}px) rotateY(${-rotY}deg) rotateX(${-rotX}deg) scale(${pulse})`,
                transformStyle: "preserve-3d",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                pointerEvents: "none",
              }}
            >
              {/* Dot */}
              <div
                style={{
                  width: isTarget ? 18 : 10,
                  height: isTarget ? 18 : 10,
                  borderRadius: "50%",
                  backgroundColor: pt.color,
                  boxShadow: `0 0 ${isTarget ? 24 : 10}px ${pt.color}`,
                  marginBottom: 6,
                }}
              />
              {/* Word Badge */}
              <div
                style={{
                  backgroundColor: isTarget ? "rgba(0, 240, 255, 0.9)" : "rgba(10, 16, 26, 0.85)",
                  color: isTarget ? "#000000" : "#FFFFFF",
                  border: `1.5px solid ${pt.color}`,
                  borderRadius: 8,
                  padding: "4px 10px",
                  fontSize: isTarget ? 20 : 15,
                  fontWeight: 800,
                  whiteSpace: "nowrap",
                  boxShadow: "0 6px 16px rgba(0,0,0,0.6)",
                }}
              >
                {pt.word}
              </div>
            </div>
          );
        })}
      </div>

      {/* Dimensional Note Card */}
      <div
        style={{
          position: "absolute",
          bottom: 140,
          left: 50,
          right: 50,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          backgroundColor: "rgba(10, 14, 22, 0.85)",
          border: "1px solid rgba(0, 240, 255, 0.3)",
          borderRadius: 14,
          padding: "14px 24px",
          backdropFilter: "blur(10px)",
          zIndex: 10,
        }}
      >
        <div style={{ fontSize: 16, fontWeight: 700, color: "#E0E6ED" }}>
          VECTOR SPACE: 1,536 DIMENSIONS (Projected to 3D)
        </div>
        <div style={{ fontSize: 16, fontWeight: 800, color: "#FF9E00", fontFamily: "monospace" }}>
          COSINE SIMILARITY CLUSTERING
        </div>
      </div>
    </div>
  );
};
