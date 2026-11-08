import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const ComparisonStage: React.FC<{
  title?: string;
  subtitle?: string;
  winnerTool?: string;
}> = ({
  title = "THE CONTENDERS: RESEARCH PDF EXTRACTION",
  subtitle = "Comparing Python PDF engines for LLM context pipelines",
  winnerTool = "pypdfium2",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const tools = [
    {
      name: "pypdf",
      tag: "Pure Python",
      speed: "386 ms (Slow)",
      layout: "Scrambled Columns",
      license: "BSD-3",
      isWinner: false,
      color: "#64748B",
    },
    {
      name: "pdfminer",
      tag: "Layout Parser",
      speed: "850+ ms (Heavy)",
      layout: "Complex AST Tree",
      license: "MIT",
      isWinner: false,
      color: "#64748B",
    },
    {
      name: "pypdfium2",
      tag: "Google PDFium C++",
      speed: "59 ms (6.5x Fast)",
      layout: "Clean Stream Flow",
      license: "Apache 2.0",
      isWinner: true,
      color: "#00F0FF",
    },
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

      {/* 3D Comparison Pedestals */}
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          gap: 18,
          width: 660,
          marginTop: 110,
          zIndex: 5,
        }}
      >
        {tools.map((t, idx) => {
          const s = spring({
            frame: frame - idx * 4,
            fps,
            config: { damping: 14, stiffness: 100 },
          });
          const translateY = interpolate(s, [0, 1], [60, 0]);
          const opacity = interpolate(s, [0, 1], [0, 1]);

          return (
            <div
              key={idx}
              style={{
                opacity,
                transform: `translateY(${translateY}px) scale(${t.isWinner ? 1.05 : 0.98})`,
                flex: 1,
                backgroundColor: t.isWinner ? "rgba(0, 240, 255, 0.18)" : "rgba(16, 22, 34, 0.85)",
                border: `2px solid ${t.isWinner ? "#00F0FF" : "rgba(255, 255, 255, 0.15)"}`,
                borderRadius: 20,
                padding: "24px 16px",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                boxShadow: t.isWinner
                  ? "0 0 40px rgba(0, 240, 255, 0.4), inset 0 0 20px rgba(0, 240, 255, 0.2)"
                  : "0 10px 25px rgba(0,0,0,0.6)",
                backdropFilter: "blur(12px)",
                position: "relative",
              }}
            >
              {t.isWinner && (
                <div
                  style={{
                    position: "absolute",
                    top: -14,
                    backgroundColor: "#FF9E00",
                    color: "#000000",
                    fontSize: 13,
                    fontWeight: 900,
                    padding: "4px 14px",
                    borderRadius: 20,
                    letterSpacing: "1px",
                    boxShadow: "0 0 15px rgba(255, 158, 0, 0.8)",
                  }}
                >
                  TOP PICK
                </div>
              )}

              <div
                style={{
                  fontSize: 28,
                  fontWeight: 900,
                  color: t.isWinner ? "#00F0FF" : "#FFFFFF",
                  marginBottom: 4,
                }}
              >
                {t.name}
              </div>
              <div
                style={{
                  fontSize: 13,
                  fontWeight: 700,
                  color: "rgba(255,255,255,0.6)",
                  textTransform: "uppercase",
                  letterSpacing: "1px",
                  marginBottom: 16,
                }}
              >
                {t.tag}
              </div>

              {/* Criteria Rails */}
              <div style={{ width: "100%", display: "flex", flexDirection: "column", gap: 10 }}>
                <div
                  style={{
                    backgroundColor: "rgba(0,0,0,0.3)",
                    padding: "8px 10px",
                    borderRadius: 8,
                  }}
                >
                  <div style={{ fontSize: 11, color: "rgba(255,255,255,0.4)", fontWeight: 700 }}>
                    5-PAGE SPEED
                  </div>
                  <div
                    style={{
                      fontSize: 15,
                      fontWeight: 800,
                      color: t.isWinner ? "#00F0FF" : "#FFFFFF",
                    }}
                  >
                    {t.speed}
                  </div>
                </div>

                <div
                  style={{
                    backgroundColor: "rgba(0,0,0,0.3)",
                    padding: "8px 10px",
                    borderRadius: 8,
                  }}
                >
                  <div style={{ fontSize: 11, color: "rgba(255,255,255,0.4)", fontWeight: 700 }}>
                    LAYOUT ACCURACY
                  </div>
                  <div style={{ fontSize: 13, fontWeight: 700, color: "#E0E6ED" }}>
                    {t.layout}
                  </div>
                </div>

                <div
                  style={{
                    backgroundColor: "rgba(0,0,0,0.3)",
                    padding: "8px 10px",
                    borderRadius: 8,
                  }}
                >
                  <div style={{ fontSize: 11, color: "rgba(255,255,255,0.4)", fontWeight: 700 }}>
                    LICENSE
                  </div>
                  <div style={{ fontSize: 13, fontWeight: 700, color: "#E0E6ED" }}>
                    {t.license}
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Benchmark Rail */}
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
          BENCHMARK: 2.43 MB PDF / 1,145 WORDS
        </div>
        <div style={{ fontSize: 16, fontWeight: 800, color: "#00F0FF", fontFamily: "monospace" }}>
          SPEEDUP: 6.5x FASTER
        </div>
      </div>
    </div>
  );
};
