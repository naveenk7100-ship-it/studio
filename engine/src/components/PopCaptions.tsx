import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";

export interface WordItem {
  word: string;
  start: number; // in seconds
  end: number;   // in seconds
}

interface PopCaptionsProps {
  words: [string, number, number][];
}

export const PopCaptions: React.FC<PopCaptionsProps> = ({ words }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentTime = frame / fps;

  // 1. Group into chunks of 3 words
  const chunks: WordItem[][] = [];
  for (let i = 0; i < words.length; i += 3) {
    const group = words.slice(i, i + 3).map(([w, s, e]) => ({
      word: w,
      start: s,
      end: e,
    }));
    chunks.push(group);
  }

  // 2. Find active chunk
  let activeChunk: WordItem[] | null = null;
  for (const chunk of chunks) {
    const chunkStart = chunk[0].start;
    const chunkEnd = chunk[chunk.length - 1].end;
    if (currentTime >= chunkStart - 0.1 && currentTime <= chunkEnd + 0.3) {
      activeChunk = chunk;
      break;
    }
  }

  if (!activeChunk) return null;

  return (
    <div
      style={{
        position: "absolute",
        top: 1360, // Reserved Caption Zone (strictly 1360 - 1480px; above bottom 380px safe zone)
        left: 60,
        right: 60,
        height: 110,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 100,
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: 16,
          padding: "16px 36px",
          borderRadius: 24,
          background: "rgba(7, 11, 20, 0.92)",
          border: "2px solid rgba(0, 229, 255, 0.5)",
          boxShadow: "0 10px 40px rgba(0, 0, 0, 0.9)",
          maxWidth: 960,
        }}
      >
        {activeChunk.map((w, idx) => {
          const isActive = currentTime >= w.start && currentTime <= w.end;
          return (
            <React.Fragment key={idx}>
              <span
                style={{
                  fontFamily: "'Inter', sans-serif",
                  fontWeight: 900,
                  fontSize: 50,
                  color: isActive ? "#ffd700" : "#ffffff",
                  transform: isActive ? "scale(1.14)" : "scale(1.0)",
                  textShadow: isActive
                    ? "0 0 25px rgba(255, 215, 0, 0.85)"
                    : "0 2px 8px rgba(0,0,0,0.8)",
                  display: "inline-block",
                  letterSpacing: "0.5px",
                }}
              >
                {w.word}
              </span>
              {/* Guaranteed space between words to prevent OCR/render merging */}
              {idx < activeChunk.length - 1 && <span style={{ width: 14 }} />}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};
