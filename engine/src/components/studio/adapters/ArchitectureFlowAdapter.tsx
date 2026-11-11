import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import realData from "../../../assets/real_gpt2_data.json";

export interface ArchitectureFlowAdapterProps {
  layer?: number;
  head?: number;
  mode?: "attention" | "probability";
  width?: number;
  height?: number;
}

export const ArchitectureFlowAdapter: React.FC<ArchitectureFlowAdapterProps> = ({
  layer = 11,
  head = 0,
  mode = "attention",
  width = 540,
  height = 580,
}) => {
  const frame = useCurrentFrame();

  const tokens = realData.tokens || [
    { text: "The", id: 464 },
    { text: " future", id: 2003 },
    { text: " of", id: 286 },
    { text: " artificial", id: 11666 },
    { text: " intelligence", id: 4430 },
    { text: " is", id: 318 },
  ];

  const targetIdx = 5; // ' is'
  const weights = realData.attention_sample?.weights[targetIdx] || [
    0.3482, 0.1408, 0.1658, 0.0522, 0.0911, 0.2018,
  ];

  const predictions = realData.top5_predictions || [
    { token_id: 8627, token_text: " uncertain", prob_pct: 7.66 },
    { token_id: 287, token_text: " in", prob_pct: 6.94 },
    { token_id: 407, token_text: " not", prob_pct: 4.41 },
    { token_id: 257, token_text: " a", prob_pct: 4.07 },
    { token_id: 991, token_text: " still", prob_pct: 3.45 },
  ];

  if (mode === "probability") {
    return (
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          height: "100%",
          padding: 6,
          boxSizing: "border-box",
          fontFamily: "'Inter', sans-serif",
        }}
      >
        <div>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
            <span style={{ fontSize: 13, fontWeight: 900, color: "#0284C7", fontFamily: "'JetBrains Mono', monospace" }}>
              SOFTMAX PROBABILITY DISTRIBUTION
            </span>
            <span
              style={{
                backgroundColor: "rgba(245, 158, 11, 0.12)",
                color: "#B45309",
                border: "1px solid #F59E0B",
                borderRadius: 6,
                fontSize: 11,
                fontWeight: 800,
                padding: "2px 8px",
                fontFamily: "'JetBrains Mono', monospace",
              }}
            >
              TOP-5 SUM: 26.53% (HIGH ENTROPY)
            </span>
          </div>

          <div style={{ fontSize: 18, fontWeight: 900, color: "#0F172A" }}>
            Next-Token Sampling: "The future of AI is..."
          </div>
        </div>

        {/* Probability Bars */}
        <div style={{ display: "flex", flexDirection: "column", gap: 10, margin: "14px 0" }}>
          {predictions.map((p, idx) => {
            const isTop = idx === 0;
            const barWidth = Math.min(100, (p.prob_pct / 8.0) * 100);

            return (
              <div key={idx} style={{ display: "flex", flexDirection: "column", gap: 3 }}>
                <div style={{ display: "flex", justifyContent: "space-between", fontSize: 14 }}>
                  <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                    <span
                      style={{
                        fontFamily: "'JetBrains Mono', monospace",
                        fontWeight: 800,
                        color: isTop ? "#0284C7" : "#0F172A",
                        backgroundColor: isTop ? "rgba(2, 132, 199, 0.1)" : "#F1F5F9",
                        padding: "2px 8px",
                        borderRadius: 6,
                      }}
                    >
                      '{p.token_text}'
                    </span>
                    <span style={{ fontSize: 11, color: "#64748B", fontFamily: "'JetBrains Mono', monospace" }}>
                      #{p.token_id}
                    </span>
                  </div>

                  <span
                    style={{
                      fontFamily: "'JetBrains Mono', monospace",
                      fontWeight: 900,
                      color: isTop ? "#0284C7" : "#475569",
                    }}
                  >
                    {p.prob_pct.toFixed(2)}%
                  </span>
                </div>

                <div
                  style={{
                    width: "100%",
                    height: 18,
                    backgroundColor: "#F1F5F9",
                    borderRadius: 9,
                    overflow: "hidden",
                    padding: 2,
                    boxSizing: "border-box",
                    border: "1px solid #E2E8F0",
                  }}
                >
                  <div
                    style={{
                      width: `${barWidth}%`,
                      height: "100%",
                      borderRadius: 7,
                      backgroundColor: isTop ? "#0284C7" : "#94A3B8",
                      background: isTop ? "linear-gradient(90deg, #0284C7 0%, #38BDF8 100%)" : undefined,
                    }}
                  />
                </div>
              </div>
            );
          })}
        </div>

        {/* Model Disclosure Footer */}
        <div
          style={{
            borderTop: "1.5px solid #F1F5F9",
            paddingTop: 8,
            display: "flex",
            justifyContent: "space-between",
            fontSize: 11,
            color: "#64748B",
            fontFamily: "'JetBrains Mono', monospace",
            fontWeight: 700,
          }}
        >
          <span>GPT-2 SMALL (124M) • OPEN PEDAGOGICAL MODEL</span>
          <span style={{ color: "#D97706" }}>CHATGPT WEIGHTS PROPRIETARY</span>
        </div>
      </div>
    );
  }

  // Attention flow mode
  const spacing = (width - 60) / tokens.length;

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        height: "100%",
        boxSizing: "border-box",
        fontFamily: "'Inter', sans-serif",
      }}
    >
      {/* Header */}
      <div>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
          <span style={{ fontSize: 13, fontWeight: 900, color: "#0284C7", fontFamily: "'JetBrains Mono', monospace" }}>
            MULTI-HEAD ATTENTION GRAPH
          </span>
          <span
            style={{
              backgroundColor: "rgba(2, 132, 199, 0.12)",
              color: "#0284C7",
              border: "1px solid #0284C7",
              borderRadius: 6,
              fontSize: 11,
              fontWeight: 800,
              padding: "2px 8px",
              fontFamily: "'JetBrains Mono', monospace",
            }}
          >
            LAYER {layer} (OF 12) • HEAD {head}
          </span>
        </div>

        <div style={{ fontSize: 18, fontWeight: 900, color: "#0F172A" }}>
          Query Token: <span style={{ color: "#0284C7" }}>' is'</span> attending to prompt context
        </div>
      </div>

      {/* Dynamic Attention Beams SVG Canvas */}
      <div style={{ position: "relative", height: 260, margin: "10px 0" }}>
        <svg style={{ position: "absolute", inset: 0, width: "100%", height: "100%" }}>
          {tokens.map((t, idx) => {
            const x = 30 + idx * spacing + spacing / 2;
            const targetX = 30 + targetIdx * spacing + spacing / 2;
            const w = weights[idx] || 0.1;

            const strokeW = Math.max(1.5, w * 14);
            const opacity = Math.max(0.2, w * 1.5);
            const dashOffset = -(frame * 2.5);

            return (
              <g key={idx}>
                <path
                  d={`M ${x} 60 C ${x} 140, ${targetX} 140, ${targetX} 200`}
                  fill="none"
                  stroke="#0284C7"
                  strokeWidth={strokeW}
                  strokeOpacity={opacity}
                  strokeDasharray="6 4"
                  strokeDashoffset={dashOffset}
                />
              </g>
            );
          })}
        </svg>

        {/* Top Tokens Row */}
        <div style={{ position: "absolute", top: 10, left: 20, right: 20, display: "flex", justifyContent: "space-between" }}>
          {tokens.map((t, idx) => (
            <div
              key={idx}
              style={{
                backgroundColor: "#FFFFFF",
                border: "1.5px solid #CBD5E1",
                borderRadius: 8,
                padding: "4px 8px",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                boxShadow: "0 2px 6px rgba(0,0,0,0.04)",
              }}
            >
              <span style={{ fontSize: 9, color: "#64748B", fontFamily: "'JetBrains Mono', monospace" }}>
                #{t.id}
              </span>
              <span style={{ fontSize: 13, fontWeight: 800, color: "#0F172A" }}>
                {t.text}
              </span>
            </div>
          ))}
        </div>

        {/* Bottom Attended Target Token */}
        <div style={{ position: "absolute", bottom: 10, left: "50%", transform: "translateX(-50%)" }}>
          <div
            style={{
              backgroundColor: "#0284C7",
              color: "#FFFFFF",
              borderRadius: 12,
              padding: "8px 20px",
              display: "flex",
              alignItems: "center",
              gap: 8,
              boxShadow: "0 6px 18px rgba(2, 132, 199, 0.35)",
            }}
          >
            <span style={{ fontSize: 11, fontFamily: "'JetBrains Mono', monospace" }}>QUERY #318</span>
            <span style={{ fontSize: 16, fontWeight: 900 }}>' is'</span>
          </div>
        </div>
      </div>

      {/* Attention Ranking List */}
      <div style={{ display: "flex", justifyContent: "space-between", borderTop: "1.5px solid #F1F5F9", paddingTop: 8 }}>
        <div style={{ fontSize: 11, color: "#64748B", fontFamily: "'JetBrains Mono', monospace" }}>
          PRIMARY ATTENTION WEIGHT: <span style={{ color: "#0284C7", fontWeight: 800 }}>'The' (34.82%)</span>
        </div>
        <div style={{ fontSize: 11, color: "#10B981", fontFamily: "'JetBrains Mono', monospace", fontWeight: 700 }}>
          MEASURED REAL WEIGHTS
        </div>
      </div>
    </div>
  );
};
