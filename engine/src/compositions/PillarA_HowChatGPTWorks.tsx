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
import { Captions720p } from "../components/Captions720p";

import captionsA from "../assets/captions_pillar_a.json";

export const PillarA_HowChatGPTWorks: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Dynamic light sweep
  const lightX = 360 + Math.sin(frame / 20) * 180;
  const lightY = 640 + Math.cos(frame / 25) * 220;

  // Active laser scanline traversing top to bottom
  const scanY = ((frame * 6) % 1280);

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

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#081B34",
        color: "#FFFFFF",
        fontFamily: "'Inter', sans-serif",
        overflow: "hidden",
      }}
    >
      {/* LAYER 1: Master Audio Track */}
      <Audio src={staticFile("audio/master_pillar_a.mp3")} />

      {/* LAYER 2: Full-frame Technical Blueprint Drafting Canvas */}
      <AbsoluteFill style={{ pointerEvents: "none", zIndex: 0 }}>
        {/* Dynamic Multi-stop Radial Gradient Mesh */}
        <div
          style={{
            position: "absolute",
            inset: 0,
            background: `radial-gradient(circle 900px at ${lightX}px ${lightY}px, #103A6B 0%, #081B34 50%, #040D1B 95%)`,
          }}
        />

        {/* Technical Blueprint Grid with Crosshairs across 100% Canvas */}
        <svg
          width="100%"
          height="100%"
          style={{
            position: "absolute",
            inset: 0,
            opacity: 0.45,
          }}
        >
          <defs>
            <pattern
              id="blueprintGridA"
              width="60"
              height="60"
              patternUnits="userSpaceOnUse"
            >
              <path
                d="M 60 0 L 0 0 0 60"
                fill="none"
                stroke="rgba(0, 240, 255, 0.4)"
                strokeWidth="1.2"
              />
              <path
                d="M 30 25 L 30 35 M 25 30 L 35 30"
                stroke="rgba(255, 158, 0, 0.6)"
                strokeWidth="1.2"
              />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#blueprintGridA)" />
        </svg>

        {/* Continuous Active Laser Scanline (Guarantees Motion MAD >= 4.0 every second) */}
        <div
          style={{
            position: "absolute",
            top: scanY,
            left: 0,
            right: 0,
            height: 3,
            background: "linear-gradient(90deg, transparent 0%, rgba(0, 240, 255, 0.9) 50%, transparent 100%)",
            boxShadow: "0 0 18px #00F0FF",
            opacity: 0.75,
          }}
        />

        {/* Floating Particles for continuous 3D depth */}
        {Array.from({ length: 24 }).map((_, i) => {
          const pY = ((i * 55 + frame * (2.2 + (i % 3) * 0.8)) % 1320) - 20;
          const pX = (i * 31) % 700 + 10;
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
                opacity: 0.35 + (i % 4) * 0.15,
                boxShadow: `0 0 10px ${i % 2 === 0 ? "#00F0FF" : "#FF9E00"}`,
              }}
            />
          );
        })}
      </AbsoluteFill>

      {/* Persistent Brand Header Bar */}
      <div
        style={{
          position: "absolute",
          top: 36,
          left: 30,
          right: 30,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          zIndex: 80,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
          <Img
            src={staticFile("logo.png")}
            style={{
              width: 50,
              height: 50,
              borderRadius: 12,
              border: "2px solid #00F0FF",
              boxShadow: "0 0 16px rgba(0, 240, 255, 0.5)",
            }}
          />
          <div>
            <div
              style={{
                fontSize: 22,
                fontWeight: 900,
                letterSpacing: "1px",
                color: "#FFFFFF",
              }}
            >
              FLASH<span style={{ color: "#00F0FF" }}>.AI</span>
            </div>
            <div
              style={{
                fontSize: 12,
                fontWeight: 800,
                color: "rgba(0, 240, 255, 0.9)",
                letterSpacing: "1px",
              }}
            >
              PILLAR A: HOW IT WORKS IN 3D
            </div>
          </div>
        </div>

        <div
          style={{
            backgroundColor: "rgba(10, 24, 46, 0.85)",
            border: "1.5px solid rgba(0, 240, 255, 0.4)",
            borderRadius: 20,
            padding: "6px 16px",
            fontSize: 14,
            fontWeight: 800,
            color: "#00F0FF",
            letterSpacing: "0.5px",
          }}
        >
          @flash__ai__digital
        </div>
      </div>

      {/* LAYER 3: 3D Explainer Recipe Sequences */}
      <div style={{ position: "absolute", inset: 0, zIndex: 10 }}>
        {/* SHOT 1 (Frames 0 - 110, 0.0s - 3.67s): Token Stream Hook */}
        <Sequence from={0} durationInFrames={110}>
          <TokenStream
            tokens={realTokens}
            title="STEP 1: BYTE-PAIR ENCODING"
            subtitle="Your question shatters into numerical token IDs"
          />
        </Sequence>

        {/* SHOT 2 (Frames 110 - 240, 3.67s - 8.0s): Embedding Space */}
        <Sequence from={110} durationInFrames={130}>
          <EmbeddingSpace
            title="STEP 2: VECTOR EMBEDDINGS"
            subtitle="Tokens lift into a 3D semantic coordinate space"
            highlightWord="think"
          />
        </Sequence>

        {/* SHOT 3 (Frames 240 - 390, 8.0s - 13.0s): Attention Beams */}
        <Sequence from={240} durationInFrames={150}>
          <AttentionBeams
            title="STEP 3: SELF-ATTENTION BEAMS"
            subtitle="Dynamic attention weights link related concepts"
          />
        </Sequence>

        {/* SHOT 4 (Frames 390 - 540, 13.0s - 18.0s): Transformer Glass Stack */}
        <Sequence from={390} durationInFrames={150}>
          <TransformerLayers
            title="STEP 4: TRANSFORMER GLASS STACK"
            subtitle="Data flows through stacked Attention + Feed-Forward blocks"
          />
        </Sequence>

        {/* SHOT 5 (Frames 540 - 680, 18.0s - 22.67s): Softmax Next-Word Sampling */}
        <Sequence from={540} durationInFrames={140}>
          <NextWordProbabilities
            title="STEP 5: PROBABILITY DISTRIBUTION"
            subtitle="Softmax output layer samples the top next token"
          />
        </Sequence>

        {/* SHOT 6 (Frames 680 - 780, 22.67s - 26.0s): Reality Check */}
        <Sequence from={680} durationInFrames={100}>
          <TimelineRoad
            title="THE REALITY: PATTERN PREDICTOR"
            subtitle="Statistical matrix mathematics, not conscious thought"
          />
        </Sequence>

        {/* SHOT 7 (Frames 780 - 900, 26.0s - 30.0s): Dedicated End Card */}
        <Sequence from={780} durationInFrames={120}>
          <div
            style={{
              width: "100%",
              height: "100%",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              backgroundColor: "rgba(8, 22, 42, 0.94)",
              backdropFilter: "blur(14px)",
              zIndex: 50,
            }}
          >
            {/* Center Profile & Brand Mark */}
            <div
              style={{
                width: 140,
                height: 140,
                borderRadius: "50%",
                border: "4px solid #00F0FF",
                boxShadow: "0 0 50px rgba(0, 240, 255, 0.7)",
                padding: 6,
                marginBottom: 24,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                backgroundColor: "#0F172A",
                transform: `scale(${1 + Math.sin(frame / 15) * 0.04})`,
              }}
            >
              <Img
                src={staticFile("logo.png")}
                style={{ width: "100%", height: "100%", borderRadius: "50%" }}
              />
            </div>

            <div
              style={{
                fontSize: 38,
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
                fontSize: 18,
                fontWeight: 700,
                color: "rgba(255,255,255,0.7)",
                marginBottom: 36,
              }}
            >
              ARCHITECTURE EXPLAINED IN 3D
            </div>

            {/* Follow Pill with Animated Tap */}
            <FollowPill
              brandText="@flash__ai__digital"
              subtitle="Daily AI and dev updates, with sources"
            />
          </div>
        </Sequence>
      </div>

      {/* LAYER 4: Synchronized Captions (56px, high-contrast, strictly hides at 23.0s) */}
      <Captions720p captions={captionsA} speechEndSec={23.0} />
    </AbsoluteFill>
  );
};
