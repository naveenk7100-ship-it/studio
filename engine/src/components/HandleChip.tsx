import React from "react";

export const HandleChip: React.FC = () => {
  return (
    <div
      style={{
        position: "absolute",
        top: 130,
        left: 50,
        display: "flex",
        alignItems: "center",
        gap: 12,
        padding: "10px 24px",
        borderRadius: 32,
        background: "rgba(7, 11, 20, 0.85)",
        border: "1.5px solid rgba(0, 240, 255, 0.45)",
        boxShadow: "0 0 20px rgba(0, 240, 255, 0.25)",
        zIndex: 50,
      }}
    >
      <svg
        width="22"
        height="22"
        viewBox="0 0 24 24"
        fill="#00f0ff"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path d="M13 2L3 14H12L11 22L21 10H12L13 2Z" />
      </svg>
      <span
        style={{
          fontFamily: "'Inter', sans-serif",
          fontWeight: 700,
          fontSize: 34,
          color: "#ffffff",
          letterSpacing: 0.5,
        }}
      >
        @flash__ai__digital
      </span>
    </div>
  );
};
