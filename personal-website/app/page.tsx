"use client";

import { useState } from "react";
import QuestionGate from "@/components/QuestionGate";
import ProfessionalTimeline from "@/components/ProfessionalTimeline";
import PersonalityBlog from "@/components/PersonalityBlog";

export default function Home() {
  const [showGate, setShowGate] = useState(true);
  const [showPersonality, setShowPersonality] = useState(false);

  const handleGateComplete = (personality: boolean) => {
    setShowPersonality(personality);
    setShowGate(false);
  };

  return (
    <main>
      {showGate && <QuestionGate onComplete={handleGateComplete} />}
      {!showGate && (
        <>
          {showPersonality ? <PersonalityBlog /> : <ProfessionalTimeline />}
        </>
      )}
    </main>
  );
}
