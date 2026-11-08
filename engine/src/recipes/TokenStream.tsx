import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export interface TokenItem {
  text: string;
  id: number;
}

export const TokenStream: React.FC<{
  tokens: TokenItem[];
  title?: string;
  subtitle?: string;
  activeTokenIndex?: number;
}> = ({
  tokens,
  title = "STEP 1: BYTE-PAIR ENCODING",
  subtitle = "Raw text is sliced into numerical token vectors",
  activeTokenIndex,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Continuous camera drift
  const camY = Math.sin(frame / 20) * 12;
  const camRotX = 14 + Math.sin(frame / 25) * 3;
  const camRotY = Math.cos(frame / 30) * 4;

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
        perspective: 1200,
        overflow: "hidden",
      }}
    >
      {/* Background 3D Perspective Grid */}
      <div
        style={{
          position: "absolute",
          inset: -300,
          backgroundImage: `
            linear-gradient(to right, rgba(0, 240, 255, 0.08) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(0, 240, 255, 0.08) 1px, transparent 1px)
          `,
          backgroundSize: "60px 60px",
          transform: `rotateX(68deg) translateY(${frame * 2}px) translateZ(-150px)`,
          transformOrigin: "center 70%",
          pointerEvents: "none",
        }}
      />

      {/* Floating Ambient Depth Particles */}
      {Array.from({ length: 18 }).map((_, i) => {
        const pY = ((i * 70 + frame * (1.2 + (i % 3) * 0.4)) % 1350) - 50;
        const pX = (i * 41) % 680 + 20;
        const size = 3 + (i % 4) * 2;
        const opacity = 0.2 + (i % 5) * 0.15;
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: pX,
              top: pY,
              width: size,
              height: size,
              borderRadius: "50%",
              backgroundColor: i % 2 === 0 ? "#00F0FF" : "#FF9E00",
              opacity,
              boxShadow: `0 0 12px ${i % 2 === 0 ? "#00F0FF" : "#FF9E00"}`,
              transform: `translateZ(${i * 15 - 100}px)`,
            }}
          />
        );
      })}

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

      {/* 3D Token Tiles Stage */}
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          gap: 16,
          maxWidth: 660,
          marginTop: 140,
          transform: `translateY(${camY}px) rotateX(${camRotX}deg) rotateY(${camRotY}deg)`,
          transformStyle: "preserve-3d",
          zIndex: 5,
        }}
      >
        {tokens.map((tok, idx) => {
          const delay = idx * 2.5;
          const s = spring({
            frame: frame - delay,
            fps,
            config: { damping: 14, stiffness: 120 },
          });
          const scale = interpolate(s, [0, 1], [0.4, 1]);
          const opacity = interpolate(s, [0, 1], [0, 1]);
          const isHighlight =
            activeTokenIndex !== undefined
              ? activeTokenIndex === idx
              : Math.floor(frame / 12) % tokens.length === idx;

          return (
            <div
              key={idx}
              style={{
                opacity,
                transform: `scale(${scale}) translateZ(${isHighlight ? 50 : 0}px)`,
                backgroundColor: isHighlight
                  ? "rgba(0, 240, 255, 0.22)"
                  : "rgba(16, 22, 34, 0.88)",
                border: `2px solid ${isHighlight ? "#00F0FF" : "rgba(255, 255, 255, 0.15)"}`,
                borderRadius: 16,
                padding: "16px 22px",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                boxShadow: isHighlight
                  ? "0 0 35px rgba(0, 240, 255, 0.5), inset 0 0 15px rgba(0, 240, 255, 0.3)"
                  : "0 12px 28px rgba(0, 0, 0, 0.6)",
                backdropFilter: "blur(12px)",
                transition: "all 0.2s ease",
              }}
            >
              <div
                style={{
                  fontSize: 18,
                  fontWeight: 700,
                  color: isHighlight ? "#00F0FF" : "rgba(255, 255, 255, 0.5)",
                  fontFamily: "monospace",
                  marginBottom: 6,
                  letterSpacing: "1px",
                }}
              >
                ID: {tok.id}
              </div>
              <div
                style={{
                  fontSize: 34,
                  fontWeight: 900,
                  color: "#FFFFFF",
                  fontFamily: "sans-serif",
                  letterSpacing: "-0.5px",
                }}
              >
                "{tok.text}"
              </div>
              <div
                style={{
                  marginTop: 8,
                  fontSize: 14,
                  fontWeight: 800,
                  color: isHighlight ? "#FF9E00" : "rgba(0, 240, 255, 0.7)",
                  textTransform: "uppercase",
                  letterSpacing: "1px",
                }}
              >
                TOKEN #{idx + 1}
              </div>
            </div>
          );
        })}
      </div>

      {/* Bottom Technical Spec Rail */}
      <div
        style={{
          position: "absolute",
          bottom: 150,
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
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div
            style={{
              width: 12,
              height: 12,
              borderRadius: "50%",
              backgroundColor: "#00F0FF",
              boxShadow: "0 0 10px #00F0FF",
            }}
          />
          <div style={{ fontSize: 16, fontWeight: 700, color: "#E0E6ED" }}>
            BPE TOKENIZER: cl100k_base
          </div>
        </div>
        <div style={{ fontSize: 16, fontWeight: 800, color: "#00F0FF", fontFamily: "monospace" }}>
          VOCAB: 100,277 TOKENS
        </div>
      </div>
    </div>
  );
};
