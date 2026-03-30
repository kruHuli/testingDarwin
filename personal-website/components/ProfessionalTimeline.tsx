"use client";

import { motion } from "framer-motion";
import { useState } from "react";

interface TimelineItem {
  id: string;
  date: string;
  title: string;
  subtitle?: string;
  organization: string;
  location: string;
  description: string[];
  type: "work" | "education" | "award" | "project";
  icon: string;
}

const timelineData: TimelineItem[] = [
  {
    id: "1",
    date: "Jan 2026",
    title: "AI Platform - Receipted",
    organization: "Personal Project",
    location: "Remote",
    type: "project",
    icon: "🚀",
    description: [
      "Built an AI platform that converts user experience stories into structured, verifiable skill profiles using FastAPI and Neo4j",
      "Delivered live product demonstrations at the Continual Learning Hackathon SF",
    ],
  },
  {
    id: "2",
    date: "Oct 2025 - Jan 2026",
    title: "AI Engineer",
    organization: "AdvantageGEO",
    location: "Remote",
    type: "work",
    icon: "💼",
    description: [
      "Partnered with technical and business stakeholders to translate requirements into implementation steps",
      "Built demo environments to showcase workflow capabilities and support technical adoption decisions",
    ],
  },
  {
    id: "3",
    date: "Sep 2023 - Dec 2023",
    title: "Team Lead and Analyst, Retail Analytics",
    subtitle: "Fellowship Award for Outstanding Team Lead",
    organization: "Philadelphia Phillies via Rutgers MBS Externship",
    location: "New Brunswick, NJ",
    type: "award",
    icon: "🏆",
    description: [
      "Led a 5-person cross-functional team delivering analytics insights from 750k+ transactions",
      "Developed executive presentations summarizing data-driven and model-supported insights",
      "Built Tableau dashboards used by stakeholders to monitor KPIs",
    ],
  },
  {
    id: "4",
    date: "Jun 2024 - Aug 2024",
    title: "AI Product Analyst Intern",
    organization: "Eltropy Inc.",
    location: "Santa Clara, CA",
    type: "work",
    icon: "💡",
    description: [
      "Analyzed 50k+ customer conversations to identify product improvement opportunities",
      "Partnered with product and HR teams to implement GenAI-driven onboarding, reducing procedures by 50%",
      "Built Sankey visualizations to help customers understand product usage patterns",
    ],
  },
  {
    id: "5",
    date: "Sep 2021 - May 2025",
    title: "Intramural Sports Team Lead, Strategy Intern, Manager, Supervisor, Referee",
    subtitle: "Rutgers University Recreation Leadership Excellence Award 2023",
    organization: "Rutgers Recreation",
    location: "New Brunswick, NJ",
    type: "award",
    icon: "⭐",
    description: [
      "Led technical onboarding for 100+ referees, translating complex rule systems into operational workflows",
      "Redesigned operational workflows across 60+ staff to improve coordination and reduce execution delays",
      "Identified process inefficiencies and redesigned officiating structure, improving operational efficiency by 33%",
    ],
  },
  {
    id: "6",
    date: "Expected May 2026",
    title: "Master's in Business Analytics",
    organization: "Rutgers University - Rutgers Professional Science Master's Program",
    location: "New Brunswick, NJ",
    type: "education",
    icon: "🎓",
    description: [
      "Focus: AI and Analytics",
    ],
  },
  {
    id: "7",
    date: "Expected May 2026",
    title: "Bachelor's in Business Analytics and Information Technologies",
    subtitle: "Leadership Skills Concentration",
    organization: "Rutgers University - Rutgers Business School",
    location: "New Brunswick, NJ",
    type: "education",
    icon: "🎓",
    description: [],
  },
];

