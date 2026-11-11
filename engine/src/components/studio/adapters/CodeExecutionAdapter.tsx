import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

export interface StdoutLine {
  text: string;
  color?: string;
  isHeader?: boolean;
}

export interface CodeExecutionAdapterProps {
  command?: string;
  toolVersion?: string;
  lines: StdoutLine[];
  executionTimeMs?: number;
}

export const CodeExecutionAdapter: React.FC<CodeExecutionAdapterProps> = ({
  command = "python extract_bench.py --paper arxiv_1706.03762.pdf",
  toolVersion = "Python 3.11.9 • ctypes",
  lines,
  executionTimeMs = 239,
}) => {
  const frame = useCurrentFrame();

  // Command typing reveal
  const charsRevealed = Math.min(command.length, Math.floor(frame * 2.2));
  const displayedCommand = command.substring(0, charsRevealed);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100%",
        fontFamily: "'JetBrains Mono', monospace",
        color: "#0F172A",
        fontSize: 13,
        lineHeight: 1.5,
      }}
    >
      {/* Command Prompt Line */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 10,
          backgroundColor: "#F1F5F9",
          padding: "10px 14px",
          borderRadius: 10,
          marginBottom: 16,
          border: "1.5px solid #CBD5E1",
        }}
      >
        <span style={{ color: "#0284C7", fontWeight: 900 }}>$</span>
        <span style={{ color: "#0F172A", fontWeight: 700, fontSize: 13.5 }}>{displayedCommand}</span>
        {charsRevealed < command.length && (
          <span style={{ color: "#0284C7", fontWeight: 900 }}>▎</span>
        )}
      </div>

      {/* Stdout Output Area */}
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          gap: 8,
          overflow: "hidden",
        }}
      >
        {lines.map((l, idx) => {
          // Reveal line based on frame
          const lineStartFrame = 15 + idx * 7;
          if (frame < lineStartFrame) return null;

          return (
            <div
              key={idx}
              style={{
                color: l.color || "#334155",
                fontWeight: l.isHeader ? 900 : 600,
                fontSize: l.isHeader ? 14 : 13,
                borderLeft: l.isHeader ? "3.5px solid #0284C7" : undefined,
                paddingLeft: l.isHeader ? 8 : 0,
                lineHeight: 1.4,
              }}
            >
              {l.text}
            </div>
          );
        })}
      </div>

      {/* Execution Telemetry Footer */}
      <div
        style={{
          borderTop: "1.5px solid #F1F5F9",
          paddingTop: 10,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          fontSize: 11,
          color: "#64748B",
          fontWeight: 700,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
          <div
            style={{
              width: 8,
              height: 8,
              borderRadius: "50%",
              backgroundColor: "#059669",
            }}
          />
          <span>{toolVersion}</span>
        </div>
        <div style={{ color: "#0284C7" }}>
          EXIT: 0 • TIME: {executionTimeMs}ms
        </div>
      </div>
    </div>
  );
};
