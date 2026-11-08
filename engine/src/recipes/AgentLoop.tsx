import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

export const AgentLoop: React.FC<{
  title?: string;
  subtitle?: string;
}> = ({
  title = "STEP 3: LLM STRUCTURED PROMPT",
  subtitle = "Feed clean markdown chunks into your model with strict extraction constraints",
}) => {
  const frame = useCurrentFrame();

  const rot = (frame * 3) % 360;

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
      {/* Background Mesh */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: "radial-gradient(circle at 50% 50%, rgba(255, 158, 0, 0.12) 0%, rgba(10, 14, 24, 0.98) 75%)",
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
            color: "#FF9E00",
            textTransform: "uppercase",
            marginBottom: 8,
            textShadow: "0 0 20px rgba(255, 158, 0, 0.6)",
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

      {/* 3D Cyclical Nodes Container */}
      <div
        style={{
          width: 600,
          backgroundColor: "rgba(16, 22, 34, 0.9)",
          border: "2px solid #FF9E00",
          borderRadius: 20,
          padding: 24,
          boxShadow: "0 0 35px rgba(255, 158, 0, 0.35)",
          backdropFilter: "blur(14px)",
          marginTop: 110,
          zIndex: 5,
        }}
      >
        <div style={{ fontSize: 16, fontWeight: 800, color: "#FF9E00", marginBottom: 12 }}>
          LLM SYNTHESIS INSTRUCTIONS:
        </div>
        <div
          style={{
            fontSize: 16,
            lineHeight: 1.6,
            color: "#E2E8F0",
            fontFamily: "monospace",
          }}
        >
          {`1. Extract primary research hypothesis
2. State baseline vs new method metrics
3. Flag mathematical assumptions & limitations
4. Format output in structured JSON schema`}
        </div>
      </div>

      {/* Bottom Rail */}
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
          OUTPUT: 100% FACTUAL GROUNDING
        </div>
        <div style={{ fontSize: 16, fontWeight: 800, color: "#FF9E00" }}>
          ZERO HALLUCINATIONS
        </div>
      </div>
    </div>
  );
};
