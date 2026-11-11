import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export interface FeatureItem {
  icon?: "sparkle" | "diamond" | "check" | "lightning" | "terminal";
  title: string;
  subtitle?: string;
  color?: string;
  metric?: string;
}

export interface FeatureBulletListProps {
  items: FeatureItem[];
  staggerFrames?: number;
  width?: number;
}

export const FeatureBulletList: React.FC<FeatureBulletListProps> = ({
  items,
  staggerFrames = 8,
  width = "100%",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const renderIcon = (type: FeatureItem["icon"] = "sparkle", color = "#0284C7") => {
    switch (type) {
      case "sparkle":
        return (
          <svg width="22" height="22" viewBox="0 0 24 24" fill={color}>
            <path d="M12 0L14.59 9.41L24 12L14.59 14.59L12 24L9.41 14.59L0 12L9.41 9.41L12 0Z" />
          </svg>
        );
      case "diamond":
        return (
          <div
            style={{
              width: 14,
              height: 14,
              transform: "rotate(45deg)",
              backgroundColor: color,
              borderRadius: 3,
            }}
          />
        );
      case "check":
        return (
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="20 6 9 17 4 12" />
          </svg>
        );
      case "lightning":
        return (
          <svg width="20" height="20" viewBox="0 0 24 24" fill={color}>
            <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
          </svg>
        );
      case "terminal":
        return (
          <span style={{ fontFamily: "'JetBrains Mono', monospace", fontWeight: 900, color, fontSize: 18 }}>
            &gt;_
          </span>
        );
    }
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: 14,
        width,
        boxSizing: "border-box",
      }}
    >
      {items.map((item, idx) => {
        const itemEntrance = spring({
          frame: frame - idx * staggerFrames,
          fps,
          config: { damping: 13, stiffness: 130 },
        });

        const opacity = interpolate(itemEntrance, [0, 1], [0, 1]);
        const translateX = interpolate(itemEntrance, [0, 1], [25, 0]);

        return (
          <div
            key={idx}
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              backgroundColor: "rgba(255, 255, 255, 0.9)",
              border: "1.5px solid #E2E8F0",
              borderRadius: 16,
              padding: "14px 18px",
              boxShadow: "0 4px 12px rgba(15, 23, 42, 0.04)",
              opacity,
              transform: `translateX(${translateX}px)`,
              boxSizing: "border-box",
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
              <div
                style={{
                  width: 36,
                  height: 36,
                  borderRadius: 10,
                  backgroundColor: "rgba(241, 245, 249, 0.8)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  flexShrink: 0,
                }}
              >
                {renderIcon(item.icon, item.color || "#0284C7")}
              </div>
              <div style={{ display: "flex", flexDirection: "column" }}>
                <span
                  style={{
                    fontSize: 20,
                    fontWeight: 800,
                    color: "#0F172A",
                    letterSpacing: "-0.3px",
                  }}
                >
                  {item.title}
                </span>
                {item.subtitle && (
                  <span
                    style={{
                      fontSize: 13,
                      fontWeight: 600,
                      color: "#64748B",
                      marginTop: 2,
                    }}
                  >
                    {item.subtitle}
                  </span>
                )}
              </div>
            </div>

            {item.metric && (
              <div
                style={{
                  fontFamily: "'JetBrains Mono', monospace",
                  fontSize: 15,
                  fontWeight: 900,
                  color: item.color || "#0284C7",
                  backgroundColor: "rgba(241, 245, 249, 0.9)",
                  padding: "4px 12px",
                  borderRadius: 8,
                  border: "1px solid #CBD5E1",
                }}
              >
                {item.metric}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};
