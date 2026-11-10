import React from "react";
import { AbsoluteFill, Sequence, useCurrentFrame } from "remotion";
import { Document3DView } from "../components/visuals/Document3DView";
import { BoundingBoxOverlay } from "../components/visuals/BoundingBoxOverlay";
import { AttentionFlowGraph } from "../components/visuals/AttentionFlowGraph";
import { ProbabilityBarChart } from "../components/visuals/ProbabilityBarChart";

export const VisualIntelligence_Preview: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#050914",
        color: "#FFFFFF",
        fontFamily: "'Inter', sans-serif",
      }}
    >
      {/* SCENE 1: Document3DView with BoundingBoxOverlay (Frames 0 - 120) */}
      <Sequence from={0} durationInFrames={120} name="Document3D & BoundingBoxes">
        <Document3DView
          title="Attention Is All You Need"
          paperId="arXiv:1706.03762"
          pageNumber={1}
          totalPages={15}
        >
          <BoundingBoxOverlay
            containerWidth={580}
            containerHeight={750}
            scanDurationFrames={90}
            showCoordinatesTag={true}
            showBlockCounter={true}
          />
        </Document3DView>
      </Sequence>

      {/* SCENE 2: AttentionFlowGraph (Frames 120 - 240) */}
      <Sequence from={120} durationInFrames={120} name="AttentionFlowGraph">
        <div
          style={{
            width: "100%",
            height: "100%",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <AttentionFlowGraph
            layer={11}
            head={0}
            targetTokenIdx={5}
            flowSpeed={1.2}
            width={680}
            height={780}
          />
        </div>
      </Sequence>

      {/* SCENE 3: ProbabilityBarChart (Frames 240 - 360) */}
      <Sequence from={240} durationInFrames={120} name="ProbabilityBarChart">
        <div
          style={{
            width: "100%",
            height: "100%",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <ProbabilityBarChart
            promptText="The future of artificial intelligence is"
            width={680}
            height={780}
            highlightTop={true}
          />
        </div>
      </Sequence>
    </AbsoluteFill>
  );
};
