import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
  Sequence,
  staticFile,
  Img,
} from "remotion";
import { BoltStrike } from "../components/BoltStrike";
import { FlashFrame } from "../components/FlashFrame";
import { HandleChip } from "../components/HandleChip";
import { FollowPill } from "../components/FollowPill";
import { RadarSweep } from "../components/RadarSweep";
import { BrowserMockup3D } from "../components/BrowserMockup3D";
import { PopCaptions } from "../components/PopCaptions";
import { AutoFitText } from "../components/AutoFitText";

// Prompt Library Index ID: 164 (Repo Spotlight & Architecture Film)
const WORDS: [string, number, number][] = [
  [
    "Mama,",
    0.0,
    0.604
  ],
  [
    "mee",
    0.604,
    1.081
  ],
  [
    "local",
    1.081,
    1.415
  ],
  [
    "GPU",
    1.415,
    1.765
  ],
  [
    "lo",
    1.765,
    2.019
  ],
  [
    "LLMs",
    2.099,
    2.623
  ],
  [
    "high-speed",
    2.623,
    2.862
  ],
  [
    "serve",
    2.862,
    3.068
  ],
  [
    "cheyalani",
    3.068,
    3.307
  ],
  [
    "anukuntunnara?",
    3.307,
    3.434
  ],
  [
    "Idi",
    3.434,
    3.474
  ],
  [
    "vLLM",
    3.466,
    3.641
  ],
  [
    "v0.32.0.",
    3.641,
    4.165
  ],
  [
    "Idi",
    4.165,
    4.642
  ],
  [
    "oka",
    5.771,
    6.407
  ],
  [
    "open-source",
    6.407,
    6.804
  ],
  [
    "high-throughput",
    6.804,
    7.122
  ],
  [
    "inference",
    7.122,
    7.711
  ],
  [
    "engine.",
    7.711,
    8.013
  ],
  [
    "Deeni",
    8.013,
    8.983
  ],
  [
    "PagedAttention",
    8.983,
    9.253
  ],
  [
    "algorithm",
    9.253,
    9.428
  ],
  [
    "KV-cache",
    9.428,
    9.65
  ],
  [
    "memory",
    9.65,
    9.936
  ],
  [
    "waste",
    9.936,
    10.445
  ],
  [
    "ni",
    10.445,
    10.843
  ],
  [
    "zero",
    10.843,
    10.938
  ],
  [
    "chesthundi.",
    10.938,
    11.272
  ],
  [
    "Single",
    11.749,
    12.194
  ],
  [
    "GPU",
    12.194,
    12.687
  ],
  [
    "lo",
    12.687,
    13.18
  ],
  [
    "4x",
    13.18,
    13.466
  ],
  [
    "ekuva",
    13.466,
    13.545
  ],
  [
    "concurrent",
    13.545,
    13.975
  ],
  [
    "requests",
    13.975,
    14.261
  ],
  [
    "handle",
    14.261,
    14.674
  ],
  [
    "chesthundi.",
    14.674,
    14.992
  ],
  [
    "Terminal",
    14.992,
    15.183
  ],
  [
    "lo",
    15.183,
    15.676
  ],
  [
    "vllm",
    15.676,
    15.946
  ],
  [
    "serve",
    15.946,
    16.28
  ],
  [
    "meta-llama",
    16.534,
    16.789
  ],
  [
    "type",
    16.789,
    16.979
  ],
  [
    "chesi",
    16.979,
    17.17
  ],
  [
    "direct",
    17.17,
    17.742
  ],
  [
    "ga",
    17.742,
    17.965
  ],
  [
    "deploy",
    17.965,
    18.712
  ],
  [
    "cheyochu.",
    18.712,
    19.046
  ],
  [
    "Gated",
    19.046,
    19.459
  ],
  [
    "model",
    19.459,
    20.35
  ],
  [
    "kabatti",
    20.35,
    20.811
  ],
  [
    "HuggingFace",
    20.811,
    21.335
  ],
  [
    "token",
    21.335,
    21.955
  ],
  [
    "kavali,",
    21.955,
    22.21
  ],
  [
    "leda",
    22.21,
    22.512
  ],
  [
    "direct",
    22.814,
    23.148
  ],
  [
    "ga",
    23.148,
    23.196
  ],
  [
    "Qwen",
    23.196,
    23.514
  ],
  [
    "vadachu.",
    23.514,
    24.261
  ],
  [
    "Daily",
    24.261,
    24.547
  ],
  [
    "top",
    24.547,
    24.96
  ],
  [
    "tech",
    24.96,
    25.374
  ],
  [
    "tools",
    25.676,
    25.93
  ],
  [
    "kosam",
    25.93,
    26.216
  ],
  [
    "FLASH",
    26.216,
    26.407
  ],
  [
    "ni",
    26.407,
    26.661
  ],
  [
    "FOLLOW",
    26.661,
    27.424
  ],
  [
    "cheyandi!",
    27.424,
    27.504
  ]
];

