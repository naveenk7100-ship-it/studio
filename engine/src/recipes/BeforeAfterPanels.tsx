import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const BeforeAfterPanels: React.FC<{
  title?: string;
  subtitle?: string;
}> = ({
  title = "THE PROBLEM: RAW PDF PARSING",
  subtitle = "Scrambled multi-column text ruins LLM paper summarization",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Sliding divider position
  const dividerPos = interpolate(Math.sin(frame / 20), [-1, 1], [40, 60]);

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
        perspective: 1000,
        overflow: "hidden",
      }}
    >
      {/* Background Mesh */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: "radial-gradient(circle at 50% 50%, rgba(239, 68, 68, 0.12) 0%, rgba(10, 14, 24, 0.98) 75%)",
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
            color: "#EF4444",
            textTransform: "uppercase",
            marginBottom: 8,
            textShadow: "0 0 20px rgba(239, 68, 68, 0.6)",
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

      {/* 3D Comparative Panels Container */}
      <div
        style={{
          width: 640,
          height: 380,
          marginTop: 110,
          display: "flex",
          gap: 16,
          zIndex: 5,
        }}
      >
        {/* Left Panel: Raw Messy PDF */}
        <div
          style={{
            flex: 1,
            backgroundColor: "rgba(30, 15, 20, 0.8)",
            border: "2px solid #EF4444",
            borderRadius: 18,
            padding: 20,
            boxShadow: "0 0 30px rgba(239, 68, 68, 0.3)",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <div
            style={{
              fontSize: 14,
              fontWeight: 800,
              color: "#EF4444",
              marginBottom: 10,
              textTransform: "uppercase",
              letterSpacing: "1px",
            }}
          >
            RAW COPY-PASTE (BROKEN)
          </div>
          <div
            style={{
              fontSize: 14,
              lineHeight: 1.5,
              color: "rgba(255,255,255,0.6)",
              fontFamily: "monospace",
              whiteSpace: "pre-wrap",
            }}
          >
            {`Section 1: In troduc tion [1]
Column 2 wraps here...
Table 1: Acc uracy 94%
References inter leaved:
[1] Vaswani et al. 2017
Equations broken into symbols:
∑ i = 1 ... softmax scrambled`}
          </div>
        </div>

        {/* Right Panel: Clean Structured Flow */}
        <div
          style={{
            flex: 1,
            backgroundColor: "rgba(10, 30, 35, 0.8)",
            border: "2px solid #00F0FF",
            borderRadius: 18,
            padding: 20,
            boxShadow: "0 0 30px rgba(0, 240, 255, 0.3)",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <div
            style={{
              fontSize: 14,
              fontWeight: 800,
              color: "#00F0FF",
              marginBottom: 10,
              textTransform: "uppercase",
              letterSpacing: "1px",
            }}
          >
            PYPDFIUM2 STREAM (CLEAN)
          </div>
          <div
            style={{
              fontSize: 14,
              lineHeight: 1.5,
              color: "#FFFFFF",
              fontFamily: "monospace",
              whiteSpace: "pre-wrap",
            }}
          >
            {`# 1. Introduction
Language models rely on
self-attention mechanisms.

## Key Findings
- 6.5x faster throughput
- Zero layout corruption
- Clean UTF-8 markdown

Ready for LLM Context ->`}
          </div>
        </div>
      </div>

      {/* Bottom Comparison Rail */}
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
          DIAGNOSIS: PRESERVE LOGICAL READING ORDER
        </div>
        <div style={{ fontSize: 16, fontWeight: 800, color: "#00F0FF" }}>
          NO HALLUCINATIONS
        </div>
      </div>
    </div>
  );
};
