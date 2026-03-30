"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";

interface QuestionGateProps {
  onComplete: (showPersonality: boolean) => void;
}

export default function QuestionGate({ onComplete }: QuestionGateProps) {
  const [question, setQuestion] = useState<string>("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(true);
  const [evaluating, setEvaluating] = useState(false);

  useEffect(() => {
    fetchQuestion();
  }, []);

  const fetchQuestion = async () => {
    try {
      const response = await fetch("/api/generate-question");
      const data = await response.json();
      setQuestion(data.question);
    } catch (error) {
      console.error("Failed to fetch question:", error);
      setQuestion(
        "If you could ask your future self one question, what would it be and why?"
      );
    } finally {
      setLoading(false);
    }
  };

  const handleSkip = () => {
    onComplete(false);
  };

  const handleSubmit = async () => {
    if (!answer.trim()) return;

    setEvaluating(true);
    try {
      const response = await fetch("/api/evaluate-answer", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question, answer }),
      });

      const data = await response.json();
      onComplete(data.showPersonality || false);
    } catch (error) {
      console.error("Failed to evaluate answer:", error);
      onComplete(false);
    }
  };

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-warm-cream text-xl"
        >
          Loading...
        </motion.div>
      </div>
    );
  }

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-gradient-to-br from-warm-terracotta/90 via-warm-sage/90 to-accent-gold/90 backdrop-blur-md z-50 flex items-center justify-center p-4"
      >
        <motion.div
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="bg-warm-cream rounded-2xl shadow-2xl max-w-2xl w-full p-8 md:p-12"
        >
          <motion.h2
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="text-2xl md:text-3xl font-bold text-gray-800 mb-6 text-center"
          >
            A Question for You
          </motion.h2>

          <motion.p
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="text-lg md:text-xl text-gray-700 mb-8 leading-relaxed text-center italic"
          >
            &ldquo;{question}&rdquo;
          </motion.p>

          <motion.textarea
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.5 }}
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            placeholder="Share your thoughts..."
            className="w-full h-40 p-4 border-2 border-warm-terracotta/30 rounded-lg focus:outline-none focus:border-warm-terracotta focus:ring-2 focus:ring-warm-terracotta/20 transition-all resize-none bg-white text-gray-800 placeholder-gray-400"
            disabled={evaluating}
          />

          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.6 }}
            className="flex flex-col sm:flex-row gap-4 mt-8"
          >
            <button
              onClick={handleSkip}
              disabled={evaluating}
              className="flex-1 px-6 py-3 border-2 border-gray-300 text-gray-600 rounded-lg hover:bg-gray-50 transition-all disabled:opacity-50 disabled:cursor-not-allowed font-medium"
            >
              Skip
            </button>
            <button
              onClick={handleSubmit}
              disabled={evaluating || !answer.trim()}
              className="flex-1 px-6 py-3 bg-warm-terracotta text-white rounded-lg hover:bg-warm-terracotta/90 transition-all disabled:opacity-50 disabled:cursor-not-allowed font-medium shadow-lg"
            >
              {evaluating ? "Evaluating..." : "Submit"}
            </button>
          </motion.div>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.7 }}
            className="text-sm text-gray-500 text-center mt-6"
          >
            Your answer helps us show you the right experience
          </motion.p>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}
