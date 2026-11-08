import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

export const AttentionBeams: React.FC<{
  title?: string;
  subtitle?: string;
}> = ({
  title = "STEP 3: SELF-ATTENTION BEAMS",
  subtitle = "Tokens calculate relevance weights to understand context",
}) => {
  const frame = useCurrentFrame();

  const tokens = [
    { text: "How", x: 80, y: 380 },
    { text: "does", x: 180, y: 380 },
    { text: "ChatGPT", x: 300, y: 380 },
    { text: "actually", x: 440, y: 380 },
    { text: "think", x: 580, y: 380 },
  ];

  // Attention links: [from, to, weight]
  const links = [
    { from: 4, to: 2, weight: 0.92, label: "0.92 (High)" }, // think -> ChatGPT
    { from: 4, to: 0, weight: 0.65, label: "0.65" },        // think -> How
    { from: 2, to: 3, weight: 0.45, label: "0.45" },        // ChatGPT -> actually
    { from: 2, to: 0, weight: 0.55, label: "0.55" },        // ChatGPT -> How
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
      {/* Background Mesh */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: "radial-gradient(circle at 50% 60%, rgba(255, 158, 0, 0.12) 0%, rgba(10, 14, 24, 0.98) 75%)",
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

      {/* SVG Canvas for Attention Arcs and Laser Beams */}
      <svg
        style={{
          position: "absolute",
          inset: 0,
          width: "100%",
          height: "100%",
          zIndex: 4,
          pointerEvents: "none",
        }}
      >
        <defs>
          <linearGradient id="beamGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#00F0FF" stopOpacity="0.8" />
            <stop offset="50%" stopColor="#FF9E00" stopOpacity="1" />
            <stop offset="100%" stopColor="#00F0FF" stopOpacity="0.8" />
          </linearGradient>
          <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="6" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>
        </defs>

        {links.map((link, idx) => {
          const p1 = tokens[link.from];
          const p2 = tokens[link.to];
          const midX = (p1.x + p2.x) / 2;
          const arcHeight = Math.abs(p1.x - p2.x) * 0.75 + Math.sin((frame + idx * 10) / 10) * 12;
          const midY = 380 - arcHeight;

          const pathD = `M ${p1.x} 380 Q ${midX} ${midY} ${p2.x} 380`;
          const strokeWidth = link.weight * 7;
          const dashOffset = (frame * (3 + link.weight * 4)) % 60;

          return (
            <g key={idx}>
              {/* Outer Glow Path */}
              <path
                d={pathD}
                fill="none"
                stroke="#00F0FF"
                strokeWidth={strokeWidth + 6}
                opacity={0.3}
                filter="url(#glow)"
              />
              {/* Core Laser Path */}
              <path
                d={pathD}
                fill="none"
                stroke="url(#beamGrad)"
                strokeWidth={strokeWidth}
                strokeDasharray="12 6"
                strokeDashoffset={-dashOffset}
              />
              {/* Weight Tag */}
              <rect
                x={midX - 35}
                y={midY - 22}
                width={70}
                height={26}
                rx={6}
                fill="rgba(10, 16, 26, 0.9)"
                stroke="#FF9E00"
                strokeWidth="1.5"
              />
              <text
                x={midX}
                y={midY - 5}
                textAnchor="middle"
                fill="#FF9E00"
                fontSize="14"
                fontWeight="800"
                fontFamily="monospace"
              >
                {link.label}
              </text>
            </g>
          );
        })}
      </svg>

      {/* Token Nodes */}
      <div
        style={{
          position: "absolute",
          top: 380,
          left: 0,
          right: 0,
          zIndex: 8,
          display: "flex",
          justifyContent: "center",
          gap: 20,
        }}
      >
        {tokens.map((tok, i) => {
          const isPrimary = tok.text === "think" || tok.text === "ChatGPT";
          return (
            <div
              key={i}
              style={{
                backgroundColor: isPrimary ? "rgba(0, 240, 255, 0.2)" : "rgba(16, 22, 34, 0.9)",
                border: `2px solid ${isPrimary ? "#00F0FF" : "rgba(255, 255, 255, 0.2)"}`,
                borderRadius: 14,
                padding: "14px 20px",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                boxShadow: isPrimary ? "0 0 25px rgba(0, 240, 255, 0.5)" : "0 8px 20px rgba(0,0,0,0.5)",
              }}
            >
              <div style={{ fontSize: 26, fontWeight: 900, color: "#FFFFFF" }}>
                {tok.text}
              </div>
              <div
                style={{
                  fontSize: 12,
                  fontWeight: 700,
                  color: isPrimary ? "#FF9E00" : "rgba(255,255,255,0.4)",
                  marginTop: 4,
                  fontFamily: "monospace",
                }}
              >
                {isPrimary ? "ATTN FOCUS" : `POS #${i + 1}`}
              </div>
            </div>
          );
        })}
      </div>

      {/* Formula Rail */}
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
        <div style={{ fontSize: 16, fontWeight: 800, color: "#FFFFFF", fontFamily: "monospace" }}>
          FORMULA: Softmax(Q · Kᵀ / √dₖ) · V
        </div>
        <div style={{ fontSize: 14, fontWeight: 700, color: "#FF9E00" }}>
          VASWANI ET AL. (2017)
        </div>
      </div>
    </div>
  );
};
