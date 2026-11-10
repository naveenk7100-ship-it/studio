import React from "react";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import realData from "../../assets/real_pypdfium2_data.json";

export interface BoundingBoxOverlayProps {
  containerWidth?: number;
  containerHeight?: number;
  scanDurationFrames?: number;
  showCoordinatesTag?: boolean;
  showBlockCounter?: boolean;
  activeColor?: string;
}

export const BoundingBoxOverlay: React.FC<BoundingBoxOverlayProps> = ({
  containerWidth = 580,
  containerHeight = 750,
  scanDurationFrames = 90,
  showCoordinatesTag = true,
  showBlockCounter = true,
  activeColor = "#00F0FF",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Scanline progress traversing from top (0) to bottom (containerHeight)
  const scanProgress = (frame % scanDurationFrames) / scanDurationFrames;
  const scanY = scanProgress * containerHeight;

  // Real data scaling factors:
  // Base coordinate system from pypdfium2 2x render: 1224 x 1584 px
  const baseW = realData.page1_render.width_px || 1224;
  const baseH = realData.page1_render.height_px || 1584;
  const scaleX = containerWidth / baseW;
  const scaleY = containerHeight / baseH;

  const boxes = realData.block_boxes_sample || [];

  // Identify currently active/scanned box
  let activeBox: (typeof boxes)[0] | null = null;
  let activeBoxScaled = { x: 0, y: 0, w: 0, h: 0 };

  return (
    <div
      style={{
        width: containerWidth,
        height: containerHeight,
        position: "relative",
        overflow: "hidden",
        pointerEvents: "none",
      }}
    >
      {/* 1. Animated Scanline Beam with trailing laser wash */}
      <div
        style={{
          position: "absolute",
          top: scanY,
          left: 0,
          right: 0,
          height: 2,
          backgroundColor: activeColor,
          boxShadow: `0 0 12px ${activeColor}, 0 0 4px #FFFFFF`,
          zIndex: 15,
        }}
      />
      <div
        style={{
          position: "absolute",
          top: Math.max(0, scanY - 32),
          left: 0,
          right: 0,
          height: 32,
          background: `linear-gradient(to top, rgba(0, 240, 255, 0.16) 0%, transparent 100%)`,
          zIndex: 14,
        }}
      />

      {/* 2. Real Bounding Box Rectangles */}
      {boxes.map((box, idx) => {
        const [x1, y1, x2, y2] = box.px_box;
        const bx = x1 * scaleX;
        const by = y1 * scaleY;
        const bw = Math.max(8, (x2 - x1) * scaleX);
        const bh = Math.max(6, (y2 - y1) * scaleY);

        // Active state: scanline is near or has reached this box
        const isPassed = scanY >= by;
        const isHovered = Math.abs(scanY - (by + bh / 2)) < 30;

        if (isHovered && !activeBox) {
          activeBox = box;
          activeBoxScaled = { x: bx, y: by, w: bw, h: bh };
        }

        const boxOpacity = isPassed ? (isHovered ? 1.0 : 0.65) : 0.15;
        const borderColor = isHovered ? "#FFFFFF" : activeColor;

        return (
          <div
            key={box.block_idx}
            style={{
              position: "absolute",
              left: bx,
              top: by,
              width: bw,
              height: bh,
              border: `1px solid ${borderColor}`,
              backgroundColor: isHovered
                ? "rgba(0, 240, 255, 0.22)"
                : isPassed
                ? "rgba(0, 240, 255, 0.06)"
                : "transparent",
              opacity: boxOpacity,
              boxSizing: "border-box",
              transition: "background-color 0.1s ease, border-color 0.1s ease",
              zIndex: isHovered ? 12 : 5,
            }}
          >
            {/* Precision Technical Corner Accent (top-left) */}
            <div
              style={{
                position: "absolute",
                top: -2,
                left: -2,
                width: 4,
                height: 4,
                borderTop: "1.5px solid #FFFFFF",
                borderLeft: "1.5px solid #FFFFFF",
              }}
            />
            {/* Precision Technical Corner Accent (bottom-right) */}
            <div
              style={{
                position: "absolute",
                bottom: -2,
                right: -2,
                width: 4,
                height: 4,
                borderBottom: "1.5px solid #FFFFFF",
                borderRight: "1.5px solid #FFFFFF",
              }}
            />
          </div>
        );
      })}

      {/* 3. Floating Coordinate Readout for currently scanned block */}
      {showCoordinatesTag && activeBox && (
        <div
          style={{
            position: "absolute",
            left: Math.min(containerWidth - 220, Math.max(10, activeBoxScaled.x)),
            top: Math.min(containerHeight - 48, activeBoxScaled.y + activeBoxScaled.h + 6),
            backgroundColor: "rgba(6, 12, 26, 0.94)",
            border: "1px solid rgba(0, 240, 255, 0.7)",
            borderRadius: 6,
            padding: "4px 8px",
            boxShadow: "0 6px 18px rgba(0, 0, 0, 0.8)",
            display: "flex",
            flexDirection: "column",
            gap: 2,
            zIndex: 25,
            backdropFilter: "blur(8px)",
          }}
        >
          <div
            style={{
              fontFamily: "'JetBrains Mono', monospace",
              fontSize: 9.5,
              fontWeight: 800,
              color: "#00F0FF",
              letterSpacing: 0.3,
            }}
          >
            RECT [{activeBox.pdf_coords[0].toFixed(1)}, {activeBox.pdf_coords[1].toFixed(1)}, {activeBox.pdf_coords[2].toFixed(1)}, {activeBox.pdf_coords[3].toFixed(1)}]
          </div>
          <div
            style={{
              fontFamily: "sans-serif",
              fontSize: 8.5,
              color: "#E2E8F0",
              maxWidth: 200,
              overflow: "hidden",
              textOverflow: "ellipsis",
              whiteSpace: "nowrap",
            }}
          >
            "{activeBox.text}"
          </div>
        </div>
      )}

      {/* 4. Top Telemetry Counter HUD */}
      {showBlockCounter && (
        <div
          style={{
            position: "absolute",
            top: 10,
            right: 12,
            backgroundColor: "rgba(5, 10, 22, 0.9)",
            border: "1px solid rgba(0, 240, 255, 0.4)",
            borderRadius: 6,
            padding: "4px 10px",
            display: "flex",
            alignItems: "center",
            gap: 8,
            zIndex: 20,
            backdropFilter: "blur(6px)",
          }}
        >
          <div
            style={{
              width: 6,
              height: 6,
              borderRadius: "50%",
              backgroundColor: activeColor,
              boxShadow: `0 0 6px ${activeColor}`,
            }}
          />
          <span
            style={{
              fontFamily: "'JetBrains Mono', monospace",
              fontSize: 10,
              fontWeight: 700,
              color: "#FFFFFF",
            }}
          >
            PYPDFIUM2: 67 BLOCKS DETECTED
          </span>
        </div>
      )}
    </div>
  );
};
