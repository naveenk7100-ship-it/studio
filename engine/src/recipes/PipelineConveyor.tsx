import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

export const PipelineConveyor: React.FC<{
  title?: string;
  subtitle?: string;
}> = ({
  title = "THE BENCHMARK RACE: 5 PAGES",
  subtitle = "pypdfium2 finishes in 59ms while pure Python takes 386ms",
}) => {
  const frame = useCurrentFrame();

  const progressPypdf = Math.min(100, frame * 2.2);
  const progressPdfium = Math.min(100, frame * 14.5);

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

      {/* Conveyor Tracks */}
      <div
        style={{
          width: 640,
          marginTop: 110,
          display: "flex",
          flexDirection: "column",
          gap: 30,
          zIndex: 5,
        }}
      >
        {/* Track 1: pypdf */}
        <div
          style={{
            backgroundColor: "rgba(16, 22, 34, 0.85)",
            border: "1px solid rgba(255, 255, 255, 0.15)",
            borderRadius: 16,
            padding: "20px 24px",
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 10 }}>
            <div style={{ fontSize: 20, fontWeight: 800, color: "#FFFFFF" }}>
              pypdf (Pure Python)
            </div>
            <div style={{ fontSize: 18, fontWeight: 800, color: "#EF4444", fontFamily: "monospace" }}>
              386.77 ms
            </div>
          </div>
          <div
            style={{
              width: "100%",
              height: 18,
              backgroundColor: "rgba(0,0,0,0.4)",
              borderRadius: 9,
              overflow: "hidden",
            }}
          >
            <div
              style={{
                width: `${progressPypdf}%`,
                height: "100%",
                backgroundColor: "#EF4444",
                borderRadius: 9,
                transition: "width 0.1s linear",
              }}
            />
          </div>
        </div>

        {/* Track 2: pypdfium2 */}
        <div
          style={{
            backgroundColor: "rgba(0, 240, 255, 0.15)",
            border: "2px solid #00F0FF",
            borderRadius: 16,
            padding: "20px 24px",
            boxShadow: "0 0 30px rgba(0, 240, 255, 0.3)",
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 10 }}>
            <div style={{ fontSize: 22, fontWeight: 900, color: "#00F0FF" }}>
              pypdfium2 (Google C++ Engine)
            </div>
            <div style={{ fontSize: 22, fontWeight: 900, color: "#FF9E00", fontFamily: "monospace" }}>
              59.19 ms (FINISHED)
            </div>
          </div>
          <div
            style={{
              width: "100%",
              height: 22,
              backgroundColor: "rgba(0,0,0,0.4)",
              borderRadius: 11,
              overflow: "hidden",
            }}
          >
            <div
              style={{
                width: `${progressPdfium}%`,
                height: "100%",
                backgroundColor: "#00F0FF",
                boxShadow: "0 0 15px #00F0FF",
                borderRadius: 11,
                transition: "width 0.1s linear",
              }}
            />
          </div>
        </div>
      </div>

      {/* Execution Proof Rail */}
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
          REAL EXECUTION RUN ON ARXІV BENCHMARK
        </div>
        <div style={{ fontSize: 16, fontWeight: 800, color: "#FF9E00", fontFamily: "monospace" }}>
          THROUGHPUT: 84.5 PAGES/SEC
        </div>
      </div>
    </div>
  );
};
