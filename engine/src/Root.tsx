import React from "react";
import { Composition } from "remotion";
import { V7_Tools_PyPdfium2 } from "./compositions/V7_Tools_PyPdfium2";
import { V7_Discovery_HowChatGPTWorks } from "./compositions/V7_Discovery_HowChatGPTWorks";
import { PillarA_HowChatGPTWorks } from "./compositions/PillarA_HowChatGPTWorks";
import { PillarB_BestToolForJob } from "./compositions/PillarB_BestToolForJob";
import { StyleTest_VariantA } from "./compositions/StyleTest_VariantA";
import { StyleTest_VariantB } from "./compositions/StyleTest_VariantB";
import { StyleTest_VariantC } from "./compositions/StyleTest_VariantC";
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
      {/* FLASH SPEC V7 STAGE 1 PRODUCTIONS */}
      <Composition
        id="V7-Tools-PyPdfium2"
        component={V7_Tools_PyPdfium2}
        durationInFrames={1440}
        fps={30}
        width={720}
        height={1280}
      />
      <Composition
        id="V7-Discovery-HowChatGPTWorks"
        component={V7_Discovery_HowChatGPTWorks}
        durationInFrames={1500}
        fps={30}
        width={720}
        height={1280}
      />

      {/* V5 Content Overhaul Compositions (30.0s, 720x1280, 900 frames) */}
      <Composition
        id="PillarA-HowChatGPTWorks"
        component={PillarA_HowChatGPTWorks}
        durationInFrames={900}
        fps={30}
        width={720}
        height={1280}
      />
      <Composition
        id="PillarB-BestToolForJob"
        component={PillarB_BestToolForJob}
        durationInFrames={900}
        fps={30}
        width={720}
        height={1280}
      />

      {/* 12-Second Visual Overhaul Style Tests */}
      <Composition
        id="StyleTest-VariantA"
        component={StyleTest_VariantA}
        durationInFrames={360}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="StyleTest-VariantB"
        component={StyleTest_VariantB}
        durationInFrames={360}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="StyleTest-VariantC"
        component={StyleTest_VariantC}
        durationInFrames={360}
        fps={30}
        width={1080}
        height={1920}
      />

      {/* Production Daily Reels */}
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
