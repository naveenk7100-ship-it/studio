import React from "react";
import { Composition } from "remotion";
import { ShowcaseBumper } from "./compositions/ShowcaseBumper";
import { CinematicEssay_Unslop } from "./compositions/CinematicEssay_Unslop";
import { CinematicEssay_UV } from "./compositions/CinematicEssay_UV";
import { CinematicEssay_Kimi } from "./compositions/CinematicEssay_Kimi";
import { CinematicEssay_Craft } from "./compositions/CinematicEssay_Craft";
import { TodayReel_Anatomy } from "./compositions/TodayReel_Anatomy";
import { TodayReel_BrowserUse } from "./compositions/TodayReel_BrowserUse";

export const Root: React.FC = () => {
  return (
    <>
      <Composition
        id="TodayReel-Anatomy"
        component={TodayReel_Anatomy}
        durationInFrames={840}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="TodayReel-BrowserUse"
        component={TodayReel_BrowserUse}
        durationInFrames={840}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="ShowcaseBumper"
        component={ShowcaseBumper}
        durationInFrames={600}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="CinematicEssay-Unslop"
        component={CinematicEssay_Unslop}
        durationInFrames={840}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="CinematicEssay-UV"
        component={CinematicEssay_UV}
        durationInFrames={840}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="CinematicEssay-Kimi"
        component={CinematicEssay_Kimi}
        durationInFrames={840}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="CinematicEssay-Craft"
        component={CinematicEssay_Craft}
        durationInFrames={840}
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
