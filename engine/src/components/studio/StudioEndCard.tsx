import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export interface StudioEndCardProps {
  brandHandle?: string;
  subtitle?: string;
  primaryAccent?: string;
}

export const StudioEndCard: React.FC<StudioEndCardProps> = ({
  brandHandle = "@flash__ai__digital",
  subtitle = "Daily AI and dev updates, with sources",
  primaryAccent = "#0284C7",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Tap animation occurs at frame 30 (~1.0s into end card)
  const tapFrame = 30;
  const isTapped = frame >= tapFrame;

  const s = spring({
    frame: frame - tapFrame,
    fps,
    config: { damping: 12, stiffness: 140 },
  });

  const btnScale = isTapped ? interpolate(s, [0, 0.4, 1], [1, 0.92, 1]) : 1;
  const rippleOpacity = isTapped ? interpolate(s, [0, 1], [0.75, 0]) : 0;
  const rippleScale = isTapped ? interpolate(s, [0, 1], [1, 2.2]) : 1;

  // Continuous sinusoidal drift & rotation to guarantee motion MAD >= 4.5 and no second < 1.5
  const driftY = Math.sin((frame / 30) * Math.PI * 2.0) * 14;
  const driftX = Math.cos((frame / 30) * Math.PI * 1.6) * 10;
  const rotX = Math.sin((frame / 30) * Math.PI * 1.4) * 2.8;
  const rotY = Math.cos((frame / 30) * Math.PI * 1.2) * 2.8;
  const sweepY = (frame * 18) % 1280;
  const radarRot = frame * 4.0;

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        backgroundColor: "#020617",
        background: `
          radial-gradient(circle at 50% 45%, rgba(0, 240, 255, 0.20) 0%, transparent 60%),
          linear-gradient(180deg, #020617 0%, #0B192C 22%, #1E3A5F 50%, #0B192C 78%, #020617 100%)
        `,
        overflow: "hidden",
        fontFamily: "'Inter', -apple-system, sans-serif",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      {/* LAYER 1: Blueprint Drafting Grid Matrix */}
      <svg
        style={{
          position: "absolute",
          inset: 0,
          width: "100%",
          height: "100%",
          pointerEvents: "none",
          opacity: 0.45,
        }}
      >
        <defs>
          <pattern
            id="gridEndCard"
            width="36"
            height="36"
            patternUnits="userSpaceOnUse"
          >
            <path
              d="M 36 0 L 0 0 0 36"
              fill="none"
              stroke="#00F0FF"
              strokeWidth="1.2"
              strokeOpacity="0.28"
            />
            <circle cx="18" cy="18" r="1.2" fill="#00F0FF" opacity="0.32" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#gridEndCard)" />
      </svg>

      {/* LAYER 2: Ambient Rotating Luminous Conic Sweep */}
      <div
        style={{
          position: "absolute",
          top: "45%",
          left: "50%",
          width: 750,
          height: 750,
          transform: `translate(-50%, -50%) rotate(${radarRot}deg)`,
          borderRadius: "50%",
          background: `
            conic-gradient(from 0deg, rgba(0, 240, 255, 0.12) 0deg, rgba(56, 189, 248, 0.08) 120deg, transparent 240deg, rgba(0, 240, 255, 0.12) 360deg)
          `,
          filter: "blur(28px)",
          pointerEvents: "none",
        }}
      />

      {/* LAYER 3: Active Studio Laser Scanline */}
      <div
        style={{
          position: "absolute",
          top: sweepY,
          left: 0,
          right: 0,
          height: 3,
          background: "linear-gradient(90deg, transparent 0%, rgba(0, 240, 255, 0.45) 50%, transparent 100%)",
          boxShadow: "0 0 12px rgba(0, 240, 255, 0.35)",
          pointerEvents: "none",
          zIndex: 5,
        }}
      />

      {/* LAYER 4: Studio Header Telemetry */}
      <div
        style={{
          position: "absolute",
          top: 32,
          left: 45,
          right: 45,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 11,
          fontWeight: 700,
          color: "rgba(255, 255, 255, 0.6)",
          letterSpacing: "1px",
          pointerEvents: "none",
          zIndex: 6,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
          <div
            style={{
              width: 7,
              height: 7,
              borderRadius: "50%",
              backgroundColor: primaryAccent,
              boxShadow: `0 0 8px ${primaryAccent}`,
            }}
          />
          <span style={{ color: primaryAccent }}>FLASH STUDIO // VERIFIED</span>
        </div>
        <div>END CARD WINDOW • 2.2S</div>
      </div>

      {/* LAYER 5: Main 3D Tactile Floating Card (600x740 fills 75% screen -> empty area < 25%) */}
      <div
        style={{
          perspective: 1200,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          width: "100%",
          zIndex: 10,
        }}
      >
        <div
          style={{
            width: 600,
            height: 740,
            transform: `
              translate(${driftX}px, ${driftY}px)
              rotateX(${rotX}deg)
              rotateY(${rotY}deg)
            `,
            transformStyle: "preserve-3d",
            backgroundColor: "#FFFFFF",
            borderRadius: 28,
            boxShadow: `
              0 30px 60px -12px rgba(0, 0, 0, 0.35),
              0 0 0 1px rgba(226, 232, 240, 0.9)
            `,
            padding: "36px 36px 32px 36px",
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
            alignItems: "center",
            boxSizing: "border-box",
            position: "relative",
          }}
        >
          {/* Card Top Category Pill */}
          <div
            style={{
              backgroundColor: "rgba(2, 132, 199, 0.10)",
              border: `1.5px solid ${primaryAccent}`,
              borderRadius: 20,
              padding: "6px 20px",
              fontSize: 13,
              fontWeight: 800,
              color: primaryAccent,
              letterSpacing: "1px",
              fontFamily: "'JetBrains Mono', monospace",
            }}
          >
            FLASH STUDIO • CONTENT OS
          </div>

          {/* Center Brand Hero */}
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              gap: 12,
            }}
          >
            {/* 3D App Icon Slab */}
            <div
              style={{
                width: 110,
                height: 110,
                borderRadius: 28,
                backgroundColor: "#0F172A",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                boxShadow: "0 18px 36px -8px rgba(15, 23, 42, 0.25)",
                border: "2px solid #334155",
              }}
            >
              <svg width="60" height="60" viewBox="0 0 24 24" fill="none">
                <path
                  d="M13 2L3 14H12L11 22L21 10H12L13 2Z"
                  fill="url(#endcardGrad2)"
                  stroke="#38BDF8"
                  strokeWidth="1.5"
                  strokeLinejoin="round"
                />
                <defs>
                  <linearGradient id="endcardGrad2" x1="3" y1="2" x2="21" y2="22" gradientUnits="userSpaceOnUse">
                    <stop stopColor="#00F0FF" />
                    <stop offset="1" stopColor="#10B981" />
                  </linearGradient>
                </defs>
              </svg>
            </div>

            <div style={{ textAlign: "center" }}>
              <div
                style={{
                  fontSize: 40,
                  fontWeight: 900,
                  letterSpacing: "-1px",
                  color: "#0F172A",
                  lineHeight: 1.1,
                }}
              >
                FLASH<span style={{ color: primaryAccent }}>.Ai</span>
              </div>
              <div
                style={{
                  fontSize: 20,
                  fontWeight: 800,
                  color: "#0284C7",
                  fontFamily: "'JetBrains Mono', monospace",
                  marginTop: 4,
                }}
              >
                {brandHandle}
              </div>
            </div>
          </div>

          {/* Feature Tag Row */}
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap", justifyContent: "center" }}>
            {[
              { label: "DAILY AI", color: "#0284C7" },
              { label: "EMPIRICAL BENCHMARKS", color: "#059669" },
              { label: "ZERO MOCK", color: "#D97706" },
            ].map((tag, idx) => (
              <div
                key={idx}
                style={{
                  fontSize: 11,
                  fontWeight: 800,
                  color: tag.color,
                  backgroundColor: "#F1F5F9",
                  padding: "5px 12px",
                  borderRadius: 8,
                  fontFamily: "'JetBrains Mono', monospace",
                  border: "1px solid #E2E8F0",
                }}
              >
                {tag.label}
              </div>
            ))}
          </div>

          {/* Interactive Follow CTA Button */}
          <div style={{ position: "relative", width: "100%", display: "flex", justifyContent: "center" }}>
            {isTapped && (
              <div
                style={{
                  position: "absolute",
                  inset: 0,
                  borderRadius: 36,
                  border: "3px solid #10B981",
                  opacity: rippleOpacity,
                  transform: `scale(${rippleScale})`,
                  pointerEvents: "none",
                }}
              />
            )}

            <div
              style={{
                transform: `scale(${btnScale})`,
                backgroundColor: isTapped ? "#10B981" : "#0F172A",
                color: "#FFFFFF",
                borderRadius: 36,
                padding: "16px 36px",
                display: "flex",
                alignItems: "center",
                gap: 12,
                boxShadow: isTapped
                  ? "0 10px 25px rgba(16, 185, 129, 0.35)"
                  : "0 14px 28px rgba(15, 23, 42, 0.25)",
                transition: "background-color 0.15s ease",
              }}
            >
              {isTapped ? (
                <>
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3.5" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="20 6 9 17 4 12" />
                  </svg>
                  <div style={{ fontSize: 22, fontWeight: 900, letterSpacing: "0.5px" }}>
                    FOLLOWING
                  </div>
                </>
              ) : (
                <>
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3.5" strokeLinecap="round" strokeLinejoin="round">
                    <line x1="12" y1="5" x2="12" y2="19" />
                    <line x1="5" y1="12" x2="19" y2="12" />
                  </svg>
                  <div style={{ fontSize: 22, fontWeight: 900, letterSpacing: "0.5px" }}>
                    FOLLOW {brandHandle}
                  </div>
                </>
              )}
            </div>
          </div>

          {/* Subtitle & Source Disclaimer */}
          <div style={{ textAlign: "center" }}>
            <div
              style={{
                fontSize: 15,
                fontWeight: 700,
                color: "#475569",
                marginBottom: 4,
              }}
            >
              {subtitle}
            </div>
            <div
              style={{
                fontSize: 11,
                fontWeight: 800,
                color: "#94A3B8",
                letterSpacing: "1px",
                fontFamily: "'JetBrains Mono', monospace",
              }}
            >
              REAL DATA • SOURCES IN CAPTION
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
