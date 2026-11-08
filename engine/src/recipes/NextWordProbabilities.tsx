import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const NextWordProbabilities: React.FC<{
  title?: string;
  subtitle?: string;
}> = ({
  title = "STEP 5: NEXT-TOKEN PROBABILITIES",
  subtitle = "Softmax output layer samples the most probable next word",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const candidates = [
    { word: "answers", prob: 0.684, percent: "68.4%", color: "#00F0FF", isWinner: true },
    { word: "generates", prob: 0.192, percent: "19.2%", color: "#3B82F6", isWinner: false },
    { word: "thinks", prob: 0.071, percent: "7.1%", color: "#FF9E00", isWinner: false },
    { word: "searches", prob: 0.038, percent: "3.8%", color: "#A78BFA", isWinner: false },
    { word: "stores", prob: 0.015, percent: "1.5%", color: "#64748B", isWinner: false },
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
        perspective: 1000,
        overflow: "hidden",
      }}
    >
      {/* Background Mesh */}
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

      {/* 3D Vertical Bars Stage */}
      <div
        style={{
          display: "flex",
          alignItems: "flex-end",
          justifyContent: "center",
          gap: 24,
          height: 380,
          width: 620,
          marginTop: 100,
          zIndex: 5,
        }}
      >
        {candidates.map((cand, idx) => {
          const s = spring({
            frame: frame - idx * 3,
            fps,
            config: { damping: 14, stiffness: 100 },
          });
          const barHeight = interpolate(s, [0, 1], [10, cand.prob * 320]);

          return (
            <div
              key={idx}
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                width: 90,
              }}
            >
              {/* Percentage Label */}
              <div
                style={{
                  fontSize: cand.isWinner ? 22 : 16,
                  fontWeight: 900,
                  color: cand.isWinner ? "#00F0FF" : "rgba(255,255,255,0.7)",
                  marginBottom: 8,
                  fontFamily: "monospace",
                  textShadow: cand.isWinner ? "0 0 15px rgba(0, 240, 255, 0.8)" : "none",
                }}
              >
                {cand.percent}
              </div>

              {/* 3D Pillar */}
              <div
                style={{
                  width: "100%",
                  height: barHeight,
                  backgroundColor: cand.isWinner ? "rgba(0, 240, 255, 0.35)" : "rgba(255, 255, 255, 0.08)",
                  border: `2px solid ${cand.color}`,
                  borderRadius: "12px 12px 4px 4px",
                  boxShadow: cand.isWinner
                    ? `0 0 35px ${cand.color}88, inset 0 0 20px ${cand.color}55`
                    : "0 8px 18px rgba(0,0,0,0.6)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  position: "relative",
                  backdropFilter: "blur(8px)",
                }}
              >
                {cand.isWinner && (
                  <div
                    style={{
                      position: "absolute",
                      top: 10,
                      backgroundColor: "#00F0FF",
                      color: "#000000",
                      fontSize: 12,
                      fontWeight: 900,
                      padding: "2px 8px",
                      borderRadius: 4,
                      letterSpacing: "1px",
                    }}
                  >
                    SAMPLED
                  </div>
                )}
              </div>

              {/* Word Tag */}
              <div
                style={{
                  marginTop: 12,
                  fontSize: cand.isWinner ? 22 : 18,
                  fontWeight: 900,
                  color: cand.isWinner ? "#FFFFFF" : "rgba(255,255,255,0.7)",
                  textAlign: "center",
                }}
              >
                "{cand.word}"
              </div>
            </div>
          );
        })}
      </div>

      {/* Softmax Temperature Rail */}
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
          SAMPLING: Top-P = 0.90 | Temperature = 0.7
        </div>
        <div style={{ fontSize: 16, fontWeight: 800, color: "#00F0FF", fontFamily: "monospace" }}>
          P(w | context) = softmax(z)
        </div>
      </div>
    </div>
  );
};
