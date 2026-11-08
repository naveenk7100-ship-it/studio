import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

export const TransformerLayers: React.FC<{
  title?: string;
  subtitle?: string;
}> = ({
  title = "STEP 4: TRANSFORMER GLASS STACK",
  subtitle = "Information passes through stacked Attention + Feed-Forward layers",
}) => {
  const frame = useCurrentFrame();

  // Continuous camera flythrough / dolly forward
  const dollyZ = (frame * 6) % 360;
  const rotX = 54 + Math.sin(frame / 25) * 4;
  const rotZ = Math.sin(frame / 35) * 6;

  const layers = [
    { name: "Layer 1: Self-Attention", type: "Multi-Head Attention", color: "#00F0FF" },
    { name: "Layer 2: LayerNorm + Add", type: "Residual Connection", color: "#3B82F6" },
    { name: "Layer 3: Feed-Forward MLP", type: "Dense Projection (4x)", color: "#FF9E00" },
    { name: "Layer 4: LayerNorm + Output", type: "Norm & Output Heads", color: "#10B981" },
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
        perspective: 900,
        overflow: "hidden",
      }}
    >
      {/* Background Mesh */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: "radial-gradient(circle at 50% 40%, rgba(0, 240, 255, 0.15) 0%, rgba(10, 14, 24, 0.98) 80%)",
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

      {/* Stacked 3D Glass Plates Stage */}
      <div
        style={{
          width: 520,
          height: 520,
          position: "relative",
          marginTop: 100,
          transform: `rotateX(${rotX}deg) rotateZ(${rotZ}deg) translateY(${dollyZ * 0.4}px)`,
          transformStyle: "preserve-3d",
          zIndex: 5,
        }}
      >
        {/* Central Vertical Energy Column shooting through all plates */}
        <div
          style={{
            position: "absolute",
            left: "50%",
            top: "50%",
            width: 8,
            height: 600,
            transform: "translate(-50%, -50%) rotateX(-90deg)",
            background: "linear-gradient(to bottom, #00F0FF, #FF9E00, #10B981)",
            boxShadow: "0 0 35px #00F0FF, 0 0 60px #FF9E00",
            borderRadius: 4,
            opacity: 0.85,
          }}
        />

        {layers.map((lay, idx) => {
          const zOffset = (idx - 1.5) * 110;
          return (
            <div
              key={idx}
              style={{
                position: "absolute",
                inset: 30,
                transform: `translateZ(${zOffset}px)`,
                backgroundColor: "rgba(16, 24, 40, 0.65)",
                border: `2.5px solid ${lay.color}`,
                borderRadius: 24,
                boxShadow: `
                  0 0 30px ${lay.color}33,
                  inset 0 0 30px ${lay.color}22,
                  0 20px 40px rgba(0,0,0,0.7)
                `,
                backdropFilter: "blur(14px)",
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
                padding: "24px 30px",
                transformStyle: "preserve-3d",
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <div style={{ fontSize: 26, fontWeight: 900, color: "#FFFFFF" }}>
                  {lay.name}
                </div>
                <div
                  style={{
                    backgroundColor: lay.color,
                    color: "#000000",
                    fontWeight: 900,
                    fontSize: 14,
                    padding: "4px 10px",
                    borderRadius: 6,
                  }}
                >
                  BLOCK {idx + 1}/32
                </div>
              </div>

              {/* Data vectors grid inside plate */}
              <div style={{ display: "flex", justifyContent: "space-around", opacity: 0.8 }}>
                {Array.from({ length: 4 }).map((_, di) => (
                  <div
                    key={di}
                    style={{
                      width: 50,
                      height: 12,
                      backgroundColor: lay.color,
                      borderRadius: 4,
                      opacity: 0.4 + (di % 3) * 0.25,
                    }}
                  />
                ))}
              </div>

              <div style={{ fontSize: 16, fontWeight: 700, color: lay.color, fontFamily: "monospace" }}>
                TYPE: {lay.type}
              </div>
            </div>
          );
        })}
      </div>

      {/* Architecture Disclaimer Rail */}
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
          TRANSFORMER STACK: 32+ LAYERS IN PRODUCTION
        </div>
        <div style={{ fontSize: 14, fontWeight: 800, color: "#00F0FF" }}>
          (SIMPLIFIED 4-LAYER DIAGRAM SHOWN)
        </div>
      </div>
    </div>
  );
};
