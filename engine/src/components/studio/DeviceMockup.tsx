import React from "react";

export type DeviceType = "smartphone" | "window" | "terminal" | "paper";

export interface DeviceMockupProps {
  type?: DeviceType;
  title?: string;
  subtitle?: string;
  badge?: string;
  width?: number;
  height?: number;
  children: React.ReactNode;
}

export const DeviceMockup: React.FC<DeviceMockupProps> = ({
  type = "window",
  title = "Terminal // bash",
  subtitle,
  badge,
  width = "100%",
  height = "100%",
  children,
}) => {
  if (type === "smartphone") {
    return (
      <div
        style={{
          width,
          height,
          backgroundColor: "#0B0F19",
          borderRadius: 44,
          border: "4px solid #1E293B",
          boxShadow: `
            inset 0 0 0 2px rgba(255, 255, 255, 0.1),
            0 25px 50px -12px rgba(0, 0, 0, 0.25)
          `,
          position: "relative",
          overflow: "hidden",
          display: "flex",
          flexDirection: "column",
          boxSizing: "border-box",
        }}
      >
        {/* Dynamic Island / Speaker Notch */}
        <div
          style={{
            position: "absolute",
            top: 10,
            left: "50%",
            transform: "translateX(-50%)",
            width: 90,
            height: 22,
            backgroundColor: "#000000",
            borderRadius: 14,
            zIndex: 50,
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            padding: "0 8px",
            boxSizing: "border-box",
          }}
        >
          <div style={{ width: 8, height: 8, borderRadius: "50%", backgroundColor: "#1E293B" }} />
          <div style={{ width: 8, height: 8, borderRadius: "50%", backgroundColor: "#0284C7" }} />
        </div>

        {/* Screen Content Container */}
        <div
          style={{
            width: "100%",
            height: "100%",
            paddingTop: 40,
            paddingBottom: 16,
            paddingLeft: 16,
            paddingRight: 16,
            boxSizing: "border-box",
            overflow: "hidden",
            position: "relative",
          }}
        >
          {children}
        </div>
      </div>
    );
  }

  if (type === "terminal") {
    return (
      <div
        style={{
          width,
          height,
          backgroundColor: "#090D16",
          borderRadius: 20,
          border: "1.5px solid rgba(255, 255, 255, 0.12)",
          boxShadow: "0 20px 40px -10px rgba(15, 23, 42, 0.4)",
          display: "flex",
          flexDirection: "column",
          overflow: "hidden",
          boxSizing: "border-box",
        }}
      >
        {/* Window Chrome Header */}
        <div
          style={{
            height: 38,
            backgroundColor: "#0F172A",
            borderBottom: "1px solid rgba(255, 255, 255, 0.08)",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            padding: "0 14px",
            boxSizing: "border-box",
          }}
        >
          <div style={{ display: "flex", gap: 7, alignItems: "center" }}>
            <div style={{ width: 10, height: 10, borderRadius: "50%", backgroundColor: "#EF4444" }} />
            <div style={{ width: 10, height: 10, borderRadius: "50%", backgroundColor: "#F59E0B" }} />
            <div style={{ width: 10, height: 10, borderRadius: "50%", backgroundColor: "#10B981" }} />
          </div>
          <div
            style={{
              fontFamily: "'JetBrains Mono', monospace",
              fontSize: 12,
              fontWeight: 700,
              color: "#94A3B8",
              letterSpacing: "0.5px",
            }}
          >
            {title}
          </div>
          {badge ? (
            <div
              style={{
                fontFamily: "'JetBrains Mono', monospace",
                fontSize: 10,
                fontWeight: 800,
                color: "#00F0FF",
                backgroundColor: "rgba(0, 240, 255, 0.12)",
                padding: "2px 8px",
                borderRadius: 6,
              }}
            >
              {badge}
            </div>
          ) : (
            <div style={{ width: 40 }} />
          )}
        </div>

        {/* Terminal Content */}
        <div
          style={{
            flex: 1,
            padding: 20,
            fontFamily: "'JetBrains Mono', monospace",
            color: "#F8FAFC",
            overflow: "hidden",
            boxSizing: "border-box",
          }}
        >
          {children}
        </div>
      </div>
    );
  }

  if (type === "paper") {
    return (
      <div
        style={{
          width,
          height,
          backgroundColor: "#FFFFFF",
          borderRadius: 16,
          border: "1px solid #E2E8F0",
          boxShadow: `
            0 20px 40px -15px rgba(15, 23, 42, 0.15),
            0 0 0 1px rgba(0, 0, 0, 0.04)
          `,
          display: "flex",
          flexDirection: "column",
          overflow: "hidden",
          boxSizing: "border-box",
          position: "relative",
        }}
      >
        {/* Paper Header Strip */}
        <div
          style={{
            padding: "16px 20px 12px 20px",
            borderBottom: "1.5px solid #F1F5F9",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <div>
            <div style={{ fontSize: 13, fontWeight: 800, color: "#0284C7", fontFamily: "'JetBrains Mono', monospace" }}>
              {badge || "ARXIV RESEARCH SPECIFICATION"}
            </div>
            <div style={{ fontSize: 16, fontWeight: 900, color: "#0F172A", marginTop: 2 }}>
              {title}
            </div>
          </div>
          {subtitle && (
            <div style={{ fontSize: 12, fontWeight: 700, color: "#64748B", fontFamily: "'JetBrains Mono', monospace" }}>
              {subtitle}
            </div>
          )}
        </div>

        {/* Paper Content */}
        <div
          style={{
            flex: 1,
            padding: 18,
            boxSizing: "border-box",
            overflow: "hidden",
            position: "relative",
          }}
        >
          {children}
        </div>
      </div>
    );
  }

  // Default: macOS / Browser Application Window
  return (
    <div
      style={{
        width,
        height,
        backgroundColor: "#FFFFFF",
        borderRadius: 20,
        border: "1.5px solid #E2E8F0",
        boxShadow: `
          0 25px 50px -12px rgba(15, 23, 42, 0.12),
          0 0 0 1px rgba(0, 0, 0, 0.04)
        `,
        display: "flex",
        flexDirection: "column",
        overflow: "hidden",
        boxSizing: "border-box",
      }}
    >
      {/* App Window Chrome */}
      <div
        style={{
          height: 42,
          backgroundColor: "#F8FAFC",
          borderBottom: "1.5px solid #E2E8F0",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "0 16px",
          boxSizing: "border-box",
        }}
      >
        <div style={{ display: "flex", gap: 7, alignItems: "center" }}>
          <div style={{ width: 10, height: 10, borderRadius: "50%", backgroundColor: "#EF4444" }} />
          <div style={{ width: 10, height: 10, borderRadius: "50%", backgroundColor: "#F59E0B" }} />
          <div style={{ width: 10, height: 10, borderRadius: "50%", backgroundColor: "#10B981" }} />
        </div>

        {/* Centered URL / Address Pill */}
        <div
          style={{
            backgroundColor: "#EDF2F7",
            borderRadius: 8,
            padding: "4px 16px",
            fontSize: 12,
            fontWeight: 700,
            color: "#475569",
            fontFamily: "'JetBrains Mono', monospace",
            display: "flex",
            alignItems: "center",
            gap: 6,
          }}
        >
          <span style={{ color: "#10B981" }}>🔒</span>
          <span>{title}</span>
        </div>

        {badge ? (
          <div
            style={{
              fontSize: 11,
              fontWeight: 800,
              color: "#0284C7",
              backgroundColor: "rgba(2, 132, 199, 0.1)",
              padding: "3px 10px",
              borderRadius: 8,
            }}
          >
            {badge}
          </div>
        ) : (
          <div style={{ width: 40 }} />
        )}
      </div>

      {/* Main Body Content */}
      <div
        style={{
          flex: 1,
          padding: 22,
          boxSizing: "border-box",
          overflow: "hidden",
          position: "relative",
          display: "flex",
          flexDirection: "column",
        }}
      >
        {children}
      </div>
    </div>
  );
};
