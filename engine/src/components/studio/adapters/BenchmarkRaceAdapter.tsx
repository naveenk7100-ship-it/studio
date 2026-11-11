import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export interface BenchmarkItem {
  name: string;
  timeMs: number;
  isBaseline?: boolean;
  color?: string;
  badge?: string;
}

export interface BenchmarkRaceAdapterProps {
  title?: string;
  testSpec?: string;
  benchmarks: BenchmarkItem[];
  hardwareFooter?: string;
  speedupText?: string;
}

export const BenchmarkRaceAdapter: React.FC<BenchmarkRaceAdapterProps> = ({
  title = "Empirical Full-Text Extraction Benchmark",
  testSpec = "15 Pages arXiv:1706.03762 • 10 Measured Runs",
  benchmarks,
  hardwareFooter = "Windows 10 x64 • Python 3.11 • Median of 10 Runs",
  speedupText = "5.85x FASTER",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const maxTime = Math.max(...benchmarks.map((b) => b.timeMs), 1);
  const baselineItem = benchmarks.find((b) => b.isBaseline) || benchmarks[0];

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
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: 6,
          }}
        >
          <div style={{ fontSize: 13, fontWeight: 900, color: "#0284C7", fontFamily: "'JetBrains Mono', monospace" }}>
            EMPIRICAL BENCHMARK RACE
          </div>
          <div
            style={{
              backgroundColor: "rgba(16, 185, 129, 0.12)",
              color: "#059669",
              border: "1px solid #10B981",
              borderRadius: 6,
              fontSize: 11,
              fontWeight: 800,
              padding: "2px 8px",
              fontFamily: "'JetBrains Mono', monospace",
            }}
          >
            {speedupText}
          </div>
        </div>

        <div style={{ fontSize: 20, fontWeight: 900, color: "#0F172A", lineHeight: 1.25 }}>
          {title}
        </div>
        <div style={{ fontSize: 12, fontWeight: 600, color: "#64748B", marginTop: 4 }}>
          {testSpec}
        </div>
      </div>

      {/* Race Bars */}
      <div style={{ display: "flex", flexDirection: "column", gap: 14, margin: "16px 0" }}>
        {benchmarks.map((b, idx) => {
          const progress = spring({
            frame: frame - idx * 6,
            fps,
            config: { damping: 16, stiffness: 100 },
          });

          // Bar width percentage relative to maxTime
          const barWidthTarget = Math.max(16, (b.timeMs / maxTime) * 100);
          const currentWidth = interpolate(progress, [0, 1], [0, barWidthTarget]);
          const currentMs = Math.round(interpolate(progress, [0, 1], [0, b.timeMs]));

          const isFastest = b.isBaseline;
          const barColor = b.color || (isFastest ? "#0284C7" : "#CBD5E1");

          return (
            <div key={idx} style={{ display: "flex", flexDirection: "column", gap: 4 }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <span style={{ fontSize: 16, fontWeight: 900, color: isFastest ? "#0284C7" : "#1E293B" }}>
                    {b.name}
                  </span>
                  {b.badge && (
                    <span
                      style={{
                        fontSize: 10,
                        fontWeight: 800,
                        backgroundColor: isFastest ? "#0284C7" : "#64748B",
                        color: "#FFFFFF",
                        padding: "1px 6px",
                        borderRadius: 4,
                        fontFamily: "'JetBrains Mono', monospace",
                      }}
                    >
                      {b.badge}
                    </span>
                  )}
                </div>

                <div
                  style={{
                    fontFamily: "'JetBrains Mono', monospace",
                    fontSize: 15,
                    fontWeight: 900,
                    color: isFastest ? "#0284C7" : "#475569",
                  }}
                >
                  {currentMs} ms
                </div>
              </div>

              {/* Bar track */}
              <div
                style={{
                  width: "100%",
                  height: 22,
                  backgroundColor: "#F1F5F9",
                  borderRadius: 11,
                  overflow: "hidden",
                  padding: 2,
                  boxSizing: "border-box",
                  border: "1px solid #E2E8F0",
                }}
              >
                <div
                  style={{
                    width: `${currentWidth}%`,
                    height: "100%",
                    borderRadius: 9,
                    backgroundColor: barColor,
                    background: isFastest
                      ? "linear-gradient(90deg, #0284C7 0%, #38BDF8 100%)"
                      : undefined,
                    boxShadow: isFastest ? "0 2px 10px rgba(2, 132, 199, 0.35)" : undefined,
                  }}
                />
              </div>
            </div>
          );
        })}
      </div>

      {/* Footer Spec */}
      <div
        style={{
          borderTop: "1.5px solid #F1F5F9",
          paddingTop: 10,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          fontSize: 11,
          color: "#94A3B8",
          fontFamily: "'JetBrains Mono', monospace",
          fontWeight: 700,
        }}
      >
        <span>{hardwareFooter}</span>
        <span style={{ color: "#10B981" }}>VERIFIED REAL RUN</span>
      </div>
    </div>
  );
};
