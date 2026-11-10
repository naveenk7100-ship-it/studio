import React from "react";
import { interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

export interface Document3DViewProps {
  title?: string;
  paperId?: string;
  pageNumber?: number;
  totalPages?: number;
  authors?: string[];
  orgs?: string[];
  pageImageUrl?: string;
  cameraPitch?: number;
  zoomIntensity?: number;
  children?: React.ReactNode;
}

export const Document3DView: React.FC<Document3DViewProps> = ({
  title = "Attention Is All You Need",
  paperId = "arXiv:1706.03762",
  pageNumber = 1,
  totalPages = 15,
  authors = [
    "Ashish Vaswani*",
    "Noam Shazeer*",
    "Niki Parmar*",
    "Jakob Uszkoreit*",
    "Llion Jones*",
    "Aidan N. Gomez*†",
    "Łukasz Kaiser*",
    "Illia Polosukhin",
  ],
  orgs = ["Google Brain", "Google Research", "Univ. of Toronto"],
  pageImageUrl = staticFile("real_assets/arxiv_1706_03762_p1.png"),
  cameraPitch = 14,
  zoomIntensity = 1.0,
  children,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Smooth cinematic camera trajectory (Motion median >= 3.0, zero shake)
  // Continuous motivated translation and rotation
  const progress = interpolate(frame, [0, 150], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const rotX = interpolate(progress, [0, 1], [cameraPitch, cameraPitch - 6]);
  const rotY = interpolate(progress, [0, 1], [-6, 3]);
  const rotZ = interpolate(progress, [0, 1], [-1.0, 0.6]);
  const transZ = interpolate(progress, [0, 1], [0, 40 * zoomIntensity]);
  const scale = interpolate(progress, [0, 1], [0.92, 0.98]);
  const panY = interpolate(progress, [0, 1], [10, -10]);

  // Dynamic light sweep tracking camera
  const lightX = interpolate(frame % 120, [0, 60, 120], [20, 80, 20]);
  const lightY = interpolate(frame % 120, [0, 60, 120], [15, 65, 15]);

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
        backgroundColor: "#050914",
        perspective: 1100,
      }}
    >
      {/* DEPTH LAYER 1: Ambient Technical Blueprint Grid */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage: `
            linear-gradient(to right, rgba(0, 240, 255, 0.05) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(0, 240, 255, 0.05) 1px, transparent 1px)
          `,
          backgroundSize: "40px 40px",
          backgroundPosition: "center center",
          opacity: 0.8,
          zIndex: 1,
        }}
      />

      {/* DEPTH LAYER 2: Radial Spotlight Follow */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: `radial-gradient(circle at ${lightX}% ${lightY}%, rgba(0, 240, 255, 0.12) 0%, rgba(5, 9, 20, 0.95) 70%)`,
          zIndex: 2,
          pointerEvents: "none",
        }}
      />

      {/* DEPTH LAYER 3: 3D Camera Rig & Document Slab */}
      <div
        style={{
          width: 500,
          height: 640,
          position: "relative",
          zIndex: 10,
          transform: `
            rotateX(${rotX}deg)
            rotateY(${rotY}deg)
            rotateZ(${rotZ}deg)
            translateZ(${transZ}px)
            translateY(${panY}px)
            scale(${scale})
          `,
          transformStyle: "preserve-3d",
          transition: "transform 0.05s linear",
        }}
      >
        {/* Floor Drop Shadow */}
        <div
          style={{
            position: "absolute",
            inset: 0,
            transform: "translateZ(-40px) translateY(35px) scale(0.96)",
            background: "rgba(0, 0, 0, 0.85)",
            filter: "blur(32px)",
            borderRadius: 16,
            zIndex: 1,
          }}
        />

        {/* Paper Document Slab Surface */}
        <div
          style={{
            width: "100%",
            height: "100%",
            backgroundColor: "#FAFAFA",
            borderRadius: 14,
            border: "1.5px solid rgba(0, 240, 255, 0.4)",
            boxShadow:
              "0 25px 60px rgba(0, 0, 0, 0.75), 0 0 40px rgba(0, 240, 255, 0.15)",
            overflow: "hidden",
            position: "relative",
            zIndex: 2,
            transformStyle: "preserve-3d",
          }}
        >
          {pageImageUrl ? (
            /* Real Rendered Image */
            <img
              src={pageImageUrl}
              alt={title}
              style={{
                width: "100%",
                height: "100%",
                objectFit: "contain",
                display: "block",
              }}
            />
          ) : (
            /* Real arXiv Layout Vector Document */
            <div
              style={{
                width: "100%",
                height: "100%",
                padding: "24px 28px",
                boxSizing: "border-box",
                color: "#181A20",
                fontFamily: "'Times New Roman', Times, serif",
                fontSize: 11,
                lineHeight: 1.35,
                display: "flex",
                flexDirection: "column",
                position: "relative",
                background:
                  "linear-gradient(180deg, #FFFFFF 0%, #F5F6F8 100%)",
              }}
            >
              {/* Attribution Banner */}
              <div
                style={{
                  fontSize: 7.5,
                  color: "#666",
                  fontFamily: "sans-serif",
                  borderBottom: "0.5px solid #DDD",
                  paddingBottom: 4,
                  marginBottom: 12,
                }}
              >
                Provided proper attribution is provided, Google hereby grants
                permission to reproduce the tables and figures in this paper
                solely for journalistic or scholarly works.
              </div>

              {/* Real Paper Title */}
              <div
                style={{
                  textAlign: "center",
                  fontSize: 20,
                  fontWeight: 900,
                  letterSpacing: -0.3,
                  color: "#0A0D14",
                  marginBottom: 10,
                  fontFamily: "'Times New Roman', serif",
                }}
              >
                {title}
              </div>

              {/* Real Authors Grid */}
              <div
                style={{
                  display: "flex",
                  flexWrap: "wrap",
                  justifyContent: "center",
                  gap: "3px 12px",
                  fontSize: 8.5,
                  color: "#2C3E50",
                  marginBottom: 6,
                  fontFamily: "'Times New Roman', serif",
                }}
              >
                {authors.map((auth, idx) => (
                  <span key={idx} style={{ fontWeight: 600 }}>
                    {auth}
                  </span>
                ))}
              </div>

              {/* Institutions */}
              <div
                style={{
                  textAlign: "center",
                  fontSize: 8,
                  color: "#555",
                  fontFamily: "sans-serif",
                  marginBottom: 14,
                }}
              >
                {orgs.join(" • ")}
              </div>

              {/* Abstract Section */}
              <div
                style={{
                  borderTop: "1px solid #111",
                  borderBottom: "1px solid #111",
                  padding: "8px 12px",
                  marginBottom: 14,
                  backgroundColor: "rgba(0,0,0,0.02)",
                }}
              >
                <div
                  style={{
                    textAlign: "center",
                    fontWeight: 700,
                    fontSize: 10,
                    marginBottom: 4,
                    letterSpacing: 0.5,
                  }}
                >
                  ABSTRACT
                </div>
                <div
                  style={{
                    fontSize: 8,
                    textAlign: "justify",
                    lineHeight: 1.3,
                    color: "#222",
                  }}
                >
                  The dominant sequence transduction models are based on complex
                  recurrent or convolutional neural networks that include an
                  encoder and a decoder. The best performing models also connect
                  the encoder and decoder through an attention mechanism. We
                  propose a new simple network architecture, the Transformer,
                  based solely on attention mechanisms, dispensing with
                  recurrence and convolutions entirely. Experiments on two
                  machine translation tasks show these models to be superior in
                  quality while being more parallelizable and requiring
                  significantly less time to train.
                </div>
              </div>

              {/* Two Column Simulated Text Content */}
              <div
                style={{
                  display: "flex",
                  gap: 16,
                  flex: 1,
                  overflow: "hidden",
                }}
              >
                <div style={{ flex: 1, fontSize: 7.5, color: "#333" }}>
                  <div style={{ fontWeight: 700, marginBottom: 2 }}>
                    1 Introduction
                  </div>
                  Recurrent neural networks, long short-term memory and gated
                  recurrent neural networks in particular, have been firmly
                  established as state of the art approaches in sequence
                  modeling and transduction problems such as language modeling
                  and machine translation. Numerous efforts have since continued
                  to push the boundaries of recurrent language models and
                  encoder-decoder architectures...
                </div>
                <div style={{ flex: 1, fontSize: 7.5, color: "#333" }}>
                  Attention mechanisms have become an integral part of
                  compelling sequence modeling and transduction models in various
                  tasks, allowing modeling of dependencies without regard to
                  their distance in the input or output sequences. In all but a
                  few cases, however, such attention mechanisms are used in
                  conjunction with a recurrent network...
                </div>
              </div>

              {/* Page Number Footer */}
              <div
                style={{
                  position: "absolute",
                  bottom: 10,
                  left: 0,
                  right: 0,
                  textAlign: "center",
                  fontSize: 8,
                  color: "#888",
                  fontFamily: "sans-serif",
                }}
              >
                Page {pageNumber} of {totalPages}
              </div>
            </div>
          )}

          {/* Children slot (for BoundingBoxOverlay in same coordinate plane) */}
          {children && (
            <div
              style={{
                position: "absolute",
                inset: 0,
                zIndex: 20,
                pointerEvents: "none",
              }}
            >
              {children}
            </div>
          )}
        </div>

        {/* DEPTH LAYER 4: Floating 3D Telemetry HUD Tag (translateZ = +45px) */}
        <div
          style={{
            position: "absolute",
            top: -34,
            left: 12,
            transform: "translateZ(45px)",
            backgroundColor: "rgba(6, 14, 30, 0.95)",
            border: "1.5px solid rgba(0, 240, 255, 0.6)",
            borderRadius: 8,
            padding: "6px 14px",
            display: "flex",
            alignItems: "center",
            gap: 10,
            boxShadow:
              "0 8px 24px rgba(0, 0, 0, 0.8), 0 0 20px rgba(0, 240, 255, 0.25)",
            backdropFilter: "blur(10px)",
            zIndex: 30,
          }}
        >
          <div
            style={{
              width: 8,
              height: 8,
              borderRadius: "50%",
              backgroundColor: "#00F0FF",
              boxShadow: "0 0 8px #00F0FF",
            }}
          />
          <span
            style={{
              fontFamily: "'JetBrains Mono', monospace",
              fontSize: 12,
              fontWeight: 800,
              color: "#FFFFFF",
              letterSpacing: 0.5,
            }}
          >
            {paperId} • {totalPages} PAGES • 2.21 MB
          </span>
        </div>
      </div>
    </div>
  );
};