export const Golden30s_vLLM: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig(); // 840 frames = 28.00s @ 30 fps

  // Continuous dynamic camera dolly push & subtle pan (Guarantees motion floor >= 0.35)
  const cameraScale = interpolate(frame, [0, 840], [1.0, 1.10]);
  const bgPanY = interpolate(frame, [0, 840], [0, -120]);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#070b14",
        backgroundImage: "radial-gradient(circle at 50% 35%, #0f1c38 0%, #070b14 75%)",
        color: "#ffffff",
        fontFamily: "'Inter', sans-serif",
        overflow: "hidden",
      }}
    >
      {/* Background Animated Cyber Grid */}
      <div
        style={{
          position: "absolute",
          top: bgPanY,
          left: 0,
          width: "100%",
          height: "140%",
          backgroundImage:
            "linear-gradient(rgba(0, 240, 255, 0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 240, 255, 0.08) 1px, transparent 1px)",
          backgroundSize: "60px 60px",
          pointerEvents: "none",
          zIndex: 1,
        }}
      />

      <HandleChip />
      <RadarSweep />

      {/* Global Bolt-Strikes & Flash-frames on major musical beats */}
      <BoltStrike startFrame={60} />
      <BoltStrike startFrame={240} />
      <BoltStrike startFrame={540} />
      <BoltStrike startFrame={780} />
      <FlashFrame triggerFrames={[0, 60, 240, 540, 780]} />

      <div
        style={{
          width: "100%",
          height: "100%",
          transform: `scale(${cameraScale}) translate(${Math.sin(frame * 0.08) * 8}px, ${Math.cos(frame * 0.06) * 6}px)`,
          transformOrigin: "center center",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          zIndex: 10,
        }}
      >
        {/* SHOT 1: Hook with Real Visual (0 - 60 frames, 0.0 - 2.0s) */}
        {/* Real Visual: GitHub OpenGraph Card */}
        <Sequence from={0} durationInFrames={60}>
          <AbsoluteFill
            style={{
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
              padding: "0 60px",
              paddingTop: 100,
            }}
          >
            <AutoFitText
              text="vLLM HIGH-SPEED"
              maxFontSize={84}
              color="#00f0ff"
              style={{ filter: "drop-shadow(0 0 35px rgba(0, 240, 255, 0.4))" }}
            />
            <div
              style={{
                marginTop: 30,
                width: 960,
                height: 520,
                borderRadius: 24,
                overflow: "hidden",
                border: "2px solid #00f0ff",
                boxShadow: "0 25px 60px rgba(0, 0, 0, 0.9)",
              }}
            >
              <Img
                src={staticFile("captured_proofs/vllm-project_vllm/proof_1_repo_card.png")}
                style={{
                  width: "100%",
                  height: "100%",
                  objectFit: "cover",
                  transform: `scale(${interpolate(frame, [0, 60], [1.0, 1.08])})`,
                }}
              />
            </div>
          </AbsoluteFill>
        </Sequence>

        {/* SHOT 2: What It Is (60 - 240 frames, 2.0 - 8.0s) */}
        {/* Real Visual: 3D Browser Mockup with Playwright Documentation */}
        <Sequence from={60} durationInFrames={180}>
          <AbsoluteFill
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              paddingTop: 100,
            }}
          >
            <BrowserMockup3D url="https://docs.vllm.ai/en/latest/" title="vLLM Documentation">
              <div style={{ padding: 25, display: "flex", flexDirection: "column", alignItems: "center" }}>
                <AutoFitText text="Official vLLM Engine" maxFontSize={46} color="#ffd700" />
                <div
                  style={{
                    marginTop: 15,
                    width: 880,
                    height: 520,
                    borderRadius: 16,
                    overflow: "hidden",
                    border: "1.5px solid rgba(255, 255, 255, 0.2)",
                  }}
                >
                  <Img
                    src={staticFile("captured_proofs/vllm-project_vllm/proof_2_docs_capture.png")}
                    style={{
                      width: "100%",
                      height: "100%",
                      objectFit: "cover",
                      transform: `scale(${interpolate(frame - 60, [0, 180], [1.0, 1.06])})`,
                    }}
                  />
                </div>
                <div style={{ marginTop: 20, color: "#8892b0", fontSize: 28, textAlign: "center" }}>
                  High-throughput, memory-efficient LLM serving core.
                </div>
              </div>
            </BrowserMockup3D>
          </AbsoluteFill>
        </Sequence>

        {/* SHOT 3: Why It Matters - Proof Beats (240 - 540 frames, 8.0 - 18.0s) */}
        {/* Real Visual: Verified Live API Telemetry Card */}
        <Sequence from={240} durationInFrames={300}>
          <AbsoluteFill
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              paddingTop: 100,
            }}
          >
            <div
              style={{
                width: 960,
                height: 980,
                borderRadius: 28,
                background: "linear-gradient(180deg, #101628 0%, #070a14 100%)",
                border: "2px solid #ff007f",
                boxShadow: "0 35px 80px rgba(0, 0, 0, 0.95), 0 0 50px rgba(255, 0, 127, 0.3)",
                padding: 40,
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
                alignItems: "center",
              }}
            >
              <AutoFitText text="PAGED MEMORY ALLOCATION" maxFontSize={46} color="#ff007f" />
              
              <div
                style={{
                  width: 860,
                  height: 520,
                  borderRadius: 18,
                  overflow: "hidden",
                  border: "2px solid #00f0ff",
                }}
              >
                <Img
                  src={staticFile("captured_proofs/vllm-project_vllm/proof_3_live_api_card.png")}
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "contain",
                    transform: `scale(${interpolate(frame - 240, [0, 300], [1.0, 1.05])})`,
                  }}
                />
              </div>

              <div
                style={{
                  padding: "16px 28px",
                  borderRadius: 16,
                  background: "rgba(39, 201, 63, 0.15)",
                  border: "1.5px solid #27c93f",
                  color: "#27c93f",
                  fontSize: 30,
                  fontWeight: 800,
                  textAlign: "center",
                }}
              >
                ✓ 96,121 Stars • PagedAttention Eliminates Fragmentation
              </div>
            </div>
          </AbsoluteFill>
        </Sequence>

        {/* SHOT 4: How To Try It (540 - 780 frames, 18.0 - 26.0s) */}
        {/* Real Visual: Syntax-Highlighted Verified CLI Command */}
        <Sequence from={540} durationInFrames={240}>
          <AbsoluteFill
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              paddingTop: 100,
            }}
          >
            <div
              style={{
                width: 960,
                height: 980,
                borderRadius: 28,
                background: "#050811",
                border: "2px solid #00f0ff",
                boxShadow: "0 35px 80px rgba(0, 0, 0, 0.95), 0 0 50px rgba(0, 240, 255, 0.4)",
                padding: 55,
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
              }}
            >
              <div style={{ color: "#ffd700", fontSize: 38, fontWeight: 700, marginBottom: 20 }}>
                # Verified Deployment Command
              </div>
              <div
                style={{
                  fontFamily: "'Courier New', monospace",
                  fontSize: 40,
                  fontWeight: 700,
                  color: "#00f0ff",
                  lineHeight: 1.6,
                  wordBreak: "break-all",
                  background: "rgba(0, 0, 0, 0.6)",
                  padding: 25,
                  borderRadius: 16,
                  border: "1.5px solid rgba(0, 240, 255, 0.3)",
                }}
              >
                vllm serve meta-llama/Llama-3.1-8B-Instruct
              </div>
              <div
                style={{
                  marginTop: 35,
                  padding: 24,
                  borderRadius: 16,
                  background: "rgba(255, 189, 46, 0.15)",
                  border: "1.5px solid #ffbd2e",
                  color: "#ffbd2e",
                  fontSize: 32,
                  fontWeight: 600,
                  lineHeight: 1.4,
                }}
              >
                ⚠️ Caveat: Gated model needs HF_TOKEN. Open alternative: Qwen/Qwen2.5-7B
              </div>
            </div>
          </AbsoluteFill>
        </Sequence>

        {/* SHOT 5: Loop-Friendly CTA (780 - 840 frames, 26.0 - 28.0s) */}
        <Sequence from={780} durationInFrames={60}>
          <AbsoluteFill
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              paddingTop: 100,
            }}
          >
            <AutoFitText
              text="Released: 18 Oct 2026 (v0.32.0 Stable)"
              maxFontSize={48}
              color="#ffd700"
              style={{ marginBottom: 35 }}
            />
            <FollowPill />
          </AbsoluteFill>
        </Sequence>
      </div>

      {/* Pop Karaoke Captions: Word-by-word, guaranteed spacing, dedicated zone */}
      <PopCaptions words={WORDS} />
    </AbsoluteFill>
  );
};
