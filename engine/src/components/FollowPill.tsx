import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const FollowPill: React.FC<{
  brandText?: string;
  subtitle?: string;
}> = ({
  brandText = "@flash__ai__digital",
  subtitle = "Daily AI and dev updates, with sources",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Tap animation occurs at frame 36 (~1.2s into the end card)
  const tapFrame = 36;
  const isTapped = frame >= tapFrame;

  // Spring transition on tap
  const s = spring({
    frame: frame - tapFrame,
    fps,
    config: { damping: 12, stiffness: 140 },
  });

  const scale = isTapped ? interpolate(s, [0, 0.4, 1], [1, 0.88, 1]) : 1;
  const rippleOpacity = isTapped ? interpolate(s, [0, 1], [0.8, 0]) : 0;
  const rippleScale = isTapped ? interpolate(s, [0, 1], [1, 2.2]) : 1;

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        position: "relative",
      }}
    >
      {/* Tap Ripple Ring */}
      {isTapped && (
        <div
          style={{
            position: "absolute",
            width: 280,
            height: 64,
            borderRadius: 32,
            border: "2px solid #10B981",
            opacity: rippleOpacity,
            transform: `scale(${rippleScale})`,
            pointerEvents: "none",
          }}
        />
      )}

      {/* Main Follow Pill */}
      <div
        style={{
          transform: `scale(${scale})`,
          backgroundColor: isTapped ? "#10B981" : "#00F0FF",
          color: isTapped ? "#FFFFFF" : "#000000",
          borderRadius: 36,
          padding: "16px 36px",
          display: "flex",
          alignItems: "center",
          gap: 12,
          boxShadow: isTapped
            ? "0 0 35px rgba(16, 185, 129, 0.7)"
            : "0 0 35px rgba(0, 240, 255, 0.7)",
          cursor: "pointer",
          transition: "background-color 0.2s ease, box-shadow 0.2s ease",
        }}
      >
        {isTapped ? (
          <>
            {/* Checkmark Icon */}
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="20 6 9 17 4 12" />
            </svg>
            <div style={{ fontSize: 24, fontWeight: 900, letterSpacing: "1px" }}>
              FOLLOWING
            </div>
          </>
        ) : (
          <>
            {/* Plus / Follow Icon */}
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
              <line x1="12" y1="5" x2="12" y2="19" />
              <line x1="5" y1="12" x2="19" y2="12" />
            </svg>
            <div style={{ fontSize: 24, fontWeight: 900, letterSpacing: "0.5px" }}>
              FOLLOW {brandText}
            </div>
          </>
        )}
      </div>

      {/* Animated Tap Hand Pointer just before tap */}
      {frame >= tapFrame - 15 && frame < tapFrame + 18 && (
        <div
          style={{
            position: "absolute",
            right: 40,
            bottom: -10,
            transform: `translate(${frame < tapFrame ? (tapFrame - frame) * 3 : 0}px, ${frame < tapFrame ? (tapFrame - frame) * 3 : 0}px)`,
            pointerEvents: "none",
            filter: "drop-shadow(0 4px 8px rgba(0,0,0,0.6))",
          }}
        >
          <svg width="42" height="42" viewBox="0 0 24 24" fill="#FFFFFF">
            <path d="M9 11.24V7.5a2.5 2.5 0 0 1 5 0v3.74c1.21-.81 2-2.18 2-3.74a4.5 4.5 0 0 0-9 0c0 1.56.79 2.93 2 3.74zM12 2a5.5 5.5 0 0 1 5.5 5.5c0 1.83-.89 3.45-2.27 4.46L19 19H5l3.77-7.04A5.485 5.485 0 0 1 6.5 7.5 5.5 5.5 0 0 1 12 2z"/>
          </svg>
        </div>
      )}

      {/* Required Subtitle */}
      <div
        style={{
          marginTop: 20,
          fontSize: 20,
          fontWeight: 700,
          color: "rgba(255, 255, 255, 0.8)",
          textAlign: "center",
          letterSpacing: "0.5px",
        }}
      >
        {subtitle}
      </div>
    </div>
  );
};
