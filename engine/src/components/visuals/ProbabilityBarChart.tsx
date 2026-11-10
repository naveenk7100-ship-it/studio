import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import realData from "../../assets/real_gpt2_data.json";

export interface ProbabilityBarChartProps {
  promptText?: string;
  width?: number;
  height?: number;
  highlightTop?: boolean;
}

export const ProbabilityBarChart: React.FC<ProbabilityBarChartProps> = ({
  promptText = "The future of artificial intelligence is",
  width = 650,
  height = 740,
  highlightTop = true,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Load real GPT-2 top 5 predictions from real_gpt2_data.json
  const predictions = realData.top5_predictions || [
    { token_id: 8627, token_text: " uncertain", prob_raw: 0.07656, prob_pct: 7.66 },
    { token_id: 287, token_text: " in", prob_raw: 0.06942, prob_pct: 6.94 },
    { token_id: 407, token_text: " not", prob_raw: 0.04409, prob_pct: 4.41 },
    { token_id: 257, token_text: " a", prob_raw: 0.04067, prob_pct: 4.07 },
    { token_id: 991, token_text: " still", prob_raw: 0.03449, prob_pct: 3.45 },
  ];

  // Highest percentage is 7.66%
  const maxPct = predictions[0]?.prob_pct || 7.66;

  // Cumulative mass of top 5
  const cumulativePct = predictions
    .reduce((sum, p) => sum + p.prob_pct, 0)
    .toFixed(2);

  return (
    <div
      style={{
        width,
        height,
        position: "relative",
        display: "flex",
        flexDirection: "column",
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
      {/* Background Drafting Grid */}
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

      {/* TOP HEADER: Prompt & Architecture Specs */}
      <div
        style={{
          width: "100%",
          display: "flex",
          flexDirection: "column",
          gap: 10,
          zIndex: 10,
          borderBottom: "2px solid #E2E8F0",
          paddingBottom: 14,
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <div
              style={{
                width: 10,
                height: 10,
                borderRadius: "50%",
                backgroundColor: "#0284C7",
                boxShadow: "0 0 10px rgba(2, 132, 199, 0.6)",
              }}
            />
            <span
              style={{
                fontFamily: "'JetBrains Mono', monospace",
                fontSize: 11.5,
                fontWeight: 800,
                color: "#0F172A",
              }}
            >
              GPT-2 (open model), example run • Next-Token Softmax
            </span>
          </div>

          <span
            style={{
              fontFamily: "'JetBrains Mono', monospace",
              fontSize: 10.5,
              fontWeight: 800,
              color: "#0284C7",
              backgroundColor: "#E0F2FE",
              padding: "2px 8px",
              borderRadius: 6,
            }}
          >
            VOCAB: 50,257
          </span>
        </div>

        {/* Input prompt snippet */}
        <div
          style={{
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: 12.5,
            color: "#334155",
            fontWeight: 700,
            backgroundColor: "#F1F5F9",
            padding: "8px 12px",
            borderRadius: 8,
            border: "1px solid #CBD5E1",
          }}
        >
          INPUT: <span style={{ color: "#0284C7", fontWeight: 800 }}>"{promptText}"</span>
        </div>
      </div>

      {/* MIDDLE SECTION: 5 Ranked Next-Token Predictions */}
      <div
        style={{
          width: "100%",
          display: "flex",
          flexDirection: "column",
          gap: 10,
          zIndex: 10,
          margin: "10px 0",
        }}
      >
        {predictions.map((item, idx) => {
          const isWinner = idx === 0 && highlightTop;

          // Spring physics entrance per bar
          const barSpring = spring({
            frame: frame - idx * 5,
            fps,
            config: { damping: 16, stiffness: 120 },
          });

          // Bar width normalized to maxPct
          const fillRatio = Math.min(1.0, item.prob_pct / maxPct);
          const currentWidthPct = interpolate(barSpring, [0, 1], [0, fillRatio * 100]);

          return (
            <div
              key={item.token_id}
              style={{
                display: "flex",
                flexDirection: "column",
                gap: 6,
                backgroundColor: isWinner ? "#E0F2FE" : "#F1F5F9",
                border: isWinner ? "2px solid #0284C7" : "1.5px solid #CBD5E1",
                borderRadius: 14,
                padding: "10px 16px",
                boxShadow: isWinner ? "0 4px 15px rgba(2, 132, 199, 0.25)" : "none",
              }}
            >
              {/* Row 1: Rank, Token Text, Token ID, and Percentage */}
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                }}
              >
                <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                  <span
                    style={{
                      fontFamily: "'JetBrains Mono', monospace",
                      fontSize: 11,
                      fontWeight: 900,
                      color: isWinner ? "#FFFFFF" : "#475569",
                      backgroundColor: isWinner ? "#0284C7" : "#CBD5E1",
                      padding: "2px 8px",
                      borderRadius: 6,
                    }}
                  >
                    #{idx + 1}
                  </span>

                  {/* Token with visual subword space indicator ␣ */}
                  <span
                    style={{
                      fontFamily: "'JetBrains Mono', monospace",
                      fontSize: 17,
                      fontWeight: 900,
                      color: isWinner ? "#0369A1" : "#0F172A",
                      letterSpacing: 0.3,
                    }}
                  >
                    <span style={{ color: "#0284C7", opacity: 0.8 }}>␣</span>
                    {item.token_text.trim()}
                  </span>

                  {/* Token ID Monospace Tag */}
                  <span
                    style={{
                      fontFamily: "'JetBrains Mono', monospace",
                      fontSize: 11,
                      color: "#64748B",
                      fontWeight: 700,
                    }}
                  >
                    (ID {item.token_id})
                  </span>
                </div>

                {/* Percentage Readout */}
                <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  {isWinner && (
                    <span
                      style={{
                        fontFamily: "'JetBrains Mono', monospace",
                        fontSize: 10,
                        fontWeight: 900,
                        color: "#FFFFFF",
                        backgroundColor: "#0284C7",
                        padding: "3px 8px",
                        borderRadius: 6,
                      }}
                    >
                      TOP CANDIDATE
                    </span>
                  )}
                  <span
                    style={{
                      fontFamily: "'JetBrains Mono', monospace",
                      fontSize: 16,
                      fontWeight: 900,
                      color: isWinner ? "#0284C7" : "#0F172A",
                    }}
                  >
                    {item.prob_pct.toFixed(2)}%
                  </span>
                </div>
              </div>

              {/* Row 2: Smooth Animated Bar Track with Shimmer */}
              <div
                style={{
                  width: "100%",
                  height: 14,
                  backgroundColor: "#E2E8F0",
                  borderRadius: 7,
                  overflow: "hidden",
                  position: "relative",
                }}
              >
                <div
                  style={{
                    width: `${currentWidthPct}%`,
                    height: "100%",
                    background: isWinner
                      ? "linear-gradient(90deg, #0284C7 0%, #00F0FF 50%, #0284C7 100%)"
                      : "linear-gradient(90deg, #3B82F6 0%, #60A5FA 50%, #3B82F6 100%)",
                    backgroundSize: "200% 100%",
                    backgroundPosition: `${(frame * 4) % 200}% 0%`,
                    borderRadius: 7,
                  }}
                />
              </div>
            </div>
          );
        })}
      </div>

      {/* LOWER TELEMETRY: Entropy & Model Limits */}
      <div
        style={{
          width: "100%",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          zIndex: 10,
          backgroundColor: "#FEF3C7",
          border: "2px solid #F59E0B",
          borderRadius: 14,
          padding: "12px 18px",
        }}
      >
        <div style={{ display: "flex", flexDirection: "column", gap: 2 }}>
          <span
            style={{
              fontFamily: "'JetBrains Mono', monospace",
              fontSize: 11,
              fontWeight: 900,
              color: "#92400E",
              letterSpacing: 0.5,
            }}
          >
            TOP-5 SUM: {cumulativePct}% (HIGH ENTROPY)
          </span>
          <span style={{ fontSize: 13, fontWeight: 800, color: "#78350F" }}>
            Model is not confident. Output mass spread across 50k tokens.
          </span>
        </div>

        <div
          style={{
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: 22,
            fontWeight: 900,
            color: "#D97706",
          }}
        >
          {cumulativePct}%
        </div>
      </div>

      {/* FOOTER: Open Model Provenance Disclaimer */}
      <div
        style={{
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 10,
          fontWeight: 700,
          color: "#64748B",
          textAlign: "center",
          zIndex: 10,
          marginTop: 4,
        }}
      >
        PyTorch empirical run • 124M weights • Real next-token probabilities
      </div>
    </div>
  );
};
