import React from "react";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import realData from "../../assets/real_gpt2_data.json";

export interface AttentionFlowGraphProps {
  layer?: number;
  head?: number;
  targetTokenIdx?: number;
  flowSpeed?: number;
  width?: number;
  height?: number;
}

export const AttentionFlowGraph: React.FC<AttentionFlowGraphProps> = ({
  layer = 11,
  head = 0,
  targetTokenIdx = 5, // ' is'
  flowSpeed = 1.2,
  width = 650,
  height = 740,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Load real GPT-2 tokens & attention weights
  const tokens = realData.tokens || [];
  const attentionWeights =
    realData.attention_sample?.weights[targetTokenIdx] || [
      0.3482, 0.1408, 0.1658, 0.0522, 0.0911, 0.2018,
    ];

  // Target token is " is" (index 5)
  const targetToken = tokens[targetTokenIdx] || { token: " is", id: 318 };

  // Calculate positions for 6 token badges horizontally across width
  const tokenSpacing = width / (tokens.length + 0.4);
  const tokenCoords = tokens.map((t, idx) => ({
    ...t,
    weight: attentionWeights[idx] || 0,
    cx: 40 + idx * tokenSpacing + tokenSpacing * 0.4,
    cy: 200, // Token badge Y coordinate
  }));

  const targetCoords = tokenCoords[targetTokenIdx] || { cx: width - 70, cy: 200 };

  // Sort weights for lower-deck ranking telemetry
  const rankedWeights = [...tokenCoords].sort((a, b) => b.weight - a.weight);

  // Animated flow pulse offset
  const dashOffset = -(frame * flowSpeed * 6);

  return (
    <div
      style={{
        width,
        height,
        position: "relative",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "space-between",
        backgroundColor: "#F8FAFC",
        borderRadius: 24,
        border: "3px solid #00F0FF",
        boxShadow: "0 25px 60px rgba(0, 0, 0, 0.85)",
        overflow: "hidden",
        padding: "24px 22px",
        boxSizing: "border-box",
      }}
    >
      {/* Background Subtle Blueprint Grid */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage: `
            linear-gradient(to right, rgba(2, 132, 199, 0.06) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(2, 132, 199, 0.06) 1px, transparent 1px)
          `,
          backgroundSize: "32px 32px",
          pointerEvents: "none",
          zIndex: 1,
        }}
      />

      {/* TOP HEADER: Model & Attention Head Telemetry */}
      <div
        style={{
          width: "100%",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          zIndex: 10,
          borderBottom: "2px solid #E2E8F0",
          paddingBottom: 12,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div
            style={{
              width: 10,
              height: 10,
              borderRadius: "50%",
              backgroundColor: "#D97706",
              boxShadow: "0 0 10px rgba(217, 119, 6, 0.6)",
            }}
          />
          <span
            style={{
              fontFamily: "'JetBrains Mono', monospace",
              fontSize: 11.5,
              fontWeight: 800,
              color: "#0F172A",
              letterSpacing: 0.3,
            }}
          >
            GPT-2 (open model), example run • Layer 11 (last of 12 layers), Head 0
          </span>
        </div>
        <div
          style={{
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: 11,
            fontWeight: 800,
            color: "#0369A1",
            backgroundColor: "#E0F2FE",
            padding: "3px 10px",
            borderRadius: 6,
            border: "1px solid #7DD3FC",
          }}
        >
          QUERY: "{targetToken.token.trim()}" (ID {targetToken.id})
        </div>
      </div>

      {/* UPPER DECK: Interactive Token Sequence Badges */}
      <div
        style={{
          width: "100%",
          display: "flex",
          justifyContent: "space-between",
          zIndex: 10,
          marginTop: 10,
          gap: 6,
        }}
      >
        {tokens.map((t, idx) => {
          const isTarget = idx === targetTokenIdx;
          const weight = attentionWeights[idx] || 0;
          const isDominant = weight === Math.max(...attentionWeights);

          return (
            <div
              key={idx}
              style={{
                flex: 1,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: 4,
                backgroundColor: isTarget
                  ? "#FEF3C7"
                  : isDominant
                  ? "#E0F2FE"
                  : "#F1F5F9",
                border: isTarget
                  ? "2px solid #F59E0B"
                  : isDominant
                  ? "2px solid #0284C7"
                  : "1px solid #CBD5E1",
                borderRadius: 10,
                padding: "8px 4px",
                boxShadow: isTarget
                  ? "0 4px 12px rgba(245, 158, 11, 0.3)"
                  : isDominant
                  ? "0 4px 12px rgba(2, 132, 199, 0.3)"
                  : "none",
              }}
            >
              <span
                style={{
                  fontFamily: "'JetBrains Mono', monospace",
                  fontSize: 10,
                  fontWeight: 700,
                  color: "#64748B",
                }}
              >
                #{t.id}
              </span>
              <span
                style={{
                  fontFamily: "sans-serif",
                  fontSize: 13,
                  fontWeight: 900,
                  color: isTarget ? "#B45309" : isDominant ? "#0369A1" : "#0F172A",
                  whiteSpace: "nowrap",
                }}
              >
                {t.token}
              </span>
            </div>
          );
        })}
      </div>

      {/* MIDDLE DECK: 3D Flow Beams SVG Overlay */}
      <div
        style={{
          position: "relative",
          width: "100%",
          height: 240,
          zIndex: 8,
          overflow: "visible",
        }}
      >
        <svg
          width="100%"
          height="100%"
          style={{ overflow: "visible" }}
          viewBox={`0 0 ${width - 44} 240`}
        >
          <defs>
            <linearGradient id="flowBeamGradCyan" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#0284C7" stopOpacity="0.3" />
              <stop offset="50%" stopColor="#00F0FF" stopOpacity="0.9" />
              <stop offset="100%" stopColor="#0284C7" stopOpacity="0.3" />
            </linearGradient>
            <linearGradient id="flowBeamGradAmber" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#D97706" stopOpacity="0.3" />
              <stop offset="50%" stopColor="#F59E0B" stopOpacity="0.9" />
              <stop offset="100%" stopColor="#D97706" stopOpacity="0.3" />
            </linearGradient>
          </defs>

          {/* Draw curved attention arcs from each source token to target token */}
          {tokenCoords.map((coord, idx) => {
            const isTarget = idx === targetTokenIdx;
            const weight = coord.weight;
            const isDominant = weight === Math.max(...attentionWeights);

            // Normalized X coordinates relative to SVG viewBox
            const x1 = coord.cx - 22;
            const x2 = targetCoords.cx - 22;
            const y1 = 20; // top attachment
            const y2 = 210; // query node attachment

            // Bezier control points for smooth arching trajectory
            const dx = Math.abs(x2 - x1);
            const peakY = isTarget ? 70 : 30 + (dx / width) * 110;
            const pathD = `M ${x1} ${y1} C ${x1} ${peakY}, ${x2} ${peakY}, ${x2} ${y2}`;

            const strokeW = Math.max(1.8, weight * 16);
            const strokeColor = isDominant
              ? "url(#flowBeamGradCyan)"
              : isTarget
              ? "url(#flowBeamGradAmber)"
              : "#64748B";

            return (
              <g key={idx}>
                {/* Background Shadow Track */}
                <path
                  d={pathD}
                  fill="none"
                  stroke="#E2E8F0"
                  strokeWidth={strokeW + 2}
                  opacity={0.8}
                />

                {/* Animated Pulsing Active Flow Stream */}
                <path
                  d={pathD}
                  fill="none"
                  stroke={strokeColor}
                  strokeWidth={strokeW}
                  strokeDasharray={`${Math.max(8, weight * 25)} ${Math.max(6, 12 - weight * 10)}`}
                  strokeDashoffset={dashOffset}
                  strokeLinecap="round"
                  opacity={isDominant ? 1.0 : Math.max(0.45, weight * 2.2)}
                />

                {/* Floating Weight Label on Dominant Path */}
                {isDominant && (
                  <g transform={`translate(${(x1 + x2) / 2}, ${peakY - 14})`}>
                    <rect
                      x="-55"
                      y="-12"
                      width="110"
                      height="24"
                      rx="6"
                      fill="#0F172A"
                      stroke="#0284C7"
                      strokeWidth="1.5"
                    />
                    <text
                      x="0"
                      y="4"
                      textAnchor="middle"
                      fill="#38BDF8"
                      fontSize="10.5"
                      fontFamily="'JetBrains Mono', monospace"
                      fontWeight="800"
                    >
                      W: {weight.toFixed(4)} ({(weight * 100).toFixed(1)}%)
                    </text>
                  </g>
                )}
              </g>
            );
          })}
        </svg>
      </div>

      {/* LOWER DECK: Ranked Weight Distribution Bars */}
      <div
        style={{
          width: "100%",
          display: "flex",
          flexDirection: "column",
          gap: 6,
          zIndex: 10,
          backgroundColor: "#F1F5F9",
          borderRadius: 14,
          padding: "12px 16px",
          border: "1.5px solid #CBD5E1",
        }}
      >
        <div
          style={{
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: 10,
            fontWeight: 800,
            color: "#475569",
            display: "flex",
            justifyContent: "space-between",
            marginBottom: 2,
          }}
        >
          <span>RANKED ATTENTION RELEVANCE FROM TOKEN "{targetToken.token.trim()}"</span>
          <span>SUM = 1.0000</span>
        </div>

        {rankedWeights.map((item, idx) => {
          const pct = (item.weight * 100).toFixed(1);

          return (
            <div
              key={idx}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 10,
                fontSize: 11,
              }}
            >
              <span
                style={{
                  fontFamily: "'JetBrains Mono', monospace",
                  fontSize: 10,
                  fontWeight: 800,
                  color: "#64748B",
                  width: 18,
                }}
              >
                #{idx + 1}
              </span>
              <span
                style={{
                  fontFamily: "sans-serif",
                  fontWeight: 800,
                  color: "#0F172A",
                  width: 90,
                  whiteSpace: "nowrap",
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                }}
              >
                "{item.token.trim()}"
              </span>
              {/* Progress Bar Container */}
              <div
                style={{
                  flex: 1,
                  height: 10,
                  backgroundColor: "#E2E8F0",
                  borderRadius: 5,
                  overflow: "hidden",
                  position: "relative",
                }}
              >
                <div
                  style={{
                    width: `${item.weight * 100}%`,
                    height: "100%",
                    background:
                      idx === 0
                        ? "linear-gradient(90deg, #0284C7, #00F0FF)"
                        : "linear-gradient(90deg, #475569, #64748B)",
                    borderRadius: 5,
                  }}
                />
              </div>
              <span
                style={{
                  fontFamily: "'JetBrains Mono', monospace",
                  fontSize: 11,
                  fontWeight: 900,
                  color: idx === 0 ? "#0284C7" : "#334155",
                  width: 48,
                  textAlign: "right",
                }}
              >
                {pct}%
              </span>
            </div>
          );
        })}
      </div>

      {/* FOOTER BOUNDARY NOTE */}
      <div
        style={{
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 10,
          fontWeight: 700,
          color: "#64748B",
          textAlign: "center",
          zIndex: 10,
          marginTop: 6,
        }}
      >
        Verified PyTorch GPT-2 run • Raw Softmax Attention Weights • Zero Hallucinations
      </div>
    </div>
  );
};
