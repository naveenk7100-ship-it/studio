import React from "react";

export interface WordItem {
  word: string;
  start: number;
  end: number;
}

export interface StudioCaptionsProps {
  words: WordItem[];
  currentSec: number;
  accentColor?: string;
  endCardStartSec?: number;
}

export const StudioCaptions: React.FC<StudioCaptionsProps> = ({
  words,
  currentSec,
  accentColor = "#0284C7",
  endCardStartSec = 39.5,
}) => {
  if (!words || words.length === 0) return null;
  if (currentSec >= endCardStartSec) return null;

  // Find active word
  const activeIdx = words.findIndex(
    (w) => currentSec >= w.start && currentSec <= w.end
  );

  if (activeIdx === -1) return null;

  // Window of 3-4 words (1 before, current, 1-2 after)
  const startIdx = Math.max(0, activeIdx - 1);
  const endIdx = Math.min(words.length, activeIdx + 3);
  const slice = words.slice(startIdx, endIdx);
  const activeWord = words[activeIdx].word;

  return (
    <div
      style={{
        position: "absolute",
        bottom: 165,
        left: 55, // 7.6% margin from edge (guarantees >= 5% audit rule)
        right: 55,
        textAlign: "center",
        zIndex: 100,
        display: "flex",
        justifyContent: "center",
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          backgroundColor: "rgba(10, 20, 36, 0.92)",
          border: "1.5px solid rgba(0, 240, 255, 0.35)",
          borderRadius: 22,
          padding: "10px 24px",
          boxShadow: `
            0 12px 32px -6px rgba(0, 0, 0, 0.4),
            0 0 16px rgba(0, 240, 255, 0.15)
          `,
          backdropFilter: "blur(16px)",
          display: "flex",
          gap: 12,
          alignItems: "center",
          maxWidth: 580,
          flexWrap: "wrap",
          justifyContent: "center",
        }}
      >
        {slice.map((item, idx) => {
          const isCurrent = item.word === activeWord;
          return (
            <span
              key={idx}
              style={{
                fontSize: 46,
                fontWeight: isCurrent ? 900 : 700,
                color: isCurrent ? "#FFFFFF" : "rgba(255, 255, 255, 0.65)",
                backgroundColor: isCurrent ? "rgba(0, 240, 255, 0.22)" : "transparent",
                border: isCurrent ? `1.5px solid ${accentColor}` : "1.5px solid transparent",
                padding: "2px 10px",
                borderRadius: 10,
                transition: "all 0.1s ease-out",
                letterSpacing: "-0.5px",
                textShadow: isCurrent ? "0 0 12px rgba(0, 240, 255, 0.5)" : "none",
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
