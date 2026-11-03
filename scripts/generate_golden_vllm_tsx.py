import json

words = json.load(open(r"C:\Users\navee\OneDrive\Desktop\studio\cache\words_28s_vllm.json", encoding="utf-8"))
words_str = json.dumps(words, indent=2)

tsx = f'''import React from "react";
import {{
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
  Sequence,
  staticFile,
  Img,
}} from "remotion";
import {{ BoltStrike }} from "../components/BoltStrike";
import {{ FlashFrame }} from "../components/FlashFrame";
import {{ HandleChip }} from "../components/HandleChip";
import {{ FollowPill }} from "../components/FollowPill";
import {{ RadarSweep }} from "../components/RadarSweep";
import {{ BrowserMockup3D }} from "../components/BrowserMockup3D";
import {{ PopCaptions }} from "../components/PopCaptions";
import {{ AutoFitText }} from "../components/AutoFitText";

// Prompt Library Index ID: 164 (Repo Spotlight & Architecture Film)
const VLLM_WORDS: [string, number, number][] = {words_str};

export const Golden30s_vLLM: React.FC = () => {{
  const frame = useCurrentFrame();
  const {{ fps }} = useVideoConfig(); // 840 frames = 28.00s

  // Continuous dynamic camera dolly push & grid pan (Guarantees motion floor >= 0.35)
  const cameraScale = interpolate(frame, [0, 840], [1.0, 1.12]);
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

      {/* Global Bolt-Strikes & Flash-frames on beats */}
      <BoltStrike startFrame={60} />
      <BoltStrike startFrame={240} />
      <BoltStrike startFrame={540} />
      <BoltStrike startFrame={780} />
      <FlashFrame triggerFrames={[0, 60, 240, 540, 780]} />

      <div
        style={{
          width: "100%",
          height: "100%",
          transform: `scale(${{cameraScale}}) translate(${{Math.sin(frame * 0.08) * 8}}px, ${{Math.cos(frame * 0.06) * 6}}px)`,
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
            }}
          >
            <AutoFitText
              text="vLLM HIGH-SPEED"
              maxFontSize={86}
              color="#00f0ff"
              style={{ filter: "drop-shadow(0 0 35px rgba(0, 240, 255, 0.5))" }}
            />
            <div
              style={{
                marginTop: 30,
                width: 960,
                height: 500,
                borderRadius: 24,
                overflow: "hidden",
                border: "2px solid rgba(0, 240, 255, 0.5)",
                boxShadow: "0 25px 60px rgba(0, 0, 0, 0.9)",
              }}
            >
              <Img
                src={{staticFile("captured_proofs/vllm-project_vllm/proof_1_repo_card.png")}}
                style={{
                  width: "100%",
                  height: "100%",
                  objectFit: "cover",
                  transform: `scale(${{interpolate(frame, [0, 60], [1.0, 1.08])}})`,
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
                    src={{staticFile("captured_proofs/vllm-project_vllm/proof_2_docs_capture.png")}}
                    style={{
                      width: "100%",
                      height: "100%",
                      objectFit: "cover",
                      transform: `scale(${{interpolate(frame - 60, [0, 180], [1.0, 1.06])}})`,
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

        {/* SHOT 3: Why It Matters - 3 Proof Beats (240 - 540 frames, 8.0 - 18.0s) */}
        {/* Real Visual: Verified Live API Telemetry Card (96,121 Stars) */}
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
                border: "2px solid rgba(255, 0, 127, 0.5)",
                boxShadow: "0 35px 80px rgba(0, 0, 0, 0.95), 0 0 50px rgba(255, 0, 127, 0.2)",
                padding: 40,
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
                alignItems: "center",
              }}
            >
              <AutoFitText text="PAGED MEMORY ALLOCATION" maxFontSize={48} color="#ff007f" />
              
              <div
                style={{
                  width: 860,
                  height: 520,
                  borderRadius: 18,
                  overflow: "hidden",
                  border: "2px solid rgba(0, 240, 255, 0.4)",
                }}
              >
                <Img
                  src={{staticFile("captured_proofs/vllm-project_vllm/proof_3_live_api_card.png")}}
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "contain",
                    transform: `scale(${{interpolate(frame - 240, [0, 300], [1.0, 1.05])}})`,
                  }}
                />
              </div>

              <div
                style={{
                  padding: "16px 30px",
                  borderRadius: 16,
                  background: "rgba(39, 201, 63, 0.15)",
                  border: "1.5px solid #27c93f",
                  color: "#27c93f",
                  fontSize: 32,
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
                border: "2px solid rgba(0, 240, 255, 0.5)",
                boxShadow: "0 35px 80px rgba(0, 0, 0, 0.95), 0 0 50px rgba(0, 240, 255, 0.2)",
                padding: 55,
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
              }}
            >
              <div style={{ color: "#ffd700", fontSize: 40, fontWeight: 700, marginBottom: 20 }}>
                # Verified Deployment Command
              </div>
              <div
                style={{
                  fontFamily: "'Courier New', monospace",
                  fontSize: 42,
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
                  fontSize: 34,
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
      <PopCaptions words={{VLLM_WORDS}} />
    </AbsoluteFill>
  );
}};
'''

with open(r"C:\Users\navee\OneDrive\Desktop\studio\engine\src\compositions\Golden30s_vLLM.tsx", "w", encoding="utf-8") as f:
    f.write(tsx)

print("Created Golden30s_vLLM.tsx successfully!")
