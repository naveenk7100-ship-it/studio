import React from "react";
import { Composition } from "remotion";
import { ShowcaseBumper } from "./compositions/ShowcaseBumper";
import { NewEditorial_SuperAgent } from "./compositions/NewEditorial_SuperAgent";
import { NewEditorial_Ollama } from "./compositions/NewEditorial_Ollama";
import { NewEditorial_QwenNews } from "./compositions/NewEditorial_QwenNews";

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
        id="NewEditorial-SuperAgent"
        component={NewEditorial_SuperAgent}
        durationInFrames={840}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="NewEditorial-Ollama"
        component={NewEditorial_Ollama}
        durationInFrames={840}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="NewEditorial-QwenNews"
        component={NewEditorial_QwenNews}
        durationInFrames={840}
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
