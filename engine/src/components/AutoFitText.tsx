import React from "react";

interface AutoFitTextProps {
  text: string;
  maxFontSize?: number;
  minFontSize?: number;
  color?: string;
  fontWeight?: number | string;
  textAlign?: "center" | "left" | "right";
  style?: React.CSSProperties;
}

export const AutoFitText: React.FC<AutoFitTextProps> = ({
  text,
  maxFontSize = 84,
  minFontSize = 46,
  color = "#ffffff",
  fontWeight = 900,
  textAlign = "center",
  style = {},
}) => {
  // Safety calculation: canvas width is 1080px.
  // Minimum margin requirement is 60px on both sides -> max width = 960px.
  const maxWidth = 960;
  
  // Approximate width per char for ultra-bold sans: ~0.62 * fontSize
  const charCount = text.length;
  let targetFontSize = maxFontSize;
  if (charCount > 0) {
    const estWidth = charCount * (maxFontSize * 0.58);
    if (estWidth > maxWidth) {
      targetFontSize = Math.max(minFontSize, Math.floor(maxWidth / (charCount * 0.58)));
    }
  }

  return (
    <div
      style={{
        maxWidth: 960,
        margin: "0 auto",
        fontSize: targetFontSize,
        fontWeight: fontWeight,
        color: color,
        textAlign: textAlign,
        lineHeight: 1.15,
        wordBreak: "break-word",
        boxSizing: "border-box",
        padding: "0 10px",
        ...style,
      }}
    >
      {text}
    </div>
  );
};
