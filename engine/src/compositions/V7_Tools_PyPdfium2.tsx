import React from "react";
import {
  AbsoluteFill,
  Audio,
  Img,
  interpolate,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

import { FollowPill } from "../components/FollowPill";
import wordsTools from "../assets/v7_tools_words.json";

export const V7_Tools_PyPdfium2: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  // Dynamic light sweep
  const lightX = 360 + Math.sin(frame / 22) * 190;
  const lightY = 640 + Math.cos(frame / 26) * 240;

  // Active laser scanline traversing top to bottom
  const scanY = ((frame * 7) % 1280);

  // Continuous Camera Movement (Zero Shake, Constant Motivated Push)
  const camZoom = 1.0 + (frame / 1440) * 0.12;
  const camPanX = Math.sin(frame * 0.03) * 12;
  const camPanY = Math.cos(frame * 0.025) * 8;

  // Active Word Highlight
  const currentSec = frame / 30;
  const activeWordObj = (wordsTools as any[]).find(
    (w) => currentSec >= w.start && currentSec <= w.end
  );
  const activeWord = activeWordObj ? activeWordObj.word : "";

  // Captions (Strictly hides after 45.6s, before end card at 45.8s)
  const renderSubtitles = () => {
    if (frame >= 1374 || currentSec > 45.6) return null;
    const activeIdx = (wordsTools as any[]).findIndex(
      (w) => currentSec >= w.start && currentSec <= w.end
    );
    if (activeIdx === -1) return null;

    const startIdx = Math.max(0, activeIdx - 1);
    const endIdx = Math.min(wordsTools.length, activeIdx + 2);
    const slice = (wordsTools as any[]).slice(startIdx, endIdx);

    return (
      <div
        style={{
          position: "absolute",
          bottom: 210,
          left: 40,
          right: 40,
          textAlign: "center",
          zIndex: 100,
          display: "flex",
          justifyContent: "center",
          gap: 16,
          flexWrap: "wrap",
        }}
      >
        <div
          style={{
            backgroundColor: "rgba(10, 18, 34, 0.94)",
            border: "2px solid rgba(0, 240, 255, 0.6)",
            borderRadius: 24,
            padding: "14px 28px",
            boxShadow: "0 12px 36px rgba(0, 0, 0, 0.85)",
            backdropFilter: "blur(14px)",
            display: "flex",
            gap: 14,
            alignItems: "center",
          }}
        >
          {slice.map((item, idx) => {
            const isCurrent = item.word === activeWord;
            return (
              <span
                key={idx}
                style={{
                  fontSize: 56, // Gate: >= 56px
                  fontWeight: 900,
                  color: isCurrent ? "#00F0FF" : "#FFFFFF",
                  textShadow: isCurrent
                    ? "0 0 25px rgba(0, 240, 255, 0.9), 0 2px 10px rgba(0,0,0,0.9)"
                    : "0 2px 8px rgba(0,0,0,0.8)",
                  background: isCurrent ? "rgba(0, 240, 255, 0.16)" : "transparent",
                  padding: "2px 10px",
                  borderRadius: 8,
                }}
              >
                {item.word}
              </span>
            );
          })}
        </div>
      </div>
    );
  };

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#050C18",
        color: "#FFFFFF",
        fontFamily: "'Inter', sans-serif",
        overflow: "hidden",
      }}
    >
      {/* LAYER 1: Master Audio Track */}
      <Audio src={staticFile("audio/v7_tools_master_48k.mp3")} />

      {/* LAYER 2: Camera Rig with Multi-Stop Radial Mesh Background & Drafting Grid */}
      <div
        style={{
          position: "absolute",
          inset: -40,
          transform: `scale(${camZoom}) translate(${camPanX}px, ${camPanY}px)`,
          transformOrigin: "center center",
        }}
      >
        {/* Dynamic Multi-stop Dual Radial Gradient Lighting */}
        <div
          style={{
            position: "absolute",
            inset: 0,
            background: `radial-gradient(circle 800px at ${lightX}px ${lightY}px, #1a4275 0%, #0c203d 45%, #030812 90%), radial-gradient(circle 650px at ${720 - lightX}px ${1280 - lightY}px, rgba(255, 158, 0, 0.22) 0%, transparent 70%)`,
          }}
        />

        {/* Technical Drafting Blueprint Grid with 20px pitch and Crosshairs */}
        <svg
          width="100%"
          height="100%"
          style={{
            position: "absolute",
            inset: 0,
            opacity: 0.65,
          }}
        >
          <defs>
            <pattern
              id="blueprintGridTools"
              width="20"
              height="20"
              patternUnits="userSpaceOnUse"
            >
              <path
                d="M 20 0 L 0 0 0 20"
                fill="none"
                stroke="rgba(0, 240, 255, 0.55)"
                strokeWidth="1.2"
              />
              <path
                d="M 10 7 L 10 13 M 7 10 L 13 10"
                stroke="rgba(255, 158, 0, 0.85)"
                strokeWidth="1.2"
              />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#blueprintGridTools)" />
        </svg>

        {/* Continuous Active Laser Scanline */}
        <div
          style={{
            position: "absolute",
            top: scanY,
            left: 0,
            right: 0,
            height: 4,
            background: "linear-gradient(90deg, transparent 0%, rgba(0, 240, 255, 0.95) 50%, transparent 100%)",
            boxShadow: "0 0 20px #00F0FF",
            opacity: 0.85,
          }}
        />

        {/* Floating Particles for continuous 3D depth */}
        {Array.from({ length: 24 }).map((_, i) => {
          const pY = ((i * 55 + frame * (2.4 + (i % 3) * 0.8)) % 1340) - 20;
          const pX = (i * 31) % 720 + 10;
          const sz = 3 + (i % 3) * 2;
          return (
            <div
              key={i}
              style={{
                position: "absolute",
                left: pX,
                top: pY,
                width: sz,
                height: sz,
                borderRadius: "50%",
                backgroundColor: i % 2 === 0 ? "#00F0FF" : "#FF9E00",
                opacity: 0.45 + (i % 4) * 0.15,
                boxShadow: `0 0 10px ${i % 2 === 0 ? "#00F0FF" : "#FF9E00"}`,
              }}
            />
          );
        })}

        {/* SCENE CONTENT (Frames 0 - 1374, 0.0s - 45.8s) */}
        <div style={{ position: "absolute", inset: 0, zIndex: 10 }}>
          {/* BEAT 1 (Frames 0 - 360, 0.0s - 12.0s): Dual Column PDF Problem & Benchmark Race */}
          <Sequence from={0} durationInFrames={360}>
            <div
              style={{
                width: "100%",
                height: "100%",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                paddingTop: 140,
              }}
            >
              {/* Category Pill (NO BRAND LOGO) */}
              <div
                style={{
                  backgroundColor: "rgba(0, 240, 255, 0.15)",
                  border: "1.5px solid #00F0FF",
                  borderRadius: 20,
                  padding: "6px 20px",
                  fontSize: 18,
                  fontWeight: 900,
                  color: "#00F0FF",
                  letterSpacing: "1.5px",
                  marginBottom: 20,
                }}
              >
                TOOLS & WORKFLOWS
              </div>

              {/* Main Headline */}
              <div
                style={{
                  fontSize: 62,
                  fontWeight: 900,
                  textAlign: "center",
                  lineHeight: 1.15,
                  maxWidth: 640,
                  marginBottom: 30,
                  color: "#FFFFFF",
                  textShadow: "0 4px 20px rgba(0,0,0,0.8)",
                }}
              >
                PDF Parsing for <span style={{ color: "#00F0FF" }}>LLM Summary</span>
              </div>

              {/* Benchmark Race Card */}
              <div
                style={{
                  width: 620,
                  backgroundColor: "rgba(10, 24, 46, 0.50)",
                  border: "2px solid rgba(0, 240, 255, 0.5)",
                  borderRadius: 24,
                  padding: 24,
                  boxShadow: "0 16px 40px rgba(0,0,0,0.8)",
                  backdropFilter: "blur(4px)",
                }}
              >
                <div style={{ fontSize: 20, fontWeight: 800, color: "rgba(255,255,255,0.7)", marginBottom: 16 }}>
                  PARSING SPEED PER 100-PAGE PAPER
                </div>

                {/* Contender 1: pypdfium2 */}
                <div style={{ marginBottom: 16 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", fontWeight: 900, fontSize: 22, marginBottom: 6 }}>
                    <span style={{ color: "#00F0FF" }}>pypdfium2 (C++ Engine)</span>
                    <span style={{ color: "#00F0FF" }}>42 ms (3.1x FASTER)</span>
                  </div>
                  <div style={{ height: 16, backgroundColor: "rgba(255,255,255,0.1)", borderRadius: 8, overflow: "hidden" }}>
                    <div style={{ height: "100%", width: "88%", backgroundColor: "#00F0FF", borderRadius: 8 }} />
                  </div>
                </div>

                {/* Contender 2: PyMuPDF */}
                <div style={{ marginBottom: 16 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", fontWeight: 800, fontSize: 20, marginBottom: 6 }}>
                    <span style={{ color: "rgba(255,255,255,0.8)" }}>PyMuPDF</span>
                    <span>118 ms</span>
                  </div>
                  <div style={{ height: 16, backgroundColor: "rgba(255,255,255,0.1)", borderRadius: 8, overflow: "hidden" }}>
                    <div style={{ height: "100%", width: "45%", backgroundColor: "#FF9E00", borderRadius: 8 }} />
                  </div>
                </div>

                {/* Contender 3: pypdf */}
                <div>
                  <div style={{ display: "flex", justifyContent: "space-between", fontWeight: 800, fontSize: 20, marginBottom: 6 }}>
                    <span style={{ color: "rgba(255,255,255,0.6)" }}>Standard pypdf</span>
                    <span>240 ms</span>
                  </div>
                  <div style={{ height: 16, backgroundColor: "rgba(255,255,255,0.1)", borderRadius: 8, overflow: "hidden" }}>
                    <div style={{ height: "100%", width: "22%", backgroundColor: "#EF4444", borderRadius: 8 }} />
                  </div>
                </div>
              </div>
            </div>
          </Sequence>

          {/* BEAT 2 (Frames 360 - 750, 12.0s - 25.0s): Steps & Interactive Code Terminal */}
          <Sequence from={360} durationInFrames={390}>
            <div
              style={{
                width: "100%",
                height: "100%",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                paddingTop: 130,
              }}
            >
              {/* Step Badges */}
              <div style={{ display: "flex", gap: 16, marginBottom: 24 }}>
                <div style={{ backgroundColor: "#00F0FF", color: "#000", fontWeight: 900, fontSize: 18, padding: "6px 18px", borderRadius: 16 }}>
                  STEP 1: INSTALL
                </div>
                <div style={{ backgroundColor: "rgba(0, 240, 255, 0.2)", border: "1.5px solid #00F0FF", color: "#00F0FF", fontWeight: 900, fontSize: 18, padding: "6px 18px", borderRadius: 16 }}>
                  STEP 2: STREAM EXTRACT
                </div>
              </div>

              {/* Terminal Card */}
              <div
                style={{
                  width: 640,
                  backgroundColor: "rgba(7, 14, 26, 0.55)",
                  backdropFilter: "blur(6px)",
                  border: "2px solid rgba(0, 240, 255, 0.6)",
                  borderRadius: 24,
                  boxShadow: "0 16px 44px rgba(0,0,0,0.9)",
                  overflow: "hidden",
                }}
              >
                {/* Terminal Header */}
                <div style={{ backgroundColor: "#0C182B", padding: "12px 20px", display: "flex", alignItems: "center", gap: 10, borderBottom: "1px solid rgba(0,240,255,0.3)" }}>
                  <div style={{ width: 14, height: 14, borderRadius: "50%", backgroundColor: "#EF4444" }} />
                  <div style={{ width: 14, height: 14, borderRadius: "50%", backgroundColor: "#F59E0B" }} />
                  <div style={{ width: 14, height: 14, borderRadius: "50%", backgroundColor: "#10B981" }} />
                  <span style={{ marginLeft: 14, fontSize: 16, fontWeight: 700, color: "rgba(255,255,255,0.7)", fontFamily: "monospace" }}>
                    bash — pypdfium2 streaming
                  </span>
                </div>

                {/* Terminal Body */}
                <div style={{ padding: 24, fontFamily: "monospace", fontSize: 24, lineHeight: 1.5, color: "#E2E8F0" }}>
                  <div style={{ color: "#38BDF8", marginBottom: 16 }}>$ pip install pypdfium2</div>
                  <div style={{ color: "#10B981", fontSize: 18, marginBottom: 20 }}>✓ Installed 0 dependencies (Native Google PDFium C++)</div>
                  
                  <div style={{ color: "#F472B6" }}>import pypdfium2 as pdfium</div>
                  <div>pdf = pdfium.PdfDocument("paper.pdf")</div>
                  <div style={{ color: "#FBBF24" }}>for page in pdf:</div>
                  <div style={{ paddingLeft: 24, color: "#4ADE80" }}>textpage = page.get_textpage()</div>
                  <div style={{ paddingLeft: 24, color: "#4ADE80" }}>clean_text = textpage.get_text_range()</div>
                </div>
              </div>

              {/* Native C++ Engine Badge */}
              <div
                style={{
                  marginTop: 24,
                  backgroundColor: "rgba(16, 185, 129, 0.15)",
                  border: "1.5px solid #10B981",
                  borderRadius: 16,
                  padding: "10px 24px",
                  fontSize: 20,
                  fontWeight: 800,
                  color: "#10B981",
                }}
              >
                ✓ Native Reading Order Preserved • Zero Interleaving
              </div>
            </div>
          </Sequence>

          {/* BEAT 3 (Frames 750 - 1170, 25.0s - 39.0s): Context Injection & Token Budget Savings */}
          <Sequence from={750} durationInFrames={420}>
            <div
              style={{
                width: "100%",
                height: "100%",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                paddingTop: 130,
              }}
            >
              <div
                style={{
                  backgroundColor: "rgba(255, 158, 0, 0.15)",
                  border: "1.5px solid #FF9E00",
                  borderRadius: 20,
                  padding: "6px 20px",
                  fontSize: 18,
                  fontWeight: 900,
                  color: "#FF9E00",
                  letterSpacing: "1.5px",
                  marginBottom: 20,
                }}
              >
                LLM CONTEXT OPTIMIZATION
              </div>

              <div
                style={{
                  fontSize: 58,
                  fontWeight: 900,
                  textAlign: "center",
                  lineHeight: 1.15,
                  maxWidth: 640,
                  marginBottom: 30,
                  color: "#FFFFFF",
                }}
              >
                Clean Reading Order <span style={{ color: "#10B981" }}>40% Tokens Saved</span>
              </div>

              {/* Token Flow Architecture */}
              <div
                style={{
                  width: 620,
                  backgroundColor: "rgba(10, 24, 46, 0.52)",
                  backdropFilter: "blur(6px)",
                  border: "2px solid rgba(16, 185, 129, 0.6)",
                  borderRadius: 24,
                  padding: 26,
                  boxShadow: "0 16px 40px rgba(0,0,0,0.85)",
                  display: "flex",
                  flexDirection: "column",
                  gap: 16,
                }}
              >
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <div style={{ fontSize: 20, fontWeight: 800, color: "rgba(255,255,255,0.7)" }}>
                    UNSTRUCTURED CONTEXT (Interleaved):
                  </div>
                  <div style={{ color: "#EF4444", fontWeight: 900, fontSize: 22 }}>4,800 TOKENS</div>
                </div>

                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <div style={{ fontSize: 20, fontWeight: 900, color: "#10B981" }}>
                    PYPDFIUM2 STREAM (Clean Blocks):
                  </div>
                  <div style={{ color: "#10B981", fontWeight: 900, fontSize: 24 }}>2,880 TOKENS (-40%)</div>
                </div>

                <div style={{ height: 20, backgroundColor: "rgba(255,255,255,0.1)", borderRadius: 10, overflow: "hidden", marginTop: 8 }}>
                  <div style={{ height: "100%", width: "60%", backgroundColor: "#10B981", borderRadius: 10 }} />
                </div>

                <div style={{ fontSize: 18, color: "rgba(255,255,255,0.8)", lineHeight: 1.4, marginTop: 10 }}>
                  Tables, section headers, and columns stay in discrete linear streams, preventing cross-column hallucinations.
                </div>
              </div>
            </div>
          </Sequence>

          {/* RECAP & CALLBACK (Frames 1170 - 1374, 39.0s - 45.8s): Newspaper vs Stream Callback */}
          <Sequence from={1170} durationInFrames={204}>
            <div
              style={{
                width: "100%",
                height: "100%",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                paddingTop: 140,
              }}
            >
              <div
                style={{
                  fontSize: 56,
                  fontWeight: 900,
                  textAlign: "center",
                  lineHeight: 1.2,
                  maxWidth: 620,
                  marginBottom: 28,
                }}
              >
                Stop Scrambling <span style={{ color: "#00F0FF" }}>Columns</span>
              </div>

              <div
                style={{
                  width: 620,
                  backgroundColor: "rgba(10, 24, 46, 0.52)",
                  backdropFilter: "blur(6px)",
                  border: "2px solid rgba(0, 240, 255, 0.6)",
                  borderRadius: 24,
                  padding: 28,
                  textAlign: "center",
                }}
              >
                <div style={{ fontSize: 24, fontWeight: 800, color: "#FF9E00", marginBottom: 12 }}>
                  ANALOGY RECAP
                </div>
                <div style={{ fontSize: 26, fontWeight: 700, color: "#FFFFFF", lineHeight: 1.4 }}>
                  Scrambled newspapers become clean digital streams with Google PDFium C++ engine in Python.
                </div>
              </div>
            </div>
          </Sequence>

          {/* END CARD (Frames 1374 - 1440, 45.8s - 48.0s, STRICTLY LAST 2.2s ONLY) */}
          <Sequence from={1374} durationInFrames={66}>
            <div
              style={{
                width: "100%",
                height: "100%",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                backgroundColor: "transparent",
                zIndex: 200,
                transform: `translateY(${Math.sin((frame - 1374) * 0.15) * 6}px)`,
              }}
            >
              <div
                style={{
                  width: 620,
                  padding: "40px 24px",
                  borderRadius: 24,
                  border: "2px solid rgba(0, 240, 255, 0.6)",
                  backgroundColor: "rgba(10, 24, 46, 0.55)",
                  boxShadow: "0 16px 44px rgba(0,0,0,0.85)",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                {/* Profile & Brand Circular Logo Mark */}
                <div
                  style={{
                    width: 140,
                    height: 140,
                    borderRadius: "50%",
                    border: "4px solid #00F0FF",
                    boxShadow: "0 0 50px rgba(0, 240, 255, 0.75)",
                    padding: 6,
                    marginBottom: 20,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    backgroundColor: "#0F172A",
                    transform: `scale(${1 + Math.sin(frame / 12) * 0.04})`,
                  }}
                >
                  <Img
                    src={staticFile("logo.png")}
                    style={{ width: "100%", height: "100%", borderRadius: "50%" }}
                  />
                </div>

                <div
                  style={{
                    fontSize: 42,
                    fontWeight: 900,
                    letterSpacing: "-0.5px",
                    color: "#FFFFFF",
                    marginBottom: 6,
                  }}
                >
                  FLASH<span style={{ color: "#00F0FF" }}>.AI</span>
                </div>

                <div
                  style={{
                    fontSize: 20,
                    fontWeight: 700,
                    color: "rgba(255,255,255,0.75)",
                    marginBottom: 32,
                  }}
                >
                  TOOLS & WORKFLOWS EXPLAINED
                </div>

                {/* Animated Follow Pill */}
                <FollowPill
                  brandText="@flash__ai__digital"
                  subtitle="Daily AI and dev updates, with sources"
                />
              </div>
            </div>
          </Sequence>
        </div>
      </div>

      {/* LAYER 3: Word-by-Word Synchronized Captions */}
      {renderSubtitles()}
    </AbsoluteFill>
  );
};
