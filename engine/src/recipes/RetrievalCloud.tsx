import React from "react";
import { useCurrentFrame } from "remotion";

export const RetrievalCloud: React.FC<{
  title?: string;
  subtitle?: string;
}> = ({
  title = "VECTOR RETRIEVAL: TOP-K NEAREST CHUNKS",
  subtitle = "Cosine similarity locates the most relevant research passages",
}) => {
  const frame = useCurrentFrame();

  const chunks = [
    { title: "arXiv:1706.03762 Sec 3.2", sim: 0.94, color: "#00F0FF" },
    { title: "Attention Matrix Proof", sim: 0.88, color: "#00F0FF" },
    { title: "FFN Dimension Expansion", sim: 0.79, color: "#FF9E00" },
    { title: "Positional Encoding Math", sim: 0.73, color: "#A78BFA" },
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
          background: "radial-gradient(circle at 50% 50%, rgba(0, 240, 255, 0.12) 0%, rgba(10, 14, 24, 0.98) 75%)",
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
            color: "#00F0FF",
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
        {chunks.map((c, i) => (
          <div
            key={i}
            style={{
              backgroundColor: "rgba(16, 24, 40, 0.85)",
              border: `1.5px solid ${c.color}`,
              borderRadius: 14,
              padding: "16px 20px",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              boxShadow: `0 4px 18px ${c.color}22`,
            }}
          >
            <div style={{ fontSize: 20, fontWeight: 800, color: "#FFFFFF" }}>
              {c.title}
            </div>
            <div
              style={{
                fontSize: 16,
                fontWeight: 900,
                color: c.color,
                fontFamily: "monospace",
              }}
            >
              SIM: {c.sim}
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
          border: "1px solid rgba(0, 240, 255, 0.3)",
          borderRadius: 14,
          padding: "14px 24px",
          backdropFilter: "blur(10px)",
          zIndex: 10,
        }}
      >
        <div style={{ fontSize: 16, fontWeight: 700, color: "#E0E6ED" }}>
          K-NEAREST NEIGHBORS (HNSW / FAISS)
        </div>
        <div style={{ fontSize: 16, fontWeight: 800, color: "#00F0FF" }}>
          QUERY LATENCY: 2.1 MS
        </div>
      </div>
    </div>
  );
};
