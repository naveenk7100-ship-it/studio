import React from "react";
import {
  AbsoluteFill,
  Audio,
  interpolate,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

import { Document3DView } from "../components/visuals/Document3DView";
import { BoundingBoxOverlay } from "../components/visuals/BoundingBoxOverlay";
import { BackgroundRig } from "../components/visuals/BackgroundRig";
import { EndCard } from "../components/visuals/EndCard";
import wordsTools from "../assets/v7_tools_words.json";

export const V7_Tools_PyPdfium2: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  // Continuous Camera Movement (Zero Shake, Constant Motivated Push)
  const camZoom = 1.0 + (frame / 1260) * 0.16;
  const camPanX = Math.sin(frame * 0.05) * 16;
  const camPanY = Math.cos(frame * 0.04) * 14;

  // Active Word Highlight
  const currentSec = frame / 30;
  const activeWordObj = (wordsTools as any[]).find(
    (w) => currentSec >= w.start && currentSec <= w.end
  );
  const activeWord = activeWordObj ? activeWordObj.word : "";

  // Captions (Strictly hides after 39.5s, before end card at 39.8s = frame 1194)
  const renderSubtitles = () => {
    if (frame >= 1185 || currentSec > 39.5) return null;
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
          bottom: 180,
          left: 55, // 7.64% margin from screen edges (guarantees >= 5% audit rule)
          right: 55,
          textAlign: "center",
          zIndex: 100,
          display: "flex",
          justifyContent: "center",
        }}
      >
        <div
          style={{
            backgroundColor: "rgba(10, 18, 34, 0.94)",
            border: "2px solid rgba(0, 240, 255, 0.7)",
            borderRadius: 22,
            padding: "10px 20px",
            boxShadow: "0 12px 36px rgba(0, 0, 0, 0.9)",
            backdropFilter: "blur(14px)",
            display: "flex",
            gap: 10,
            alignItems: "center",
            maxWidth: 590,
            flexWrap: "wrap",
            justifyContent: "center",
          }}
        >
          {slice.map((item, idx) => {
            const isCurrent = item.word === activeWord;
            return (
              <span
                key={idx}
                style={{
                  fontSize: 50,
                  fontWeight: 900,
                  color: isCurrent ? "#00F0FF" : "#FFFFFF",
                  textShadow: isCurrent
                    ? "0 0 25px rgba(0, 240, 255, 0.9), 0 2px 10px rgba(0,0,0,0.9)"
                    : "0 2px 8px rgba(0,0,0,0.8)",
                  background: isCurrent ? "rgba(0, 240, 255, 0.18)" : "transparent",
                  padding: "2px 8px",
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
      {/* LAYER 1: Master Audio Track (48kHz, -14.5 LUFS, <= -1.5 dBTP) */}
      <Audio src={staticFile("audio/v7_tools_master_48k.mp3")} />

      {/* LAYER 2: Camera Rig with Background Rig */}
      <div
        style={{
          position: "absolute",
          inset: -40,
          transform: `scale(${camZoom}) translate(${camPanX}px, ${camPanY}px)`,
          transformOrigin: "center center",
        }}
      >
        <BackgroundRig primaryColor="#00F0FF" secondaryColor="rgba(0, 240, 255, 0.25)" gridId="gridTools">
          {/* SCENE CONTENT (Frames 0 - 1194, 0.0s - 39.8s) */}
          <div style={{ position: "absolute", inset: 0 }}>
            {/* BEAT 1 (Frames 0 - 300, 0.0s - 10.0s): Hero 3D Document & Real Bounding Boxes */}
            <Sequence from={0} durationInFrames={300}>
              <div
                style={{
                  width: "100%",
                  height: "100%",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  paddingTop: 100,
                }}
              >
                {/* Category Pill */}
                <div
                  style={{
                    backgroundColor: "rgba(0, 240, 255, 0.18)",
                    border: "2px solid #00F0FF",
                    borderRadius: 20,
                    padding: "6px 20px",
                    fontSize: 16,
                    fontWeight: 900,
                    color: "#00F0FF",
                    letterSpacing: "1.2px",
                    marginBottom: 12,
                    boxShadow: "0 0 15px rgba(0, 240, 255, 0.4)",
                  }}
                >
                  PDF TEXT EXTRACTION
                </div>

                {/* Main Headline */}
                <div
                  style={{
                    fontSize: 52,
                    fontWeight: 900,
                    textAlign: "center",
                    lineHeight: 1.15,
                    maxWidth: 630,
                    marginBottom: 16,
                    color: "#FFFFFF",
                    textShadow: "0 2px 12px rgba(0,0,0,0.8)",
                  }}
                >
                  pypdfium2 <span style={{ color: "#00F0FF" }}>Speed Benchmark</span>
                </div>

                {/* Hero Real Asset: Document3DView with real arXiv Page 1 + real bounding boxes */}
                <div style={{ width: 540, height: 650 }}>
                  <Document3DView
                    title="Attention Is All You Need"
                    paperId="arXiv:1706.03762"
                    totalPages={15}
                  >
                    <BoundingBoxOverlay
                      containerWidth={500}
                      containerHeight={640}
                      scanDurationFrames={90}
                      showCoordinatesTag={true}
                      showBlockCounter={true}
                    />
                  </Document3DView>
                </div>
              </div>
            </Sequence>

            {/* BEAT 2 (Frames 300 - 690, 10.0s - 23.0s): 10-Run Benchmark Race (Empirical Evidence) */}
            <Sequence from={300} durationInFrames={390}>
              <div
                style={{
                  width: "100%",
                  height: "100%",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  paddingTop: 100,
                }}
              >
                {/* Step Badges */}
                <div style={{ display: "flex", gap: 14, marginBottom: 14 }}>
                  <div
                    style={{
                      backgroundColor: "#00F0FF",
                      color: "#050914",
                      fontWeight: 900,
                      fontSize: 16,
                      padding: "6px 18px",
                      borderRadius: 14,
                      boxShadow: "0 0 15px rgba(0, 240, 255, 0.5)",
                    }}
                  >
                    10 RUNS BENCHMARK
                  </div>
                  <div
                    style={{
                      backgroundColor: "rgba(0, 240, 255, 0.18)",
                      border: "1.5px solid #00F0FF",
                      color: "#00F0FF",
                      fontWeight: 800,
                      fontSize: 15,
                      padding: "6px 18px",
                      borderRadius: 14,
                    }}
                  >
                    15 PAGES FULL-TEXT
                  </div>
                </div>

                {/* Main Benchmark Race Card - Crisp Light Technical Sheet */}
                <div
                  style={{
                    width: 610,
                    height: 620,
                    backgroundColor: "#F8FAFC",
                    border: "3px solid #00F0FF",
                    borderRadius: 24,
                    padding: "20px 24px",
                    boxShadow: "0 25px 60px rgba(0,0,0,0.85)",
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "space-between",
                    boxSizing: "border-box",
                  }}
                >
                  <div>
                    <div
                      style={{
                        fontSize: 15,
                        fontWeight: 900,
                        color: "#0284C7",
                        fontFamily: "'JetBrains Mono', monospace",
                        marginBottom: 16,
                        letterSpacing: "1px",
                      }}
                    >
                      MEASURED EXTRACTION TIME (10 RUNS)
                    </div>

                    {/* Contender 1: pypdfium2 */}
                    <div style={{ marginBottom: 20 }}>
                      <div
                        style={{
                          display: "flex",
                          justifyContent: "space-between",
                          fontWeight: 900,
                          fontSize: 22,
                          marginBottom: 8,
                        }}
                      >
                        <span style={{ color: "#0F172A" }}>pypdfium2 5.6.0</span>
                        <span style={{ color: "#0284C7", fontWeight: 900 }}>239 ms (1.0x)</span>
                      </div>
                      <div
                        style={{
                          height: 28,
                          backgroundColor: "#E2E8F0",
                          borderRadius: 8,
                          overflow: "hidden",
                          border: "1.5px solid #0284C7",
                          position: "relative",
                        }}
                      >
                        <div
                          style={{
                            width: "100%",
                            height: "100%",
                            background: "linear-gradient(90deg, #0284C7, #00F0FF)",
                            boxShadow: "0 0 15px rgba(0, 240, 255, 0.7)",
                          }}
                        />
                      </div>
                      <div
                        style={{
                          fontSize: 13,
                          color: "#475569",
                          fontFamily: "'JetBrains Mono', monospace",
                          marginTop: 4,
                          fontWeight: 700,
                        }}
                      >
                        Min: 207 ms • Max: 344 ms • Mean: 250 ms
                      </div>
                    </div>

                    {/* Contender 2: pypdf */}
                    <div style={{ marginBottom: 20 }}>
                      <div
                        style={{
                          display: "flex",
                          justifyContent: "space-between",
                          fontWeight: 900,
                          fontSize: 20,
                          marginBottom: 8,
                        }}
                      >
                        <span style={{ color: "#0F172A" }}>pypdf 6.9.2</span>
                        <span style={{ color: "#D97706", fontWeight: 900 }}>1,400 ms (5.85x slower)</span>
                      </div>
                      <div
                        style={{
                          height: 24,
                          backgroundColor: "#E2E8F0",
                          borderRadius: 8,
                          overflow: "hidden",
                          border: "1.5px solid #D97706",
                          position: "relative",
                        }}
                      >
                        <div
                          style={{
                            width: "35%",
                            height: "100%",
                            backgroundColor: "#F59E0B",
                          }}
                        />
                      </div>
                      <div
                        style={{
                          fontSize: 13,
                          color: "#475569",
                          fontFamily: "'JetBrains Mono', monospace",
                          marginTop: 4,
                          fontWeight: 700,
                        }}
                      >
                        Min: 1317 ms • Max: 1646 ms • Mean: 1423 ms
                      </div>
                    </div>

                    {/* Contender 3: pdfminer.six */}
                    <div style={{ marginBottom: 14 }}>
                      <div
                        style={{
                          display: "flex",
                          justifyContent: "space-between",
                          fontWeight: 800,
                          fontSize: 18,
                          marginBottom: 6,
                          color: "#475569",
                        }}
                      >
                        <span>pdfminer.six 20251230</span>
                        <span style={{ fontWeight: 800 }}>4,065 ms (17.0x slower)</span>
                      </div>
                      <div
                        style={{
                          height: 18,
                          backgroundColor: "#E2E8F0",
                          borderRadius: 6,
                          overflow: "hidden",
                        }}
                      >
                        <div
                          style={{
                            width: "12%",
                            height: "100%",
                            backgroundColor: "#64748B",
                          }}
                        />
                      </div>
                      <div
                        style={{
                          fontSize: 12,
                          color: "#64748B",
                          fontFamily: "'JetBrains Mono', monospace",
                          marginTop: 4,
                          fontWeight: 700,
                        }}
                      >
                        Min: 3970 ms • Max: 4206 ms • Mean: 4078 ms
                      </div>
                    </div>
                  </div>

                  {/* Benchmark Environment Footer */}
                  <div
                    style={{
                      borderTop: "2px solid #E2E8F0",
                      paddingTop: 14,
                      display: "flex",
                      flexDirection: "column",
                      gap: 6,
                    }}
                  >
                    <div
                      style={{
                        fontSize: 13,
                        color: "#0284C7",
                        fontWeight: 800,
                        fontFamily: "'JetBrains Mono', monospace",
                      }}
                    >
                      ENVIRONMENT: Windows 10 x64 • AMD64 • Python 3.11.0
                    </div>
                    <div
                      style={{
                        fontSize: 12,
                        color: "#475569",
                        fontFamily: "'JetBrains Mono', monospace",
                        fontWeight: 600,
                      }}
                    >
                      Method: 1 warm-up run + 10 measured runs • Full text of all 15 pages
                    </div>
                  </div>
                </div>
              </div>
            </Sequence>

            {/* BEAT 3 (Frames 690 - 1020, 23.0s - 34.0s): Single-Column Truth & Token Count */}
            <Sequence from={690} durationInFrames={330}>
              <div
                style={{
                  width: "100%",
                  height: "100%",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  paddingTop: 100,
                }}
              >
                {/* Header Tag */}
                <div
                  style={{
                    backgroundColor: "rgba(255, 176, 32, 0.2)",
                    border: "2px solid #FFB020",
                    borderRadius: 16,
                    padding: "6px 20px",
                    fontSize: 16,
                    fontWeight: 900,
                    color: "#FFB020",
                    marginBottom: 16,
                  }}
                >
                  EMPIRICAL LIMITATIONS & TOKENS
                </div>

                {/* Content Container - Crisp Light Technical Sheet */}
                <div
                  style={{
                    width: 610,
                    height: 590,
                    backgroundColor: "#F8FAFC",
                    border: "3px solid #F59E0B",
                    borderRadius: 24,
                    padding: "20px",
                    boxShadow: "0 25px 60px rgba(0,0,0,0.85)",
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "space-between",
                    boxSizing: "border-box",
                  }}
                >
                  {/* Card 1: Single-Column Truth Callout */}
                  <div
                    style={{
                      backgroundColor: "#FEF3C7",
                      border: "2px solid #F59E0B",
                      borderRadius: 18,
                      padding: 22,
                    }}
                  >
                    <div
                      style={{
                        fontSize: 14,
                        fontWeight: 900,
                        color: "#92400E",
                        letterSpacing: "1px",
                        marginBottom: 10,
                        fontFamily: "'JetBrains Mono', monospace",
                      }}
                    >
                      SINGLE-COLUMN PAPER WARNING:
                    </div>
                    <div
                      style={{
                        fontSize: 26,
                        fontWeight: 900,
                        color: "#78350F",
                        lineHeight: 1.35,
                      }}
                    >
                      Idi single-column paper. Two-column lo order maarochu, nenu test cheyyaledu.
                    </div>
                  </div>

                  {/* Card 2: Token Count with tiktoken (cl100k_base) */}
                  <div
                    style={{
                      backgroundColor: "#ECFDF5",
                      border: "2px solid #10B981",
                      borderRadius: 18,
                      padding: 22,
                    }}
                  >
                    <div
                      style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                        marginBottom: 10,
                      }}
                    >
                      <span
                        style={{
                          fontSize: 14,
                          fontWeight: 900,
                          color: "#065F46",
                          fontFamily: "'JetBrains Mono', monospace",
                        }}
                      >
                        TOKENIZER: tiktoken 0.14.0
                      </span>
                      <span
                        style={{
                          backgroundColor: "#10B981",
                          color: "#FFFFFF",
                          fontSize: 12,
                          fontWeight: 900,
                          padding: "4px 10px",
                          borderRadius: 8,
                        }}
                      >
                        cl100k_base
                      </span>
                    </div>

                    <div
                      style={{
                        fontSize: 48,
                        fontWeight: 900,
                        color: "#059669",
                        marginBottom: 6,
                      }}
                    >
                      10,187 TOKENS
                    </div>
                    <div
                      style={{
                        fontSize: 18,
                        fontWeight: 700,
                        color: "#065F46",
                      }}
                    >
                      tiktoken tho 10187 tokens count chesam.
                    </div>
                  </div>

                  {/* Telemetry Footer */}
                  <div
                    style={{
                      borderTop: "2px solid #E2E8F0",
                      paddingTop: 12,
                      display: "flex",
                      justifyContent: "space-between",
                      fontSize: 13,
                      color: "#64748B",
                      fontFamily: "'JetBrains Mono', monospace",
                      fontWeight: 700,
                    }}
                  >
                    <span>Paper: arXiv:1706.03762</span>
                    <span>Chars: 40,407 • Words: 6,103</span>
                  </div>
                </div>
              </div>
            </Sequence>

            {/* BEAT 4 (Frames 1020 - 1194, 34.0s - 39.8s): Recap & Takeaways */}
            <Sequence from={1020} durationInFrames={174}>
              <div
                style={{
                  width: "100%",
                  height: "100%",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  paddingTop: 100,
                }}
              >
                <div
                  style={{
                    backgroundColor: "rgba(0, 240, 255, 0.18)",
                    border: "2px solid #00F0FF",
                    borderRadius: 16,
                    padding: "6px 20px",
                    fontSize: 16,
                    fontWeight: 900,
                    color: "#00F0FF",
                    marginBottom: 16,
                  }}
                >
                  EMPIRICAL SUMMARY
                </div>

                <div
                  style={{
                    width: 610,
                    height: 590,
                    backgroundColor: "#F8FAFC",
                    border: "3px solid #00F0FF",
                    borderRadius: 24,
                    padding: "20px",
                    boxShadow: "0 25px 60px rgba(0,0,0,0.85)",
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "space-between",
                    boxSizing: "border-box",
                  }}
                >
                  {/* Takeaway 1 */}
                  <div
                    style={{
                      backgroundColor: "#EFF6FF",
                      border: "2px solid #3B82F6",
                      borderRadius: 18,
                      padding: 22,
                    }}
                  >
                    <div style={{ fontSize: 13, color: "#1D4ED8", marginBottom: 8, fontFamily: "'JetBrains Mono', monospace", fontWeight: 800 }}>
                      RESULT 1:
                    </div>
                    <div style={{ fontSize: 26, fontWeight: 900, color: "#1E3A8A", lineHeight: 1.35 }}>
                      pypdfium2 median 239 milliseconds lo text extract chesindi.
                    </div>
                  </div>

                  {/* Takeaway 2 */}
                  <div
                    style={{
                      backgroundColor: "#FEF3C7",
                      border: "2px solid #F59E0B",
                      borderRadius: 18,
                      padding: 22,
                    }}
                  >
                    <div style={{ fontSize: 13, color: "#B45309", marginBottom: 8, fontFamily: "'JetBrains Mono', monospace", fontWeight: 800 }}>
                      RESULT 2:
                    </div>
                    <div style={{ fontSize: 26, fontWeight: 900, color: "#78350F", lineHeight: 1.35 }}>
                      pypdf 1400 ms teeskundi, 5.85 times slow.
                    </div>
                  </div>

                  {/* Speedup Box */}
                  <div
                    style={{
                      backgroundColor: "#0284C7",
                      borderRadius: 16,
                      padding: "16px 20px",
                      textAlign: "center",
                      boxShadow: "0 4px 15px rgba(2, 132, 199, 0.4)",
                    }}
                  >
                    <div style={{ fontSize: 32, fontWeight: 900, color: "#FFFFFF" }}>
                      5.85x SPEEDUP
                    </div>
                    <div style={{ fontSize: 14, color: "rgba(255,255,255,0.9)", fontFamily: "'JetBrains Mono', monospace", fontWeight: 700 }}>
                      C++ PDFium Engine via Python ctypes
                    </div>
                  </div>
                </div>
              </div>
            </Sequence>

            {/* BEAT 5 (Frames 1194 - 1260, 39.8s - 42.0s = LAST 2.2 SECONDS): Official Gated End Card */}
            <Sequence from={1194} durationInFrames={66}>
              <EndCard
                brandHandle="@flash__ai__digital"
                subtitle="Daily AI and dev updates, with sources"
              />
            </Sequence>
          </div>
        </BackgroundRig>
      </div>

      {/* LAYER 3: Word-by-Word Synchronized Captions */}
      {renderSubtitles()}
    </AbsoluteFill>
  );
};
