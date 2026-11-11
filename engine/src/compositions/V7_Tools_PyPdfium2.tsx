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

import {
  LightStudioCanvas,
  Studio3DSlab,
  DeviceMockup,
  KineticTypography,
  FeatureBulletList,
  StudioCaptions,
  StudioEndCard,
  BenchmarkRaceAdapter,
  CodeExecutionAdapter,
  DocumentExtractionAdapter,
} from "../components/studio";

import wordsTools from "../assets/v7_tools_words.json";

export const V7_Tools_PyPdfium2: React.FC = () => {
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
      <Audio src={staticFile("audio/v7_tools_master_48k.mp3")} />

      {/* LAYER 2: Light Studio Canvas & 3D Camera Environment */}
      <LightStudioCanvas primaryAccent="#0284C7" gridId="gridToolsStudio">
        <div style={{ position: "absolute", inset: 0 }}>
          {/* BEAT 1 (0.0s - 10.0s, Frames 0 - 300): Real arXiv Paper & Bounding Boxes */}
          <Sequence from={0} durationInFrames={300}>
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
                kicker="ACADEMIC PDF TEXT EXTRACTION"
                prefix="Which Python tool is best for extraction?"
                focalText="pypdfium2 Speed Benchmark"
                kickerColor="#0284C7"
                focalColor="#0F172A"
              />

              <Studio3DSlab width={600} height={680} pitch={6} yaw={-3} elevation={24}>
                <DeviceMockup
                  type="paper"
                  title="Attention Is All You Need"
                  subtitle="15 Pages • arXiv:1706.03762"
                  badge="PDFIUM C++"
                >
                  <DocumentExtractionAdapter
                    title="Attention Is All You Need"
                    paperId="arXiv:1706.03762"
                    totalPages={15}
                    containerWidth={560}
                    containerHeight={600}
                  />
                </DeviceMockup>
              </Studio3DSlab>
            </div>
          </Sequence>

          {/* BEAT 2 (10.0s - 23.0s, Frames 300 - 690): Empirical 10-Run Benchmark Race */}
          <Sequence from={300} durationInFrames={390}>
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
                kicker="EMPIRICAL EVIDENCE • 10 RUNS"
                prefix="Full text extracted from all 15 pages"
                focalText="Benchmark Race"
                kickerColor="#0284C7"
                focalColor="#0F172A"
              />

              <Studio3DSlab width={600} height={680} pitch={5} yaw={3} elevation={22}>
                <DeviceMockup
                  type="window"
                  title="benchmarks.py // 10 runs"
                  badge="MEASURED MEDIAN"
                >
                  <BenchmarkRaceAdapter
                    title="Extraction Time (All 15 Pages)"
                    testSpec="arXiv:1706.03762 • 1 Warmup + 10 Measured Runs"
                    speedupText="5.85x FASTER"
                    hardwareFooter="AMD64 Windows 10 • Python 3.11"
                    benchmarks={[
                      { name: "pypdfium2 5.6.0", timeMs: 239, isBaseline: true, badge: "FASTEST (1.0x)" },
                      { name: "pypdf 6.9.2", timeMs: 1400, badge: "5.85x SLOW" },
                      { name: "pdfminer.six", timeMs: 4065, badge: "17.0x SLOW" },
                    ]}
                  />
                </DeviceMockup>
              </Studio3DSlab>
            </div>
          </Sequence>

          {/* BEAT 3 (23.0s - 34.0s, Frames 690 - 1020): Single-Column Truth & Token Count */}
          <Sequence from={690} durationInFrames={330}>
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
                kicker="LIMITATIONS & TRUTH CHECK"
                prefix="Full empirical disclosure"
                focalText="Paper Layout & Tokens"
                kickerColor="#D97706"
                focalColor="#0F172A"
              />

              <Studio3DSlab width={600} height={680} pitch={6} yaw={-3} elevation={20}>
                <div style={{ padding: 22, height: "100%", display: "flex", flexDirection: "column", justifyContent: "space-between", boxSizing: "border-box" }}>
                  <FeatureBulletList
                    items={[
                      {
                        icon: "diamond",
                        title: "Single-Column Paper Warning",
                        subtitle: "Idi single-column paper. Two-column lo order maarochu, nenu test cheyyaledu.",
                        color: "#D97706",
                        metric: "LAYOUT",
                      },
                      {
                        icon: "sparkle",
                        title: "Exact Token Count",
                        subtitle: "tiktoken tho 10187 tokens count chesam (cl100k_base tokenizer).",
                        color: "#059669",
                        metric: "10,187 TOKENS",
                      },
                      {
                        icon: "check",
                        title: "Zero Native Build Tools Needed",
                        subtitle: "Precompiled Chromium PDFium binaries included in pip wheel.",
                        color: "#0284C7",
                        metric: "WHEEL",
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
                    <span>arXiv:1706.03762v7 • Attention Is All You Need</span>
                    <span style={{ color: "#D97706" }}>DISCLOSED LIMITATION</span>
                  </div>
                </div>
              </Studio3DSlab>
            </div>
          </Sequence>

          {/* BEAT 4 (34.0s - 39.8s, Frames 1020 - 1194): Real CLI Run & Summary */}
          <Sequence from={1020} durationInFrames={174}>
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
                kicker="SUMMARY & INSTALLATION"
                prefix="Fastest extraction in pure Python"
                focalText="pypdfium2 Ready"
                kickerColor="#0284C7"
                focalColor="#0F172A"
              />

              <Studio3DSlab width={600} height={680} pitch={5} yaw={2} elevation={22}>
                <DeviceMockup
                  type="window"
                  title="terminal // bash execution"
                  badge="VERIFIED"
                >
                  <CodeExecutionAdapter
                    command="pip install pypdfium2 && python extract.py"
                    toolVersion="pypdfium2 5.6.0 • ctypes"
                    executionTimeMs={239}
                    lines={[
                      { text: ">>> Loading arXiv:1706.03762 (15 pages)...", color: "#38BDF8", isHeader: true },
                      { text: "[Run 1..10] Median extraction time: 239.07 ms", color: "#10B981" },
                      { text: "[Comparative] pypdf: 1399.62 ms (5.85x slower)", color: "#F59E0B" },
                      { text: "[Comparative] pdfminer.six: 4065.08 ms (17.0x slower)", color: "#EF4444" },
                      { text: "[Tokens] 10,187 tokens counted via tiktoken cl100k_base", color: "#A855F7" },
                      { text: "✓ Extraction finished with zero corrupted character blocks", color: "#10B981" },
                    ]}
                  />
                </DeviceMockup>
              </Studio3DSlab>
            </div>
          </Sequence>

          {/* BEAT 5 (39.8s - 42.0s = LAST 2.2 SECONDS): Gated Light Studio End Card */}
          <Sequence from={1194} durationInFrames={66}>
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
        words={wordsTools}
        currentSec={currentSec}
        accentColor="#0284C7"
        endCardStartSec={39.8}
      />
    </AbsoluteFill>
  );
};
