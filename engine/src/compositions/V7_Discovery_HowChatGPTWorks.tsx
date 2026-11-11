import React from "react";
import {
  AbsoluteFill,
  Audio,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

import {
  LightStudioCanvas,
  Studio3DSlab,
  DeviceMockup,
  KineticTypography,
  FeatureBulletList,
  StudioCaptions,
  StudioEndCard,
  ArchitectureFlowAdapter,
} from "../components/studio";

import wordsDiscovery from "../assets/v7_discovery_words.json";

export const V7_Discovery_HowChatGPTWorks: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentSec = frame / fps;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#050C18",
        color: "#FFFFFF",
        fontFamily: "'Inter', -apple-system, sans-serif",
        overflow: "hidden",
      }}
    >
      {/* LAYER 1: Master Audio Track (48kHz, -14.0 +/- 0.5 LUFS, <= -1.5 dBTP) */}
      <Audio src={staticFile("audio/v7_discovery_master_48k.mp3")} />

      {/* LAYER 2: Light Studio Canvas & 3D Environment */}
      <LightStudioCanvas primaryAccent="#0284C7" gridId="gridDiscoveryStudio">
        <div style={{ position: "absolute", inset: 0 }}>
          {/* BEAT 1 (0.0s - 9.0s, Frames 0 - 270): Subword Tokens Breakdown */}
          <Sequence from={0} durationInFrames={270}>
            <div
              style={{
                width: "100%",
                height: "100%",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                paddingTop: 80,
                boxSizing: "border-box",
              }}
            >
              <KineticTypography
                kicker="GPT-2 (OPEN MODEL), EXAMPLE RUN"
                prefix="How do language models predict the next word?"
                focalText="Subword Token Input"
                kickerColor="#0284C7"
                focalColor="#0F172A"
              />

              <Studio3DSlab width={600} height={680} pitch={6} yaw={-3} elevation={24}>
                <DeviceMockup
                  type="window"
                  title="tokenizer.py // cl100k / bpe"
                  badge="INPUT PROMPT"
                >
                  <div style={{ display: "flex", flexDirection: "column", justifyContent: "space-between", height: "100%", boxSizing: "border-box" }}>
                    <div>
                      <div style={{ fontSize: 13, fontWeight: 900, color: "#0284C7", fontFamily: "'JetBrains Mono', monospace", marginBottom: 8 }}>
                        EXAMPLE PROMPT STRING:
                      </div>
                      <div
                        style={{
                          fontSize: 22,
                          fontWeight: 800,
                          color: "#0F172A",
                          backgroundColor: "#F1F5F9",
                          border: "1.5px solid #CBD5E1",
                          borderRadius: 14,
                          padding: "16px 18px",
                          lineHeight: 1.35,
                          marginBottom: 16,
                        }}
                      >
                        "The future of artificial intelligence is"
                      </div>

                      <div style={{ fontSize: 13, fontWeight: 900, color: "#64748B", fontFamily: "'JetBrains Mono', monospace", marginBottom: 8 }}>
                        PARSED BPE TOKEN IDS:
                      </div>

                      <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                        {[
                          { text: "The", id: 464 },
                          { text: " future", id: 2003 },
                          { text: " of", id: 286 },
                          { text: " artificial", id: 11666 },
                          { text: " intelligence", id: 4430 },
                          { text: " is", id: 318 },
                        ].map((t, idx) => (
                          <div
                            key={idx}
                            style={{
                              backgroundColor: "#FFFFFF",
                              border: "1.5px solid #E2E8F0",
                              borderRadius: 8,
                              padding: "6px 10px",
                              display: "flex",
                              flexDirection: "column",
                              alignItems: "center",
                              boxShadow: "0 2px 6px rgba(0,0,0,0.04)",
                            }}
                          >
                            <span style={{ fontSize: 10, color: "#64748B", fontFamily: "'JetBrains Mono', monospace" }}>
                              #{t.id}
                            </span>
                            <span style={{ fontSize: 14, fontWeight: 800, color: "#0284C7" }}>
                              {t.text}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div
                      style={{
                        borderTop: "1.5px solid #F1F5F9",
                        paddingTop: 10,
                        display: "flex",
                        justifyContent: "space-between",
                        fontSize: 11,
                        color: "#64748B",
                        fontFamily: "'JetBrains Mono', monospace",
                        fontWeight: 700,
                      }}
                    >
                      <span>GPT-2 Small • 124M Parameters</span>
                      <span style={{ color: "#059669" }}>768-DIM EMBEDDING</span>
                    </div>
                  </div>
                </DeviceMockup>
              </Studio3DSlab>
            </div>
          </Sequence>

          {/* BEAT 2 (9.0s - 22.0s, Frames 270 - 660): Layer 11 Head 0 Self-Attention Weights */}
          <Sequence from={270} durationInFrames={390}>
            <div
              style={{
                width: "100%",
                height: "100%",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                paddingTop: 80,
                boxSizing: "border-box",
              }}
            >
              <KineticTypography
                kicker="TRANSFORMER ATTENTION MATRIX"
                prefix="Attention connects previous tokens to query"
                focalText="Layer 11 • Head 0"
                kickerColor="#0284C7"
                focalColor="#0F172A"
              />

              <Studio3DSlab width={600} height={680} pitch={5} yaw={3} elevation={22}>
                <div style={{ padding: 18, height: "100%", boxSizing: "border-box" }}>
                  <ArchitectureFlowAdapter
                    layer={11}
                    head={0}
                    mode="attention"
                    width={560}
                    height={630}
                  />
                </div>
              </Studio3DSlab>
            </div>
          </Sequence>

          {/* BEAT 3 (22.0s - 35.0s, Frames 660 - 1050): Softmax Top 5 Probabilities & Entropy */}
          <Sequence from={660} durationInFrames={390}>
            <div
              style={{
                width: "100%",
                height: "100%",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                paddingTop: 80,
                boxSizing: "border-box",
              }}
            >
              <KineticTypography
                kicker="SOFTMAX PROBABILITY SAMPLING"
                prefix="Model confident ga ledu, entropy ekkuvaga undi"
                focalText="Top-5 Sum: 26.53%"
                kickerColor="#D97706"
                focalColor="#0F172A"
              />

              <Studio3DSlab width={600} height={680} pitch={6} yaw={-3} elevation={22}>
                <div style={{ padding: 18, height: "100%", boxSizing: "border-box" }}>
                  <ArchitectureFlowAdapter
                    layer={11}
                    head={0}
                    mode="probability"
                    width={560}
                    height={630}
                  />
                </div>
              </Studio3DSlab>
            </div>
          </Sequence>

          {/* BEAT 4 (35.0s - 41.8s, Frames 1050 - 1254): Recap & ChatGPT Disclosure */}
          <Sequence from={1050} durationInFrames={204}>
            <div
              style={{
                width: "100%",
                height: "100%",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                paddingTop: 80,
                boxSizing: "border-box",
              }}
            >
              <KineticTypography
                kicker="ARCHITECTURE TAKEAWAY"
                prefix="Core principles of next-token generation"
                focalText="How LLMs Predict"
                kickerColor="#0284C7"
                focalColor="#0F172A"
              />

              <Studio3DSlab width={600} height={680} pitch={5} yaw={2} elevation={20}>
                <div style={{ padding: 22, height: "100%", display: "flex", flexDirection: "column", justifyContent: "space-between", boxSizing: "border-box" }}>
                  <FeatureBulletList
                    items={[
                      {
                        icon: "sparkle",
                        title: "Multi-Head Attention",
                        subtitle: "Weights context tokens dynamically for the final query token.",
                        color: "#0284C7",
                        metric: "ATTN",
                      },
                      {
                        icon: "diamond",
                        title: "Softmax Probability",
                        subtitle: "Converts logits into probability distribution across vocabulary.",
                        color: "#D97706",
                        metric: "SOFTMAX",
                      },
                      {
                        icon: "check",
                        title: "Open Model Baseline",
                        subtitle: "ChatGPT weights are proprietary; GPT-2 small is open baseline.",
                        color: "#059669",
                        metric: "OPEN GPT-2",
                      },
                    ]}
                  />

                  <div
                    style={{
                      borderTop: "1.5px solid #F1F5F9",
                      paddingTop: 10,
                      display: "flex",
                      justifyContent: "space-between",
                      fontSize: 11,
                      color: "#64748B",
                      fontFamily: "'JetBrains Mono', monospace",
                      fontWeight: 700,
                    }}
                  >
                    <span>Vaswani et al. 2017 • Radford et al. 2019</span>
                    <span style={{ color: "#0284C7" }}>VERIFIED ARCHITECTURE</span>
                  </div>
                </div>
              </Studio3DSlab>
            </div>
          </Sequence>

          {/* BEAT 5 (41.8s - 44.0s = LAST 2.2 SECONDS): Gated Light Studio End Card */}
          <Sequence from={1254} durationInFrames={66}>
            <StudioEndCard
              brandHandle="@flash__ai__digital"
              subtitle="Daily AI and dev updates, with sources"
              primaryAccent="#0284C7"
            />
          </Sequence>
        </div>
      </LightStudioCanvas>

      {/* LAYER 3: Word-by-Word Synchronized Captions */}
      <StudioCaptions
        words={wordsDiscovery}
        currentSec={currentSec}
        accentColor="#0284C7"
        endCardStartSec={41.8}
      />
    </AbsoluteFill>
  );
};
