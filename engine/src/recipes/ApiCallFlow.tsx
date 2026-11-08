import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

export const ApiCallFlow: React.FC<{
  title?: string;
  subtitle?: string;
  codeSnippet?: string;
}> = ({
  title = "STEP 1: ABI STREAMING",
  subtitle = "Zero-copy C++ stream directly loads PDF pages into memory",
  codeSnippet = "import pypdfium2 as pdfium\ndoc = pdfium.PdfDocument('paper.pdf')\npage = doc.get_page(0)",
}) => {
  const frame = useCurrentFrame();

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

      {/* Code Card Container */}
      <div
        style={{
          width: 620,
          backgroundColor: "rgba(16, 24, 40, 0.9)",
          border: "2px solid #00F0FF",
          borderRadius: 20,
          padding: 26,
          boxShadow: "0 0 35px rgba(0, 240, 255, 0.35)",
          backdropFilter: "blur(14px)",
          marginTop: 110,
          zIndex: 5,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 16 }}>
          <div style={{ width: 12, height: 12, borderRadius: "50%", backgroundColor: "#EF4444" }} />
          <div style={{ width: 12, height: 12, borderRadius: "50%", backgroundColor: "#FF9E00" }} />
          <div style={{ width: 12, height: 12, borderRadius: "50%", backgroundColor: "#10B981" }} />
          <div style={{ fontSize: 13, color: "rgba(255,255,255,0.4)", marginLeft: 12, fontFamily: "monospace" }}>
            stream_loader.py
          </div>
        </div>
        <pre
          style={{
            margin: 0,
            fontSize: 20,
            lineHeight: 1.6,
            color: "#00F0FF",
            fontFamily: "monospace",
            whiteSpace: "pre-wrap",
          }}
        >
          {codeSnippet}
        </pre>
      </div>

      {/* Bottom Rail */}
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
          MEMORY FOOTPRINT: ZERO BUFFER BLOAT
        </div>
        <div style={{ fontSize: 16, fontWeight: 800, color: "#00F0FF" }}>
          STREAMING PAGE ITERATOR
        </div>
      </div>
    </div>
  );
};
