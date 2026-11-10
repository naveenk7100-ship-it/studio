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

import { AttentionFlowGraph } from "../components/visuals/AttentionFlowGraph";
import { ProbabilityBarChart } from "../components/visuals/ProbabilityBarChart";
import { BackgroundRig } from "../components/visuals/BackgroundRig";
import { EndCard } from "../components/visuals/EndCard";
import wordsDiscovery from "../assets/v7_discovery_words.json";

export const V7_Discovery_HowChatGPTWorks: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  // Continuous Camera Movement (Zero Shake, Constant Motivated Push)
  const camZoom = 1.0 + (frame / 1320) * 0.16;
  const camPanX = Math.sin(frame * 0.05) * 16;
  const camPanY = Math.cos(frame * 0.04) * 14;

  // Real tokens from GPT-2 for "The future of artificial intelligence is"
  const realTokens = [
    { text: "The", id: 464 },
    { text: " future", id: 2003 },
    { text: " of", id: 286 },
    { text: " artificial", id: 11666 },
    { text: " intelligence", id: 4430 },
    { text: " is", id: 318 },
  ];

  // Active Word Highlight
  const currentSec = frame / 30;
  const activeWordObj = (wordsDiscovery as any[]).find(
    (w) => currentSec >= w.start && currentSec <= w.end
  );
  const activeWord = activeWordObj ? activeWordObj.word : "";

  // Captions (Strictly hides after 41.5s, before end card at 41.8s = frame 1254)
  const renderSubtitles = () => {
    if (frame >= 1245 || currentSec > 41.5) return null;
    const activeIdx = (wordsDiscovery as any[]).findIndex(
      (w) => currentSec >= w.start && currentSec <= w.end
    );
    if (activeIdx === -1) return null;

    const startIdx = Math.max(0, activeIdx - 1);
    const endIdx = Math.min(wordsDiscovery.length, activeIdx + 2);
    const slice = (wordsDiscovery as any[]).slice(startIdx, endIdx);

    return (
      <div
        style={{
          position: "absolute",
          bottom: 180,
          left: 55, // 7.64% margin from edges (guarantees >= 5% audit rule)
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
      {/* LAYER 1: Master Audio Track (48kHz, -14.4 LUFS, <= -1.5 dBTP) */}
      <Audio src={staticFile("audio/v7_discovery_master_48k.mp3")} />

      {/* LAYER 2: Camera Rig with Background Rig */}
      <div
        style={{
          position: "absolute",
          inset: -40,
          transform: `scale(${camZoom}) translate(${camPanX}px, ${camPanY}px)`,
          transformOrigin: "center center",
        }}
      >
        <BackgroundRig
          primaryColor="#00F0FF"
          secondaryColor="rgba(255, 176, 32, 0.3)"
          gridId="gridDiscovery"
        >
          {/* SCENE CONTENT (Frames 0 - 1254, 0.0s - 41.8s) */}
          <div style={{ position: "absolute", inset: 0 }}>
            {/* BEAT 1 (Frames 0 - 270, 0.0s - 9.0s): Prompt Input & Real Subword Token IDs */}
            <Sequence from={0} durationInFrames={270}>
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
                  GPT-2 (OPEN MODEL), EXAMPLE RUN
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
                  Next Word <span style={{ color: "#00F0FF" }}>Prediction</span>
                </div>

                {/* Real Input Prompt Card - Crisp Light Technical Sheet */}
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
                  <div>
                    <div
                      style={{
                        fontSize: 14,
                        color: "#0284C7",
                        fontFamily: "'JetBrains Mono', monospace",
                        fontWeight: 900,
                        marginBottom: 12,
                        letterSpacing: "1px",
                      }}
                    >
                      EXAMPLE PROMPT INPUT:
                    </div>
                    <div
                      style={{
                        fontSize: 30,
                        fontWeight: 900,
                        color: "#0F172A",
                        lineHeight: 1.3,
                        marginBottom: 24,
                        padding: "16px 20px",
                        backgroundColor: "#EFF6FF",
                        border: "2px solid #3B82F6",
                        borderRadius: 16,
                      }}
                    >
                      "The future of artificial intelligence is"
                    </div>

                    <div
                      style={{
                        fontSize: 14,
                        color: "#475569",
                        fontFamily: "'JetBrains Mono', monospace",
                        fontWeight: 800,
                        marginBottom: 14,
                      }}
                    >
                      SUBWORD TOKENS & EMBEDDING IDS (GPT-2 VOCAB: 50,257):
                    </div>

                    {/* Subword Tokens Breakdown */}
                    <div
                      style={{
                        display: "flex",
                        flexWrap: "wrap",
                        gap: 10,
                        justifyContent: "center",
                      }}
                    >
                      {realTokens.map((t, i) => (
                        <div
                          key={i}
                          style={{
                            backgroundColor: "#F1F5F9",
                            border: "2px solid #0284C7",
                            borderRadius: 14,
                            padding: "10px 18px",
                            display: "flex",
                            flexDirection: "column",
                            alignItems: "center",
                            gap: 4,
                            minWidth: 90,
                          }}
                        >
                          <span
                            style={{
                              fontSize: 12,
                              color: "#64748B",
                              fontFamily: "'JetBrains Mono', monospace",
                              fontWeight: 700,
                            }}
                          >
                            #{t.id}
                          </span>
                          <span
                            style={{
                              fontSize: 20,
                              fontWeight: 900,
                              color: "#0284C7",
                            }}
                          >
                            {t.text}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Architecture Specs Footer */}
                  <div
                    style={{
                      borderTop: "2px solid #E2E8F0",
                      paddingTop: 14,
                      display: "flex",
                      justifyContent: "space-between",
                      fontSize: 13,
                      color: "#475569",
                      fontFamily: "'JetBrains Mono', monospace",
                      fontWeight: 700,
                    }}
                  >
                    <span>GPT-2 Small • 124M Parameters</span>
                    <span>12 Layers • 12 Heads • 768 Dim</span>
                  </div>
                </div>
              </div>
            </Sequence>

            {/* BEAT 2 (Frames 270 - 660, 9.0s - 22.0s): AttentionFlowGraph (Real Layer 11 Head 0 Weights) */}
            <Sequence from={270} durationInFrames={390}>
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
                <AttentionFlowGraph
                  layer={11}
                  head={0}
                  targetTokenIdx={5}
                  flowSpeed={1.5}
                  width={610}
                  height={620}
                />
              </div>
            </Sequence>

            {/* BEAT 3 (Frames 660 - 1050, 22.0s - 35.0s): ProbabilityBarChart (Top-5 Sum ~26%) */}
            <Sequence from={660} durationInFrames={390}>
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
                <ProbabilityBarChart
                  promptText="The future of artificial intelligence is"
                  width={610}
                  height={620}
                  highlightTop={true}
                />
              </div>
            </Sequence>

            {/* BEAT 4 (Frames 1050 - 1254, 35.0s - 41.8s): Recap & Architecture Takeaway */}
            <Sequence from={1050} durationInFrames={204}>
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
                {/* Telemetry Header */}
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
                  ARCHITECTURE SUMMARY
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
                  {/* Takeaway Card 1 (<= 12 words) */}
                  <div
                    style={{
                      backgroundColor: "#EFF6FF",
                      border: "2px solid #3B82F6",
                      borderRadius: 18,
                      padding: 22,
                    }}
                  >
                    <div
                      style={{
                        fontSize: 13,
                        color: "#1D4ED8",
                        marginBottom: 8,
                        fontFamily: "'JetBrains Mono', monospace",
                        fontWeight: 900,
                      }}
                    >
                      CORE LESSON 1:
                    </div>
                    <div
                      style={{
                        fontSize: 26,
                        fontWeight: 900,
                        color: "#1E3A8A",
                        lineHeight: 1.35,
                      }}
                    >
                      Softmax top 5 probabilities 26 percent vachayi.
                    </div>
                  </div>

                  {/* Takeaway Card 2 (<= 12 words) */}
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
                        fontSize: 13,
                        color: "#B45309",
                        marginBottom: 8,
                        fontFamily: "'JetBrains Mono', monospace",
                        fontWeight: 900,
                      }}
                    >
                      CORE LESSON 2:
                    </div>
                    <div
                      style={{
                        fontSize: 26,
                        fontWeight: 900,
                        color: "#78350F",
                        lineHeight: 1.35,
                      }}
                    >
                      Model confident ga ledu, entropy ekkuvaga undi.
                    </div>
                  </div>

                  {/* Technical Disclosure Box */}
                  <div
                    style={{
                      backgroundColor: "#F1F5F9",
                      border: "1.5px solid #CBD5E1",
                      borderRadius: 16,
                      padding: "16px 20px",
                    }}
                  >
                    <div
                      style={{
                        fontSize: 13,
                        fontWeight: 800,
                        color: "#0284C7",
                        marginBottom: 6,
                        fontFamily: "'JetBrains Mono', monospace",
                      }}
                    >
                      MODEL DISCLOSURE:
                    </div>
                    <div
                      style={{
                        fontSize: 14,
                        color: "#334155",
                        lineHeight: 1.4,
                        fontWeight: 600,
                      }}
                    >
                      ChatGPT internals are not public. GPT-2 is an older open model used here for example demonstration.
                    </div>
                  </div>
                </div>
              </div>
            </Sequence>

            {/* BEAT 5 (Frames 1254 - 1320, 41.8s - 44.0s = LAST 2.2 SECONDS): Official Gated End Card */}
            <Sequence from={1254} durationInFrames={66}>
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