export default function ProfessionalTimeline() {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const getTypeColor = (type: TimelineItem["type"]) => {
    switch (type) {
      case "work":
        return "bg-warm-terracotta";
      case "education":
        return "bg-warm-sage";
      case "award":
        return "bg-accent-gold";
      case "project":
        return "bg-warm-terracotta";
      default:
        return "bg-gray-400";
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-warm-cream via-warm-beige to-warm-cream py-16 px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-5xl mx-auto"
      >
        <motion.header
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <h1 className="text-5xl md:text-6xl font-bold text-gray-800 mb-4">
            Professional Journey
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Technology consulting analyst with experience in AI, analytics, and
            operational excellence
          </p>
        </motion.header>

        <div className="relative">
          {/* Timeline line */}
          <div className="absolute left-8 md:left-1/2 top-0 bottom-0 w-0.5 bg-gradient-to-b from-warm-terracotta via-warm-sage to-accent-gold" />

          {timelineData.map((item, index) => (
            <motion.div
              key={item.id}
              initial={{ opacity: 0, x: index % 2 === 0 ? -50 : 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className={`relative mb-12 ${
                index % 2 === 0
                  ? "md:pr-1/2 md:text-right"
                  : "md:pl-1/2 md:ml-auto"
              }`}
            >
              {/* Timeline dot */}
              <div
                className={`absolute left-8 md:left-1/2 -ml-4 w-8 h-8 rounded-full ${getTypeColor(
                  item.type
                )} border-4 border-warm-cream flex items-center justify-center text-lg z-10 shadow-lg`}
              >
                {item.icon}
              </div>

              {/* Content card */}
              <motion.div
                whileHover={{ scale: 1.02 }}
                onClick={() =>
                  setExpandedId(expandedId === item.id ? null : item.id)
                }
                className={`ml-20 md:ml-0 ${
                  index % 2 === 0 ? "md:mr-16" : "md:ml-16"
                } cursor-pointer`}
              >
                <div
                  className={`bg-white rounded-xl shadow-lg p-6 border-l-4 ${
                    item.type === "award"
                      ? "border-accent-gold"
                      : item.type === "education"
                      ? "border-warm-sage"
                      : "border-warm-terracotta"
                  } hover:shadow-xl transition-all`}
                >
                  <div className="flex justify-between items-start mb-2">
                    <span className="text-sm font-semibold text-warm-terracotta">
                      {item.date}
                    </span>
                    <span className="text-xs text-gray-500">{item.location}</span>
                  </div>

                  <h3 className="text-xl font-bold text-gray-800 mb-1">
                    {item.title}
                  </h3>

                  {item.subtitle && (
                    <p className="text-sm font-semibold text-accent-gold mb-2 flex items-center gap-1">
                      {item.type === "award" && "🏆"} {item.subtitle}
                    </p>
                  )}

                  <p className="text-gray-600 font-medium mb-3">
                    {item.organization}
                  </p>

                  <motion.div
                    initial={false}
                    animate={{
                      height: expandedId === item.id ? "auto" : "0px",
                      opacity: expandedId === item.id ? 1 : 0,
                    }}
                    className="overflow-hidden"
                  >
                    <ul className="space-y-2 mt-4">
                      {item.description.map((desc, idx) => (
                        <li
                          key={idx}
                          className="text-gray-700 text-sm leading-relaxed flex items-start gap-2"
                        >
                          <span className="text-warm-terracotta mt-1">•</span>
                          <span>{desc}</span>
                        </li>
                      ))}
                    </ul>
                  </motion.div>

                  {item.description.length > 0 && (
                    <button className="text-xs text-warm-terracotta mt-3 hover:underline">
                      {expandedId === item.id ? "Show less" : "Show more"}
                    </button>
                  )}
                </div>
              </motion.div>
            </motion.div>
          ))}
        </div>

        {/* Skills section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="mt-16 bg-white rounded-2xl shadow-lg p-8"
        >
          <h2 className="text-3xl font-bold text-gray-800 mb-6">Skills</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-lg font-semibold text-warm-terracotta mb-3">
                Technical
              </h3>
              <div className="flex flex-wrap gap-2">
                {[
                  "Python",
                  "REST APIs",
                  "FastAPI",
                  "SQL",
                  "Neo4j",
                  "LLM workflows",
                  "AI agents",
                  "Workflow automation",
                ].map((skill) => (
                  <span
                    key={skill}
                    className="px-3 py-1 bg-warm-terracotta/10 text-warm-terracotta rounded-full text-sm font-medium"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-warm-sage mb-3">
                Consulting
              </h3>
              <div className="flex flex-wrap gap-2">
                {[
                  "Technical discovery",
                  "Solution architecture",
                  "Technical demos",
                  "Stakeholder presentations",
                  "Integration design",
                  "Customer enablement",
                  "Solution storytelling",
                  "Cross-functional execution",
                  "Requirements gathering",
                  "Process optimization",
                ].map((skill) => (
                  <span
                    key={skill}
                    className="px-3 py-1 bg-warm-sage/10 text-warm-sage rounded-full text-sm font-medium"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </div>
  );
}
