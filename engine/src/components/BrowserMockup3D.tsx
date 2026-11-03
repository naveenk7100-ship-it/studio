import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

interface BrowserMockup3DProps {
  url: string;
  title: string;
  children: React.ReactNode;
}

export const BrowserMockup3D: React.FC<BrowserMockup3DProps> = ({
  url,
  title,
  children,
}) => {
  const frame = useCurrentFrame();

  // 3D tilt & smooth floating parallax
  const tiltX = 9 + Math.sin(frame * 0.08) * 2;
  const tiltY = -6 + Math.cos(frame * 0.06) * 2;
  const cursorX = interpolate(frame % 90, [0, 45, 90], [120, 680, 240]);
  const cursorY = interpolate(frame % 90, [0, 45, 90], [220, 420, 300]);

  return (
    <div
      style={{
        width: 1000,
        height: 1020, // 53.1% of 1920px canvas height (exceeds 45% gate)
        perspective: 1200,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        position: "relative",
      }}
    >
      <div
        style={{
          width: "100%",
          height: "100%",
          borderRadius: 28,
          background: "linear-gradient(180deg, #101628 0%, #080c16 100%)",
          border: "2px solid rgba(0, 240, 255, 0.45)",
          boxShadow:
            "0 35px 80px rgba(0, 0, 0, 0.9), 0 0 50px rgba(0, 240, 255, 0.18)",
          transform: `rotateX(${tiltX}deg) rotateY(${tiltY}deg)`,
          transformStyle: "preserve-3d",
          overflow: "hidden",
          display: "flex",
          flexDirection: "column",
        }}
      >
        {/* Top Browser Window Header */}
        <div
          style={{
            height: 70,
            background: "rgba(18, 25, 45, 0.95)",
            borderBottom: "1.5px solid rgba(0, 240, 255, 0.25)",
            display: "flex",
            alignItems: "center",
            padding: "0 24px",
            gap: 16,
          }}
        >
          {/* Traffic Lights */}
          <div style={{ display: "flex", gap: 10 }}>
            <div style={{ width: 16, height: 16, borderRadius: "50%", background: "#ff5f56" }} />
            <div style={{ width: 16, height: 16, borderRadius: "50%", background: "#ffbd2e" }} />
            <div style={{ width: 16, height: 16, borderRadius: "50%", background: "#27c93f" }} />
          </div>

          {/* URL Pill Bar */}
          <div
            style={{
              flex: 1,
              height: 42,
              borderRadius: 20,
              background: "rgba(7, 11, 20, 0.8)",
              border: "1px solid rgba(255, 255, 255, 0.15)",
              display: "flex",
              alignItems: "center",
              padding: "0 18px",
              gap: 10,
            }}
          >
            <span style={{ fontSize: 18, color: "#27c93f" }}>🔒</span>
            <span
              style={{
                fontFamily: "'Courier New', monospace",
                fontSize: 22,
                color: "#8892b0",
                overflow: "hidden",
                whiteSpace: "nowrap",
              }}
            >
              {url}
            </span>
          </div>
        </div>

        {/* Browser Body Area */}
        <div
          style={{
            flex: 1,
            position: "relative",
            padding: 40,
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
          }}
        >
          {children}

          {/* Smooth Virtual Cursor */}
          <div
            style={{
              position: "absolute",
              top: cursorY,
              left: cursorX,
              pointerEvents: "none",
              zIndex: 90,
              transition: "transform 0.05s ease-out",
            }}
          >
            <svg
              width="36"
              height="36"
              viewBox="0 0 24 24"
              fill="#ffffff"
              style={{
                filter: "drop-shadow(0 4px 10px rgba(0,0,0,0.8))",
              }}
            >
              <path d="M4 0L20 16L12 17L8 24L4 22L8 16L4 16Z" fill="#00f0ff" stroke="#ffffff" strokeWidth="1.5" />
            </svg>
          </div>
        </div>
      </div>
    </div>
  );
};
