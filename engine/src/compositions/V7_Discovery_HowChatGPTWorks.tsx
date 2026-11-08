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

import { TokenStream } from "../recipes/TokenStream";
import { EmbeddingSpace } from "../recipes/EmbeddingSpace";
import { AttentionBeams } from "../recipes/AttentionBeams";
import { TransformerLayers } from "../recipes/TransformerLayers";
import { NextWordProbabilities } from "../recipes/NextWordProbabilities";
import { TimelineRoad } from "../recipes/TimelineRoad";
import { FollowPill } from "../components/FollowPill";
import wordsDiscovery from "../assets/v7_discovery_words.json";

export const V7_Discovery_HowChatGPTWorks: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  // Dynamic light sweep
  const lightX = 360 + Math.sin(frame / 24) * 200;
  const lightY = 640 + Math.cos(frame / 28) * 250;

  // Active laser scanline traversing top to bottom
  const scanY = ((frame * 7) % 1280);

  // Continuous Camera Movement (Zero Shake, Constant Motivated Push)
  const camZoom = 1.0 + (frame / 1500) * 0.12;
  const camPanX = Math.sin(frame * 0.03) * 12;
  const camPanY = Math.cos(frame * 0.025) * 8;

  // Real tokens from tiktoken cl100k_base for "How does ChatGPT actually think?"
  const realTokens = [
    { text: "How", id: 4438 },
    { text: "does", id: 1587 },
    { text: "Chat", id: 13149 },
    { text: "G", id: 38 },
    { text: "PT", id: 2898 },
    { text: "actually", id: 3604 },
    { text: "think", id: 1781 },
    { text: "?", id: 30 },
  ];

  // Active Word Highlight
  const currentSec = frame / 30;
  const activeWordObj = (wordsDiscovery as any[]).find(
    (w) => currentSec >= w.start && currentSec <= w.end
  );
  const activeWord = activeWordObj ? activeWordObj.word : "";

  // Captions (Strictly hides after 47.4s, before end card at 47.5s)
  const renderSubtitles = () => {
    if (frame >= 1425 || currentSec > 47.4) return null;
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
      <Audio src={staticFile("audio/v7_discovery_master_48k.mp3")} />

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
              id="blueprintGridDisc"
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
          <rect width="100%" height="100%" fill="url(#blueprintGridDisc)" />
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

        {/* SCENE CONTENT (Frames 0 - 1425, 0.0s - 47.5s) */}
        <div style={{ position: "absolute", inset: 0, zIndex: 10 }}>
          {/* BEAT 1 (Frames 0 - 450, 0.0s - 15.0s): Token Stream & 3D Embedding Space */}
          <Sequence from={0} durationInFrames={225}>
            <TokenStream
              tokens={realTokens}
              title="STEP 1: BYTE-PAIR ENCODING"
              subtitle="Your question shatters into numerical token IDs"
            />
          </Sequence>

          <Sequence from={225} durationInFrames={225}>
            <EmbeddingSpace
              title="STEP 2: VECTOR EMBEDDINGS"
              subtitle="Tokens lift into a 3D semantic coordinate space"
              highlightWord="think"
            />
          </Sequence>

          {/* BEAT 2 (Frames 450 - 900, 15.0s - 30.0s): Attention Beams & Glass Stack */}
          <Sequence from={450} durationInFrames={225}>
            <AttentionBeams
              title="STEP 3: SELF-ATTENTION BEAMS"
              subtitle="Dynamic attention weights link related concepts"
            />
          </Sequence>

          <Sequence from={675} durationInFrames={225}>
            <TransformerLayers
              title="STEP 4: TRANSFORMER GLASS STACK"
              subtitle="Data flows through stacked Attention + Feed-Forward blocks"
            />
          </Sequence>

          {/* BEAT 3 (Frames 900 - 1260, 30.0s - 42.0s): Softmax Probability & Autoregressive Loop */}
          <Sequence from={900} durationInFrames={210}>
            <NextWordProbabilities
              title="STEP 5: PROBABILITY DISTRIBUTION"
              subtitle="Softmax output layer samples the top next token"
            />
          </Sequence>

          <Sequence from={1110} durationInFrames={150}>
            <TimelineRoad
              title="STEP 6: AUTOREGRESSIVE LOOP"
              subtitle="Picks one token, appends it to context, and repeats"
            />
          </Sequence>

          {/* RECAP & CALLBACK (Frames 1260 - 1425, 42.0s - 47.5s): Lego Blocks with GPS Analogy */}
          <Sequence from={1260} durationInFrames={165}>
            <div
              style={{
                width: "100%",
                height: "100%",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                paddingTop: 150,
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
                Mathematical <span style={{ color: "#00F0FF" }}>Pattern Flow</span>
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
                  Words convert to Lego blocks with GPS coordinates, predicting the next high-probability token.
                </div>
              </div>
            </div>
          </Sequence>

          {/* END CARD (Frames 1425 - 1500, 47.5s - 50.0s, STRICTLY LAST 2.5s ONLY) */}
          <Sequence from={1425} durationInFrames={75}>
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
                transform: `translateY(${Math.sin((frame - 1425) * 0.15) * 6}px)`,
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
                  AI ARCHITECTURES IN 3D
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
