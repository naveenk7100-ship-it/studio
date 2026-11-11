import React from "react";
import { interpolate, staticFile, useCurrentFrame } from "remotion";
import realData from "../../../assets/real_pypdfium2_data.json";

export interface DocumentExtractionAdapterProps {
  title?: string;
  paperId?: string;
  pageNumber?: number;
  totalPages?: number;
  containerWidth?: number;
  containerHeight?: number;
}

export const DocumentExtractionAdapter: React.FC<DocumentExtractionAdapterProps> = ({
  title = "Attention Is All You Need",
  paperId = "arXiv:1706.03762",
  pageNumber = 1,
  totalPages = 15,
  containerWidth = 500,
  containerHeight = 600,
}) => {
  const frame = useCurrentFrame();

  const scanDuration = 90;
  const scanProgress = (frame % scanDuration) / scanDuration;
  const scanY = scanProgress * containerHeight;

  // Real extracted text blocks from pypdfium2
  const textBlocks = realData.text_blocks || [];
  const baseW = realData.source_render?.width || 1224;
  const baseH = realData.source_render?.height || 1584;

  const scaleX = containerWidth / baseW;
  const scaleY = containerHeight / baseH;

  const totalBlocks = textBlocks.length;
  const activeCount = Math.min(
    totalBlocks,
    Math.floor((frame / 120) * totalBlocks) + 1
  );

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        position: "relative",
        overflow: "hidden",
        backgroundColor: "#FFFFFF",
      }}
    >
      {/* Background Real Document Image */}
      <img
        src={staticFile("real_assets/arxiv_1706_03762_p1.png")}
        alt="arXiv Page 1"
        style={{
          width: "100%",
          height: "100%",
          objectFit: "fill",
          display: "block",
          opacity: 0.94,
        }}
      />

      {/* SVG Animated Bounding Boxes */}
      <svg
        style={{
          position: "absolute",
          inset: 0,
          width: "100%",
          height: "100%",
          pointerEvents: "none",
        }}
      >
        {textBlocks.map((b: any, idx: number) => {
          const x = b.box[0] * scaleX;
          const y = b.box[1] * scaleY;
          const w = (b.box[2] - b.box[0]) * scaleX;
          const h = (b.box[3] - b.box[1]) * scaleY;

          const isExtracted = idx < activeCount;
          const isScanningNow = Math.abs(y - scanY) < 30;

          if (!isExtracted && !isScanningNow) return null;

          return (
            <rect
              key={idx}
              x={x}
              y={y}
              width={w}
              height={h}
              fill={isScanningNow ? "rgba(2, 132, 199, 0.25)" : "rgba(16, 185, 129, 0.12)"}
              stroke={isScanningNow ? "#0284C7" : "rgba(16, 185, 129, 0.7)"}
              strokeWidth={isScanningNow ? 2 : 1.2}
              rx={3}
            />
          );
        })}
      </svg>

      {/* Animated Scanning Beam */}
      <div
        style={{
          position: "absolute",
          top: scanY,
          left: 0,
          right: 0,
          height: 3,
          background: "linear-gradient(90deg, transparent 0%, #0284C7 50%, transparent 100%)",
          boxShadow: "0 0 14px #0284C7",
          zIndex: 20,
          pointerEvents: "none",
        }}
      />

      {/* HUD Telemetry Overlay */}
      <div
        style={{
          position: "absolute",
          bottom: 12,
          left: 12,
          right: 12,
          backgroundColor: "rgba(15, 23, 42, 0.92)",
          backdropFilter: "blur(8px)",
          borderRadius: 8,
          padding: "6px 12px",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 10,
          color: "#F8FAFC",
          zIndex: 30,
        }}
      >
        <span style={{ color: "#38BDF8", fontWeight: 800 }}>
          PAGE {pageNumber}/{totalPages} • {paperId}
        </span>
        <span style={{ color: "#10B981", fontWeight: 800 }}>
          EXTRACTED {activeCount}/{totalBlocks} BLOCKS
        </span>
      </div>
    </div>
  );
};
