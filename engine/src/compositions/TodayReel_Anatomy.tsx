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
import wordsData from "../../../cache/words_final_today_1_anatomy.json";

export const TodayReel_Anatomy: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  // Sentence-derived Narrative Visual Beats across 840 frames (28.00s @ 30fps)
  // Shot 1: 0 - 98 (0.00s - 3.28s) Cover Lockup: Anatomy - Claude Code Skill
  // Shot 2: 98 - 190 (3.28s - 6.36s) Concept & Installation: npx skills add wheresryan22/anatomy
  // Shot 3: 190 - 341 (6.36s - 11.40s) Hero Visual 1: Raptor 2 Engine Test Stand (Real WebGL/SVG Figure)
  // Shot 4: 341 - 472 (11.40s - 15.76s) Usage & Slash Command: /anatomy <one-line idea>
  // Shot 5: 472 - 584 (15.76s - 19.48s) Hero Visual 2: Raptor 2 Deconstructed Assembly
  // Shot 6: 584 - 662 (19.48s - 22.10s) GitHub Stars: 25,676 Stars
  // Shot 7: 662 - 744 (22.10s - 24.80s) Source & License: Ryan (@wheresryan22) • MIT License
  // Shot 8: 744 - 840 (24.80s - 28.00s) FLASH Brand End Card

  const shot =
    frame < 98
      ? 1
      : frame < 190
      ? 2
      : frame < 341
      ? 3
      : frame < 472
      ? 4
      : frame < 584
      ? 5
      : frame < 662
      ? 6
      : frame < 744
      ? 7
      : 8;

  const shotRel =
    shot === 1
      ? frame
      : shot === 2
      ? frame - 98
      : shot === 3
      ? frame - 190
      : shot === 4
      ? frame - 341
      : shot === 5
      ? frame - 472
      : shot === 6
      ? frame - 584
      : shot === 7
      ? frame - 662
      : frame - 744;

  // CONTINUOUS ACTIVE MOTION DERIVED FROM SENTENCE TIMELINE
  const camZoom = 1.0 + (frame / 840) * 0.10;
  const camPanX = Math.sin(frame * 0.05) * 14;
  const camPanY = Math.cos(frame * 0.04) * 10;

  // Distinct transitions at each sentence cut point
  const cutFrames = [98, 190, 341, 472, 584, 662, 744];
  const distToCut = Math.min(...cutFrames.map((cf) => Math.abs(frame - cf)));
  const transitionFlash =
    distToCut === 0 ? 0.70 : distToCut === 1 ? 0.35 : distToCut === 2 ? 0.12 : 0;
  const transitionWhipX = distToCut === 0 ? 45 : distToCut === 1 ? 18 : 0;

  // Technical ambient grid scan line
  const scanLineY = (frame * 14) % height;
  const gridShiftY = (frame * 3) % 50;

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
                color: isCurrent ? "#00E5FF" : "#FFFFFF",
                textShadow: isCurrent
                  ? "0 0 25px rgba(0, 229, 255, 0.8), 0 2px 10px rgba(0,0,0,0.9)"
                  : "0 2px 8px rgba(0,0,0,0.8)",
                background: isCurrent ? "rgba(0, 229, 255, 0.15)" : "transparent",
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
      {/* Background Animated Technical Grid */}
      <div
        style={{
          position: "absolute",
          inset: -100,
          backgroundImage: `linear-gradient(to right, rgba(0, 229, 255, 0.05) 1px, transparent 1px),
                            linear-gradient(to bottom, rgba(0, 229, 255, 0.05) 1px, transparent 1px)`,
          backgroundSize: "50px 50px",
          transform: `translateY(${gridShiftY}px)`,
          opacity: 0.8,
        }}
      />

      {/* Ambient Radial Cyan Glow */}
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
            "radial-gradient(circle, rgba(0, 229, 255, 0.14) 0%, transparent 70%)",
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
            "linear-gradient(90deg, transparent, rgba(0, 229, 255, 0.6), transparent)",
          boxShadow: "0 0 15px rgba(0, 229, 255, 0.8)",
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
              backgroundColor: "#00E5FF",
              boxShadow: "0 0 12px #00E5FF",
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
            FLASH ARCHITECTURE
          </span>
        </div>
        <div
          style={{
            padding: "6px 14px",
            borderRadius: 20,
            background: "rgba(0, 229, 255, 0.12)",
            border: "1px solid rgba(0, 229, 255, 0.3)",
            fontSize: 16,
            fontWeight: 700,
            color: "#00E5FF",
          }}
        >
          CLAUDE CODE SKILL
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
          transform: `scale(${camZoom}) translate(${camPanX + transitionWhipX}px, ${camPanY}px)`,
          padding: "160px 60px",
          zIndex: 50,
        }}
      >
        {/* SHOT 1: Cover Lockup (0 - 98 frames | 0.0s - 3.28s) */}
        {shot === 1 && (
          <div style={{ textAlign: "center", maxWidth: 960 }}>
            <div
              style={{
                display: "inline-block",
                padding: "8px 20px",
                borderRadius: 20,
                background: "rgba(0, 229, 255, 0.15)",
                border: "1px solid #00E5FF",
                fontSize: 18,
                fontWeight: 800,
                color: "#00E5FF",
                letterSpacing: 2,
                marginBottom: 24,
                textTransform: "uppercase",
              }}
            >
              PHYSICAL MACHINE BLUEPRINTS
            </div>
            <div
              style={{
                fontSize: 90,
                fontWeight: 900,
                letterSpacing: -2,
                lineHeight: 1.05,
                background: "linear-gradient(180deg, #FFFFFF 0%, #94A3B8 100%)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
                marginBottom: 24,
              }}
            >
              Anatomy
            </div>
            <div
              style={{
                fontSize: 32,
                color: "#E2E8F0",
                lineHeight: 1.4,
                fontWeight: 600,
              }}
            >
              Explains ideas by building them as real working objects
            </div>
          </div>
        )}

        {/* SHOT 2: Concept & Installation (98 - 190 frames | 3.28s - 6.36s) */}
        {shot === 2 && (
          <div style={{ width: "100%", maxWidth: 880 }}>
            <div
              style={{
                fontSize: 18,
                fontWeight: 800,
                color: "#00E5FF",
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
                border: "1px solid rgba(0, 229, 255, 0.4)",
                borderRadius: 18,
                padding: 32,
                boxShadow: "0 20px 50px rgba(0,0,0,0.8)",
              }}
            >
              <div style={{ display: "flex", gap: 10, marginBottom: 20 }}>
                <div style={{ width: 14, height: 14, borderRadius: "50%", background: "#FF5F56" }} />
                <div style={{ width: 14, height: 14, borderRadius: "50%", background: "#FFBD2E" }} />
                <div style={{ width: 14, height: 14, borderRadius: "50%", background: "#27C93F" }} />
                <div style={{ fontSize: 16, color: "#94A3B8", marginLeft: 10, fontFamily: "monospace" }}>bash</div>
              </div>
              <div style={{ fontFamily: "monospace", fontSize: 28, color: "#38BDF8", lineHeight: 1.6 }}>
                <div>$ npx skills add wheresryan22/anatomy</div>
              </div>
              <div style={{ color: "#E2E8F0", marginTop: 20, fontSize: 20, lineHeight: 1.5 }}>
                Zero dependencies. Runs in Claude Code, Antigravity, OpenCode, and Codex.
              </div>
            </div>
          </div>
        )}

        {/* SHOT 3: HERO VISUAL 1 - Real Raptor 2 Engine Figure (190 - 341 frames | 6.36s - 11.40s) */}
        {shot === 3 && (
          <div style={{ width: "100%", maxWidth: 900, textAlign: "center" }}>
            <div
              style={{
                fontSize: 16,
                fontWeight: 800,
                color: "#00E5FF",
                letterSpacing: 2,
                marginBottom: 16,
                textTransform: "uppercase",
              }}
            >
              ISOMETRIC SYSTEM FIGURE
            </div>
            {/* Hero Visual >= 45% frame height (880px height in 1920) */}
            <div
              style={{
                width: "100%",
                height: 880,
                borderRadius: 24,
                overflow: "hidden",
                border: "2px solid rgba(0, 229, 255, 0.5)",
                boxShadow: "0 0 60px rgba(0, 229, 255, 0.25)",
                background: "#0F172A",
                position: "relative",
              }}
            >
              <Img
                src={staticFile("captured_proofs/wheresryan22_anatomy/raptor-engine-firing.webp")}
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
                Fig 1: Raptor 2 Test Stand • SVG Apparatus with WebGL Plume Shader
              </div>
            </div>
          </div>
        )}

        {/* SHOT 4: Usage & Slash Command (341 - 472 frames | 11.40s - 15.76s) */}
        {shot === 4 && (
          <div style={{ width: "100%", maxWidth: 880 }}>
            <div
              style={{
                fontSize: 18,
                fontWeight: 800,
                color: "#00E5FF",
                letterSpacing: 2,
                marginBottom: 16,
                textTransform: "uppercase",
              }}
            >
              CLAUDE COMMAND
            </div>
            <div
              style={{
                background: "#04060A",
                border: "2px solid #00E5FF",
                borderRadius: 20,
                padding: 36,
                boxShadow: "0 0 40px rgba(0, 229, 255, 0.3)",
              }}
            >
              <div style={{ fontFamily: "monospace", fontSize: 26, color: "#00E5FF", fontWeight: 800, lineHeight: 1.4 }}>
                &gt; /anatomy explain token bucket rate limiter, interactive
              </div>
              <div style={{ fontSize: 20, color: "#E2E8F0", marginTop: 20, lineHeight: 1.5 }}>
                Invents a physical mechanical apparatus representing your idea in SVG, WebGL, or 3D.
              </div>
            </div>
          </div>
        )}

        {/* SHOT 5: HERO VISUAL 2 - Deconstructed Parts Assembly (472 - 584 frames | 15.76s - 19.48s) */}
        {shot === 5 && (
          <div style={{ width: "100%", maxWidth: 900, textAlign: "center" }}>
            <div
              style={{
                fontSize: 16,
                fontWeight: 800,
                color: "#00E5FF",
                letterSpacing: 2,
                marginBottom: 16,
                textTransform: "uppercase",
              }}
            >
              MULTI-PART DECONSTRUCTION
            </div>
            {/* Hero Visual >= 45% frame height */}
            <div
              style={{
                width: "100%",
                height: 880,
                borderRadius: 24,
                overflow: "hidden",
                border: "2px solid rgba(0, 229, 255, 0.5)",
                boxShadow: "0 0 60px rgba(0, 229, 255, 0.25)",
                background: "#0F172A",
                position: "relative",
              }}
            >
              <Img
                src={staticFile("captured_proofs/wheresryan22_anatomy/raptor-engine-apart.webp")}
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
                11 Independent Assemblies • Hover to explode view with zero pipe collision
              </div>
            </div>
          </div>
        )}

        {/* SHOT 6: GitHub Stars (584 - 662 frames | 19.48s - 22.10s) */}
        {shot === 6 && (
          <div style={{ textAlign: "center" }}>
            <div
              style={{
                fontSize: 18,
                fontWeight: 800,
                color: "#00E5FF",
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
                textShadow: "0 0 50px rgba(0, 229, 255, 0.6)",
                lineHeight: 1,
              }}
            >
              25,676
            </div>
            <div
              style={{
                fontSize: 32,
                fontWeight: 800,
                color: "#00E5FF",
                marginTop: 12,
                letterSpacing: 2,
              }}
            >
              STARS REACHED
            </div>
          </div>
        )}

        {/* SHOT 7: MIT License & Author Grounding (662 - 744 frames | 22.10s - 24.80s) */}
        {shot === 7 && (
          <div style={{ textAlign: "center", maxWidth: 800 }}>
            <div
              style={{
                fontSize: 16,
                fontWeight: 800,
                color: "#00E5FF",
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
              Created by Ryan (@wheresryan22)
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
                color: "#00E5FF",
                fontFamily: "monospace",
              }}
            >
              github.com/wheresryan22/anatomy
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
                boxShadow: "0 0 40px rgba(0, 229, 255, 0.6), 0 0 60px rgba(255, 45, 149, 0.3)",
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
