import React from "react";
import { Composition } from "remotion";
import { GoldenReel1_vLLM } from "./compositions/GoldenReel1_vLLM";
import { GoldenReel2_ClaudeCode } from "./compositions/GoldenReel2_ClaudeCode";
import { ShowcaseBumper } from "./compositions/ShowcaseBumper";
import { Golden30s_vLLM } from "./compositions/Golden30s_vLLM";
import { Golden30s_ClaudeCode } from "./compositions/Golden30s_ClaudeCode";
import { Golden30s_MCP } from "./compositions/Golden30s_MCP";

export const Root: React.FC = () => {
  return (
    <>
      <Composition
        id="ShowcaseBumper"
        component={ShowcaseBumper}
        durationInFrames={600}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="Golden30s-vLLM"
        component={Golden30s_vLLM}
        durationInFrames={840}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="Golden30s-ClaudeCode"
        component={Golden30s_ClaudeCode}
        durationInFrames={840}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="Golden30s-MCP"
        component={Golden30s_MCP}
        durationInFrames={840}
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
