import React from "react";
import { useCurrentFrame } from "remotion";

export const TimelineRoad: React.FC<{
  title?: string;
  subtitle?: string;
}> = ({
  title = "THE REALITY: PATTERN PREDICTOR",
  subtitle = "Statistical matrix math, not conscious reasoning or live search",
}) => {
  const frame = useCurrentFrame();

  const milestones = [
    { label: "1. Tokenize", status: "BPE Encoding", color: "#00F0FF" },
    { label: "2. Vectorize", status: "Embedding Projection", color: "#00F0FF" },
    { label: "3. Transform", status: "Attention Weights", color: "#00F0FF" },
    { label: "4. Sample", status: "Softmax Next Token", color: "#FF9E00" },
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
        overflow: "hidden",
      }}
    >
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: "radial-gradient(circle at 50% 50%, rgba(255, 158, 0, 0.12) 0%, rgba(10, 14, 24, 0.98) 75%)",
          zIndex: 0,
        }}
      />

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
            color: "#FF9E00",
            textTransform: "uppercase",
            marginBottom: 8,
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
          }}
        >
          {subtitle}
        </div>
      </div>

      <div
        style={{
          width: 620,
          marginTop: 110,
          display: "flex",
          flexDirection: "column",
          gap: 16,
          zIndex: 5,
        }}
      >
        {milestones.map((m, i) => (
          <div
            key={i}
            style={{
              backgroundColor: "rgba(16, 24, 40, 0.85)",
              border: `1.5px solid ${m.color}`,
              borderRadius: 14,
              padding: "16px 20px",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <div style={{ fontSize: 20, fontWeight: 800, color: "#FFFFFF" }}>
              {m.label}
            </div>
            <div
              style={{
                fontSize: 16,
                fontWeight: 800,
                color: m.color,
                fontFamily: "monospace",
              }}
            >
              {m.status}
            </div>
          </div>
        ))}
      </div>

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
          border: "1px solid rgba(255, 158, 0, 0.4)",
          borderRadius: 14,
          padding: "14px 24px",
          backdropFilter: "blur(10px)",
          zIndex: 10,
        }}
      >
        <div style={{ fontSize: 16, fontWeight: 700, color: "#E0E6ED" }}>
          CORE ARCHITECTURE: AUTOREGRESSIVE DECODER
        </div>
        <div style={{ fontSize: 16, fontWeight: 800, color: "#FF9E00" }}>
          TOKEN BY TOKEN
        </div>
      </div>
    </div>
  );
};
