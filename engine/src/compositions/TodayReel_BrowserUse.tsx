import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  staticFile,
  Img,
} from "remotion";
import wordsData from "../../../cache/words_final_today_2_browseruse.json";

export const TodayReel_BrowserUse: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  // Sentence-derived Narrative Visual Beats across 840 frames (28.00s @ 30fps)
  // Shot 1: 0 - 153 (0.00s - 5.11s) Cover Lockup: Browser Use - Autonomous Web Agent
  // Shot 2: 153 - 223 (5.11s - 7.44s) Core Release 0.13.14 & Official Architecture Visual
  // Shot 3: 223 - 363 (7.44s - 12.13s) Official Quickstart: uv pip install browser-use & uvx install
  // Shot 4: 363 - 474 (12.13s - 15.81s) Real Python Controller: from browser_use import Agent, ChatBrowserUse
  // Shot 5: 474 - 548 (15.81s - 18.27s) Hero Benchmark Visual: accuracy_by_model_dark.png
  // Shot 6: 548 - 670 (18.27s - 22.36s) GitHub Stars: 120,244 Stars
  // Shot 7: 670 - 744 (22.36s - 24.80s) Source & License: browser-use team (@browser-use) • MIT
  // Shot 8: 744 - 840 (24.80s - 28.00s) FLASH Brand End Card

  const shot =
    frame < 153
      ? 1
      : frame < 223
      ? 2
      : frame < 363
      ? 3
      : frame < 474
      ? 4
      : frame < 548
      ? 5
      : frame < 670
      ? 6
      : frame < 744
      ? 7
      : 8;

  const shotRel =
    shot === 1
      ? frame
      : shot === 2
      ? frame - 153
      : shot === 3
      ? frame - 223
      : shot === 4
      ? frame - 363
      : shot === 5
      ? frame - 474
      : shot === 6
      ? frame - 548
      : shot === 7
      ? frame - 670
      : frame - 744;

  // CONTINUOUS ACTIVE MOTION DERIVED FROM SENTENCE TIMELINE (Unique Dynamics for Reel 2)
  const camZoom = 1.0 + (frame / 840) * 0.11;
  const camPanX = Math.cos(frame * 0.04) * 15;
  const camPanY = Math.sin(frame * 0.05) * 12;

  // Distinct transitions at each sentence cut point
  const cutFrames = [153, 223, 363, 474, 548, 670, 744];
  const distToCut = Math.min(...cutFrames.map((cf) => Math.abs(frame - cf)));
  const transitionFlash =
    distToCut === 0 ? 0.70 : distToCut === 1 ? 0.35 : distToCut === 2 ? 0.12 : 0;
  const transitionWhipY = distToCut === 0 ? 35 : distToCut === 1 ? 14 : 0;

  // Dynamic Amber/Orange Grid Shift
  const scanLineY = (frame * 16) % height;
  const gridShiftX = (frame * 3) % 50;

  // Active Spoken Caption
  const currentSec = frame / 30;
  const activeWordObj = (wordsData as any[]).find(
    (w) => currentSec >= w.start && currentSec <= w.end
  );
  const activeWord = activeWordObj ? activeWordObj.word : "";

  // Render Subtitles (max 3 words per group, active word highlighted)
  const renderSubtitles = () => {
    if (shot === 8 || currentSec > 24.5) return null;
    const activeIdx = (wordsData as any[]).findIndex(
      (w) => currentSec >= w.start && currentSec <= w.end
    );
    if (activeIdx === -1) return null;

    const startIdx = Math.max(0, activeIdx - 1);
    const endIdx = Math.min(wordsData.length, activeIdx + 2);
    const slice = (wordsData as any[]).slice(startIdx, endIdx);

    return (
      <div
        style={{
          position: "absolute",
          bottom: 180,
          left: 40,
          right: 40,
          textAlign: "center",
          zIndex: 100,
          display: "flex",
          justifyContent: "center",
          gap: 12,
          flexWrap: "wrap",
        }}
      >
        {slice.map((item, idx) => {
          const isCurrent = item.word === activeWord;
          return (
            <span
              key={idx}
              style={{
                fontSize: isCurrent ? 42 : 36,
                fontWeight: 900,
                color: isCurrent ? "#FFB703" : "#FFFFFF",
                textShadow: isCurrent
                  ? "0 0 25px rgba(255, 183, 3, 0.8), 0 2px 10px rgba(0,0,0,0.9)"
                  : "0 2px 8px rgba(0,0,0,0.8)",
                background: isCurrent ? "rgba(255, 183, 3, 0.15)" : "transparent",
                padding: "2px 8px",
                borderRadius: 8,
              }}
            >
              {item.word}
            </span>
          );
        })}
      </div>
    );
  };

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#07090E",
        color: "#FFFFFF",
        fontFamily:
          '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        overflow: "hidden",
      }}
    >
      {/* Background Animated Dynamic Amber Grid */}
      <div
        style={{
          position: "absolute",
          inset: -100,
          backgroundImage: `linear-gradient(to right, rgba(255, 183, 3, 0.05) 1px, transparent 1px),
                            linear-gradient(to bottom, rgba(255, 183, 3, 0.05) 1px, transparent 1px)`,
          backgroundSize: "50px 50px",
          transform: `translateX(${gridShiftX}px)`,
          opacity: 0.8,
        }}
      />

      {/* Ambient Radial Amber Glow */}
      <div
        style={{
          position: "absolute",
          top: "15%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          width: 900,
          height: 900,
          borderRadius: "50%",
          background:
            "radial-gradient(circle, rgba(255, 183, 3, 0.14) 0%, transparent 70%)",
          filter: "blur(60px)",
          pointerEvents: "none",
        }}
      />

      {/* Moving Technical Scanner Line */}
      <div
        style={{
          position: "absolute",
          top: scanLineY,
          left: 0,
          right: 0,
          height: 2,
          background:
            "linear-gradient(90deg, transparent, rgba(255, 183, 3, 0.6), transparent)",
          boxShadow: "0 0 15px rgba(255, 183, 3, 0.8)",
          pointerEvents: "none",
        }}
      />

      {/* Flash Transition Overlay */}
      {transitionFlash > 0 && (
        <AbsoluteFill
          style={{
            backgroundColor: "#FFFFFF",
            opacity: transitionFlash,
            pointerEvents: "none",
            zIndex: 90,
          }}
        />
      )}

      {/* Header Bar */}
      <div
        style={{
          position: "absolute",
          top: 70,
          left: 60,
          right: 60,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          zIndex: 80,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
          <div
            style={{
              width: 14,
              height: 14,
              borderRadius: "50%",
              backgroundColor: "#FFB703",
              boxShadow: "0 0 12px #FFB703",
            }}
          />
          <span
            style={{
              fontSize: 22,
              fontWeight: 800,
              letterSpacing: 3,
              color: "#FFFFFF",
            }}
          >
            FLASH AUTOMATION
          </span>
        </div>
        <div
          style={{
            padding: "6px 14px",
            borderRadius: 20,
            background: "rgba(255, 183, 3, 0.12)",
            border: "1px solid rgba(255, 183, 3, 0.3)",
            fontSize: 16,
            fontWeight: 700,
            color: "#FFB703",
          }}
        >
          RELEASE 0.13.14
        </div>
      </div>

      {/* MAIN CONTENT AREA */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          transform: `scale(${camZoom}) translate(${camPanX}px, ${camPanY + transitionWhipY}px)`,
          padding: "160px 60px",
          zIndex: 50,
        }}
      >
        {/* SHOT 1: Cover Lockup (0 - 153 frames | 0.00s - 5.11s) */}
        {shot === 1 && (
          <div style={{ textAlign: "center", maxWidth: 960 }}>
            <div
              style={{
                display: "inline-block",
                padding: "8px 20px",
                borderRadius: 20,
                background: "rgba(255, 183, 3, 0.15)",
                border: "1px solid #FFB703",
                fontSize: 18,
                fontWeight: 800,
                color: "#FFB703",
                letterSpacing: 2,
                marginBottom: 24,
                textTransform: "uppercase",
              }}
            >
              AUTONOMOUS WEB ENGINE
            </div>
            <div
              style={{
                fontSize: 90,
                fontWeight: 900,
                letterSpacing: -2,
                lineHeight: 1.05,
                background: "linear-gradient(180deg, #FFFFFF 0%, #CBD5E1 100%)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
                marginBottom: 24,
              }}
            >
              Browser Use
            </div>
            <div
              style={{
                fontSize: 32,
                color: "#E2E8F0",
                lineHeight: 1.4,
                fontWeight: 600,
              }}
            >
              Open-source Python library for AI browser agents and Playwright automation
            </div>
          </div>
        )}

        {/* SHOT 2: HERO VISUAL 1 - Real Architecture / Brand Visual (153 - 223 frames | 5.11s - 7.44s) */}
        {shot === 2 && (
          <div style={{ width: "100%", maxWidth: 900, textAlign: "center" }}>
            <div
              style={{
                fontSize: 16,
                fontWeight: 800,
                color: "#FFB703",
                letterSpacing: 2,
                marginBottom: 16,
                textTransform: "uppercase",
              }}
            >
              CORE RELEASE 0.13.14
            </div>
            {/* Hero Visual >= 45% frame height (880px height in 1920) */}
            <div
              style={{
                width: "100%",
                height: 880,
                borderRadius: 24,
                overflow: "hidden",
                border: "2px solid rgba(255, 183, 3, 0.5)",
                boxShadow: "0 0 60px rgba(255, 183, 3, 0.25)",
                background: "#080C14",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                padding: 40,
                position: "relative",
              }}
            >
              <Img
                src={staticFile("captured_proofs/browser_use/browser-use-dark.png")}
                style={{
                  width: "90%",
                  maxHeight: 500,
                  objectFit: "contain",
                }}
              />
              <div
                style={{
                  marginTop: 30,
                  background: "rgba(15, 23, 42, 0.8)",
                  padding: "16px 24px",
                  borderRadius: 14,
                  border: "1px solid rgba(255, 255, 255, 0.1)",
                  fontSize: 22,
                  color: "#E2E8F0",
                  fontWeight: 600,
                  maxWidth: 760,
                }}
              >
                Connects LLMs directly to browser DOM elements, tabs, and interactive sessions
              </div>
            </div>
          </div>
        )}

        {/* SHOT 3: Official Installation (223 - 363 frames | 7.44s - 12.13s) */}
        {shot === 3 && (
          <div style={{ width: "100%", maxWidth: 880 }}>
            <div
              style={{
                fontSize: 18,
                fontWeight: 800,
                color: "#FFB703",
                letterSpacing: 2,
                marginBottom: 16,
                textTransform: "uppercase",
              }}
            >
              INSTALLATION
            </div>
            <div
              style={{
                background: "#05070B",
                border: "1px solid rgba(255, 183, 3, 0.4)",
                borderRadius: 18,
                padding: 36,
                boxShadow: "0 20px 50px rgba(0,0,0,0.8)",
              }}
            >
              <div style={{ display: "flex", gap: 10, marginBottom: 20 }}>
                <div style={{ width: 14, height: 14, borderRadius: "50%", background: "#FF5F56" }} />
                <div style={{ width: 14, height: 14, borderRadius: "50%", background: "#FFBD2E" }} />
                <div style={{ width: 14, height: 14, borderRadius: "50%", background: "#27C93F" }} />
                <div style={{ fontSize: 16, color: "#94A3B8", marginLeft: 10, fontFamily: "monospace" }}>terminal</div>
              </div>
              <div style={{ fontFamily: "monospace", fontSize: 26, color: "#38BDF8", lineHeight: 1.8 }}>
                <div>$ uv pip install browser-use</div>
                <div style={{ color: "#FFB703" }}>$ uvx browser-use install</div>
              </div>
              <div style={{ color: "#E2E8F0", marginTop: 24, fontSize: 20, lineHeight: 1.5 }}>
                Official quickstart with Astral uv package manager and Playwright browser binaries.
              </div>
            </div>
          </div>
        )}

        {/* SHOT 4: Real Python Controller (363 - 474 frames | 12.13s - 15.81s) */}
        {shot === 4 && (
          <div style={{ width: "100%", maxWidth: 880 }}>
            <div
              style={{
                fontSize: 18,
                fontWeight: 800,
                color: "#FFB703",
                letterSpacing: 2,
                marginBottom: 16,
                textTransform: "uppercase",
              }}
            >
              PYTHON CONTROLLER
            </div>
            <div
              style={{
                background: "#030508",
                border: "2px solid #FFB703",
                borderRadius: 20,
                padding: 32,
                boxShadow: "0 0 40px rgba(255, 183, 3, 0.3)",
              }}
            >
              <div style={{ fontFamily: "monospace", fontSize: 22, lineHeight: 1.5 }}>
                <div style={{ color: "#FF7B72" }}>
                  from <span style={{ color: "#FFA657" }}>browser_use</span> import <span style={{ color: "#79C0FF" }}>Agent, ChatBrowserUse</span>
                </div>
                <div style={{ marginTop: 14, color: "#E6EDF3" }}>
                  agent = <span style={{ color: "#79C0FF" }}>Agent</span>(
                </div>
                <div style={{ paddingLeft: 24, color: "#A5D6FF" }}>
                  task=<span style={{ color: "#A5D6FF" }}>&quot;Find stars of browser-use repo&quot;</span>,
                </div>
                <div style={{ paddingLeft: 24, color: "#A5D6FF" }}>
                  llm=ChatBrowserUse(model=&quot;bu-2-0&quot;)
                </div>
                <div style={{ color: "#E6EDF3" }}>)</div>
                <div style={{ marginTop: 14, color: "#7EE787" }}>
                  history = await agent.run()
                </div>
              </div>
            </div>
          </div>
        )}

        {/* SHOT 5: HERO VISUAL 2 - Accuracy / Benchmark Visual (474 - 548 frames | 15.81s - 18.27s) */}
        {shot === 5 && (
          <div style={{ width: "100%", maxWidth: 900, textAlign: "center" }}>
            <div
              style={{
                fontSize: 16,
                fontWeight: 800,
                color: "#FFB703",
                letterSpacing: 2,
                marginBottom: 16,
                textTransform: "uppercase",
              }}
            >
              AUTOMATION BENCHMARK
            </div>
            {/* Hero Visual >= 45% frame height */}
            <div
              style={{
                width: "100%",
                height: 880,
                borderRadius: 24,
                overflow: "hidden",
                border: "2px solid rgba(255, 183, 3, 0.5)",
                boxShadow: "0 0 60px rgba(255, 183, 3, 0.25)",
                background: "#080C14",
                position: "relative",
              }}
            >
              <Img
                src={staticFile("captured_proofs/browser_use/accuracy_by_model_dark.png")}
                style={{
                  width: "100%",
                  height: "100%",
                  objectFit: "contain",
                }}
              />
              <div
                style={{
                  position: "absolute",
                  bottom: 20,
                  left: 20,
                  right: 20,
                  background: "rgba(7, 9, 14, 0.85)",
                  backdropFilter: "blur(12px)",
                  padding: "12px 20px",
                  borderRadius: 12,
                  border: "1px solid rgba(255,255,255,0.1)",
                  fontSize: 18,
                  color: "#E2E8F0",
                  fontWeight: 600,
                }}
              >
                Official Benchmark • Web Navigation Success Rate Across LLMs
              </div>
            </div>
          </div>
        )}

        {/* SHOT 6: GitHub Stars (548 - 670 frames | 18.27s - 22.36s) */}
        {shot === 6 && (
          <div style={{ textAlign: "center" }}>
            <div
              style={{
                fontSize: 18,
                fontWeight: 800,
                color: "#FFB703",
                letterSpacing: 2,
                marginBottom: 16,
                textTransform: "uppercase",
              }}
            >
              GITHUB REPOSITORY METRICS
            </div>
            <div
              style={{
                fontSize: 110,
                fontWeight: 900,
                letterSpacing: -3,
                color: "#FFFFFF",
                textShadow: "0 0 50px rgba(255, 183, 3, 0.6)",
                lineHeight: 1,
              }}
            >
              120,244
            </div>
            <div
              style={{
                fontSize: 32,
                fontWeight: 800,
                color: "#FFB703",
                marginTop: 12,
                letterSpacing: 2,
              }}
            >
              STARS REACHED
            </div>
          </div>
        )}

        {/* SHOT 7: MIT License & Team Grounding (670 - 744 frames | 22.36s - 24.80s) */}
        {shot === 7 && (
          <div style={{ textAlign: "center", maxWidth: 800 }}>
            <div
              style={{
                fontSize: 16,
                fontWeight: 800,
                color: "#FFB703",
                letterSpacing: 2,
                marginBottom: 16,
                textTransform: "uppercase",
              }}
            >
              SOURCE &amp; LICENSE
            </div>
            <div style={{ fontSize: 36, fontWeight: 900, color: "#FFFFFF", marginBottom: 12 }}>
              MIT OPEN-SOURCE LICENSE
            </div>
            <div style={{ fontSize: 24, color: "#E2E8F0", fontWeight: 700 }}>
              Maintained by browser-use team (@browser-use)
            </div>
            <div
              style={{
                display: "inline-block",
                marginTop: 24,
                padding: "10px 24px",
                borderRadius: 12,
                background: "rgba(255, 255, 255, 0.08)",
                border: "1px solid rgba(255, 255, 255, 0.2)",
                fontSize: 20,
                color: "#FFB703",
                fontFamily: "monospace",
              }}
            >
              github.com/browser-use/browser-use
            </div>
          </div>
        )}

        {/* SHOT 8: FLASH Brand End Card (744 - 840 frames | 24.80s - 28.00s) */}
        {shot === 8 && (
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              textAlign: "center",
            }}
          >
            {/* FLASH Official Brand Logo */}
            <div
              style={{
                width: 150,
                height: 150,
                borderRadius: "50%",
                overflow: "hidden",
                border: "3px solid #00E5FF",
                boxShadow: "0 0 40px rgba(0, 229, 255, 0.6), 0 0 60px rgba(255, 183, 3, 0.3)",
                marginBottom: 20,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                background: "#07090E",
              }}
            >
              <Img
                src={staticFile("assets/brand/logo.png")}
                style={{ width: "100%", height: "100%", objectFit: "cover" }}
              />
            </div>

            {/* Profile Avatar */}
            <div
              style={{
                width: 72,
                height: 72,
                borderRadius: "50%",
                overflow: "hidden",
                border: "2px solid rgba(255, 255, 255, 0.3)",
                marginBottom: 24,
              }}
            >
              <Img
                src={staticFile("assets/brand/profile.png")}
                style={{ width: "100%", height: "100%", objectFit: "cover" }}
              />
            </div>

            {/* Animated Follow Pill */}
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 12,
                padding: "14px 32px",
                borderRadius: 30,
                background: frame > 790 ? "#00E676" : "#00E5FF",
                color: "#040810",
                fontSize: 22,
                fontWeight: 900,
                letterSpacing: 1,
                boxShadow: "0 0 30px rgba(0, 229, 255, 0.5)",
                transform: `scale(${frame > 790 ? 1.05 : 1.0})`,
                transition: "all 0.2s ease",
              }}
            >
              <span>{frame > 790 ? "✓ Following" : "+ FOLLOW @flash__ai__digital"}</span>
            </div>

            <div
              style={{
                fontSize: 18,
                color: "#94A3B8",
                marginTop: 20,
                fontWeight: 600,
              }}
            >
              Daily AI and dev updates, with sources
            </div>
          </div>
        )}
      </div>

      {/* Render Subtitles */}
      {renderSubtitles()}
    </AbsoluteFill>
  );
};
