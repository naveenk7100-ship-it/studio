import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
  Sequence,
} from "remotion";
import { BoltStrike } from "../components/BoltStrike";
import { FlashFrame } from "../components/FlashFrame";

export const ShowcaseBumper: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig(); // 600 frames = 20.00s

  // 120 BPM Beat Grid: 1 beat = 15 frames (0.5s), 1 bar = 60 frames (2.0s)
  const isDownbeat = frame % 30 === 0;

  // Camera punch-in on major beats
  const punchScale =
    frame >= 10 && frame < 525
      ? interpolate(frame % 60, [0, 6, 25, 60], [1.06, 1.0, 1.0, 1.0], {
          extrapolateRight: "clamp",
        })
      : 1.0;

  // Settle at end (frames 525 - 599): micro-breath scale (1.000 -> 1.012 -> 1.000)
  // At frame 599: sin(pi) = 0 -> settleScale = 1.000
  // At frame 0: settleScale = 1.000
  const settleScale =
    frame >= 525
      ? 1.0 + Math.sin(((frame - 525) / 74) * Math.PI) * 0.012
      : 1.0;

  const totalCameraScale = punchScale * settleScale;

  // Print misregistration on accent downbeats only (none on frame 0 or frame 599)
  const misreg =
    isDownbeat && frame >= 15 && frame < 525
      ? { x: frame % 4 === 0 ? 3 : -3, y: frame % 4 === 0 ? -2 : 2 }
      : { x: 0, y: 0 };

  const renderBrandLockup = () => (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        padding: 50,
      }}
    >
      <div
        style={{
          display: "inline-block",
          padding: "24px 44px",
          borderRadius: 36,
          background: "linear-gradient(135deg, #FF2D95 0%, #00E5FF 100%)",
          boxShadow:
            "0 0 60px rgba(0, 229, 255, 0.5), 0 0 80px rgba(255, 45, 149, 0.4)",
          textAlign: "center",
        }}
      >
        <div
          style={{
            fontSize: 52,
            fontWeight: 900,
            color: "#07080F",
            letterSpacing: 1.5,
            textTransform: "uppercase",
          }}
        >
          @FLASH__AI__DIGITAL
        </div>
      </div>

      <div
        style={{
          marginTop: 40,
          fontFamily: "'Courier New', monospace",
          fontSize: 28,
          color: "#00E5FF",
          letterSpacing: 4,
        }}
      >
        DAILY AI FOR BUILDERS
      </div>
    </div>
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#07080F",
        color: "#ffffff",
        fontFamily: "'Inter', sans-serif",
        overflow: "hidden",
      }}
    >
      {/* Background Cyber Grid */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          backgroundImage:
            "linear-gradient(rgba(0, 229, 255, 0.06) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 229, 255, 0.06) 1px, transparent 1px)",
          backgroundSize: "60px 60px",
          pointerEvents: "none",
        }}
      />

      {/* Signature Downbeat Lightning Flash on Major Transitions */}
      <FlashFrame triggerFrames={[10, 75, 180, 270, 360, 450, 525]} />
      <BoltStrike startFrame={10} />
      <BoltStrike startFrame={75} />
      <BoltStrike startFrame={270} />
      <BoltStrike startFrame={450} />

      {/* Camera Wrapper */}
      <div
        style={{
          width: "100%",
          height: "100%",
          transform: `scale(${totalCameraScale}) translate(${misreg.x}px, ${misreg.y}px)`,
          transformOrigin: "center center",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          position: "relative",
        }}
      >
        {/* FRAME 0 - 9 (0.0 - 0.3s): SEAMLESS LOOP LOCKUP (Identical to frame 599) */}
        <Sequence from={0} durationInFrames={10}>
          <AbsoluteFill
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            {renderBrandLockup()}
          </AbsoluteFill>
        </Sequence>

        {/* BEAT 1 (0.3 - 2.5s, Frames 10 - 75): STOP SCROLLING (Spring Slam from below) */}
        <Sequence from={10} durationInFrames={65}>
          <AbsoluteFill
            style={{
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
              padding: 60,
            }}
          >
            <div
              style={{
                fontFamily: "'Courier New', monospace",
                fontSize: 32,
                letterSpacing: 6,
                color: "#00E5FF",
                marginBottom: 30,
              }}
            >
              // REPOS
            </div>

            <div
              style={{
                fontSize: 104,
                fontWeight: 900,
                textAlign: "center",
                lineHeight: 1.05,
                color: "#FF2D95",
                textTransform: "uppercase",
                letterSpacing: 2,
                filter: "drop-shadow(0 0 45px rgba(255, 45, 149, 0.65))",
                transform: `scale(${interpolate(frame, [10, 25], [0.85, 1.0], { extrapolateRight: "clamp" })})`,
              }}
            >
              STOP<br />SCROLLING
            </div>

            <div
              style={{
                marginTop: 40,
                width: 240,
                height: 6,
                background: "#00E5FF",
                boxShadow: "0 0 20px #00E5FF",
              }}
            />
          </AbsoluteFill>
        </Sequence>

        {/* BEAT 2 (2.5 - 6.0s, Frames 75 - 180): AI MOVES DAILY */}
        <Sequence from={75} durationInFrames={105}>
          <AbsoluteFill
            style={{
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
              padding: 60,
            }}
          >
            <div
              style={{
                fontFamily: "'Courier New', monospace",
                fontSize: 32,
                letterSpacing: 6,
                color: "#FF2D95",
                marginBottom: 30,
              }}
            >
              // RELEASES
            </div>

            <div
              style={{
                fontSize: 96,
                fontWeight: 900,
                textAlign: "center",
                lineHeight: 1.1,
                color: "#FFFFFF",
                textTransform: "uppercase",
                letterSpacing: 1.5,
              }}
            >
              AI MOVES<br />
              <span style={{ color: "#00E5FF" }}>DAILY</span>
            </div>

            <div
              style={{
                marginTop: 35,
                padding: "14px 28px",
                borderRadius: 16,
                background: "rgba(0, 229, 255, 0.12)",
                border: "2px solid #00E5FF",
                color: "#00E5FF",
                fontSize: 32,
                fontWeight: 800,
              }}
            >
              0 COMMITS MISSED
            </div>
          </AbsoluteFill>
        </Sequence>

        {/* BEAT 3 (6.0 - 9.0s, Frames 180 - 270): MISS ONE */}
        <Sequence from={180} durationInFrames={90}>
          <AbsoluteFill
            style={{
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
              padding: 60,
            }}
          >
            <div
              style={{
                fontFamily: "'Courier New', monospace",
                fontSize: 32,
                letterSpacing: 6,
                color: "#00E5FF",
                marginBottom: 30,
              }}
            >
              // MCP
            </div>

            <div
              style={{
                fontSize: 108,
                fontWeight: 900,
                textAlign: "center",
                color: "#FF2D95",
                letterSpacing: 3,
                textTransform: "uppercase",
              }}
            >
              MISS ONE
            </div>
          </AbsoluteFill>
        </Sequence>

        {/* BEAT 4 (9.0 - 12.0s, Frames 270 - 360): MISS A LOT */}
        <Sequence from={270} durationInFrames={90}>
          <AbsoluteFill
            style={{
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
              padding: 60,
            }}
          >
            <div
              style={{
                fontFamily: "'Courier New', monospace",
                fontSize: 32,
                letterSpacing: 6,
                color: "#FF2D95",
                marginBottom: 30,
              }}
            >
              // CLAUDE CODE
            </div>

            <div
              style={{
                fontSize: 108,
                fontWeight: 900,
                textAlign: "center",
                color: "#00E5FF",
                letterSpacing: 3,
                textTransform: "uppercase",
                filter: "drop-shadow(0 0 45px rgba(0, 229, 255, 0.6))",
              }}
            >
              MISS A LOT
            </div>
          </AbsoluteFill>
        </Sequence>

        {/* BEAT 5 (12.0 - 15.0s, Frames 360 - 450): SOURCED. 30 SECONDS. */}
        <Sequence from={360} durationInFrames={90}>
          <AbsoluteFill
            style={{
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
              padding: 60,
            }}
          >
            <div
              style={{
                fontFamily: "'Courier New', monospace",
                fontSize: 32,
                letterSpacing: 6,
                color: "#00E5FF",
                marginBottom: 30,
              }}
            >
              // 30 SEC
            </div>

            <div
              style={{
                fontSize: 88,
                fontWeight: 900,
                textAlign: "center",
                lineHeight: 1.15,
                color: "#FFFFFF",
                textTransform: "uppercase",
              }}
            >
              SOURCED.<br />
              <span style={{ color: "#FF2D95" }}>30 SECONDS.</span>
            </div>

            <div
              style={{
                marginTop: 35,
                fontFamily: "'Courier New', monospace",
                fontSize: 28,
                color: "#8892b0",
              }}
            >
              README • DOCS • TELEMETRY
            </div>
          </AbsoluteFill>
        </Sequence>

        {/* BEAT 6 (15.0 - 17.5s, Frames 450 - 525): FOLLOW */}
        <Sequence from={450} durationInFrames={75}>
          <AbsoluteFill
            style={{
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
              padding: 60,
            }}
          >
            <div
              style={{
                fontFamily: "'Courier New', monospace",
                fontSize: 32,
                letterSpacing: 6,
                color: "#FF2D95",
                marginBottom: 30,
              }}
            >
              // SOURCES
            </div>

            <div
              style={{
                fontSize: 120,
                fontWeight: 900,
                textAlign: "center",
                color: "#00E5FF",
                letterSpacing: 6,
                textTransform: "uppercase",
                filter: "drop-shadow(0 0 50px rgba(0, 229, 255, 0.7))",
              }}
            >
              FOLLOW
            </div>
          </AbsoluteFill>
        </Sequence>

        {/* BEAT 7 (17.5 - 20.0s, Frames 525 - 600): @FLASH__AI__DIGITAL (Loop Lock) */}
        <Sequence from={525} durationInFrames={75}>
          <AbsoluteFill
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            {renderBrandLockup()}
          </AbsoluteFill>
        </Sequence>
      </div>

      {/* Corner Monospace Tech Framing */}
      <div
        style={{
          position: "absolute",
          top: 70,
          left: 60,
          fontFamily: "'Courier New', monospace",
          fontSize: 24,
          color: "rgba(0, 229, 255, 0.6)",
        }}
      >
        [00:00:20 // FLASH.Ai]
      </div>
      <div
        style={{
          position: "absolute",
          top: 70,
          right: 60,
          fontFamily: "'Courier New', monospace",
          fontSize: 24,
          color: "rgba(255, 45, 149, 0.6)",
        }}
      >
        BPM: 120 // 48kHz
      </div>
    </AbsoluteFill>
  );
};
