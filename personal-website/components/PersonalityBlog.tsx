"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { blogPosts, achievements, BlogPost } from "@/lib/blogData";

export default function PersonalityBlog() {
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<BlogPost[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [selectedPost, setSelectedPost] = useState<BlogPost | null>(null);

  useEffect(() => {
    const delaySearch = setTimeout(() => {
      if (searchQuery.trim()) {
        performSearch();
      } else {
        setSearchResults([]);
      }
    }, 500);

    return () => clearTimeout(delaySearch);
  }, [searchQuery]);

  const performSearch = async () => {
    setIsSearching(true);
    try {
      const response = await fetch("/api/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: searchQuery }),
      });

      const data = await response.json();
      setSearchResults(data.results || []);
    } catch (error) {
      console.error("Search failed:", error);
    } finally {
      setIsSearching(false);
    }
  };

  const displayPosts = searchQuery.trim() ? searchResults : blogPosts;

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 py-16 px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-6xl mx-auto"
      >
        {/* Header */}
        <motion.header
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-5xl md:text-7xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-pink-400 to-orange-400 mb-4">
            Welcome to the Real Me
          </h1>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            You made it here because you put in the effort. Here's where I share
            what I'm actually thinking about.
          </p>
        </motion.header>

        {/* Semantic Search */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="mb-12"
        >
          <div className="relative max-w-2xl mx-auto">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search my thoughts with semantic understanding..."
              className="w-full px-6 py-4 bg-white/10 backdrop-blur-md border-2 border-purple-400/30 rounded-full text-white placeholder-gray-400 focus:outline-none focus:border-purple-400 focus:ring-2 focus:ring-purple-400/20 transition-all"
            />
            {isSearching && (
              <div className="absolute right-6 top-1/2 -translate-y-1/2">
                <div className="animate-spin h-5 w-5 border-2 border-purple-400 border-t-transparent rounded-full" />
              </div>
            )}
          </div>
          {searchQuery && (
            <p className="text-center text-gray-400 mt-3 text-sm">
              Found {searchResults.length} relevant{" "}
              {searchResults.length === 1 ? "result" : "results"}
            </p>
          )}
        </motion.div>

        {/* Blog Posts Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-16">
          {displayPosts.map((post, index) => (
            <motion.article
              key={post.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              onClick={() => setSelectedPost(post)}
              className="bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl p-6 hover:bg-white/10 transition-all cursor-pointer group"
            >
              <div className="flex justify-between items-start mb-4">
                <h2 className="text-2xl font-bold text-white group-hover:text-purple-400 transition-colors">
                  {post.title}
                </h2>
                <span className="text-sm text-gray-400">{post.date}</span>
              </div>

              <p className="text-gray-300 mb-4 line-clamp-3">{post.content}</p>

              <div className="flex flex-wrap gap-2">
                {post.tags.map((tag) => (
                  <span
                    key={tag}
                    className="px-3 py-1 bg-purple-500/20 text-purple-300 rounded-full text-xs font-medium"
                  >
                    #{tag}
                  </span>
                ))}
              </div>
            </motion.article>
          ))}
        </div>

        {/* Achievements Section */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mb-16"
        >
          <h2 className="text-3xl font-bold text-white mb-8 text-center">
            Achievements I'm Proud Of
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {achievements.map((achievement, index) => (
              <motion.div
                key={achievement.id}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.5 + index * 0.1 }}
                className="bg-gradient-to-br from-orange-500/20 to-pink-500/20 backdrop-blur-md border border-orange-400/30 rounded-xl p-6"
              >
                <div className="text-4xl mb-3">🏆</div>
                <h3 className="text-lg font-bold text-white mb-2">
                  {achievement.title}
                </h3>
                <p className="text-gray-300 text-sm mb-3">
                  {achievement.content}
                </p>
                <span className="text-xs text-orange-400">
                  {achievement.date}
                </span>
              </motion.div>
            ))}
          </div>
        </motion.section>

        {/* Skills & Interests */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl p-8"
        >
          <h2 className="text-3xl font-bold text-white mb-6">
            What I'm Working With
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-xl font-semibold text-purple-400 mb-4">
                Tech Stack
              </h3>
              <div className="flex flex-wrap gap-2">
                {[
                  "Python",
                  "FastAPI",
                  "LLM Workflows",
                  "AI Agents",
                  "Neo4j",
                  "SQL",
                  "REST APIs",
                  "Workflow Automation",
                ].map((skill) => (
                  <span
                    key={skill}
                    className="px-3 py-1 bg-purple-500/20 text-purple-300 rounded-lg text-sm"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
            <div>
              <h3 className="text-xl font-semibold text-pink-400 mb-4">
                Superpowers
              </h3>
              <div className="flex flex-wrap gap-2">
                {[
                  "Translating Tech → Business",
                  "Solution Storytelling",
                  "Cross-functional Leadership",
                  "Data → Insights → Action",
                  "Process Optimization",
                  "Customer Enablement",
                ].map((skill) => (
                  <span
                    key={skill}
                    className="px-3 py-1 bg-pink-500/20 text-pink-300 rounded-lg text-sm"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </motion.section>
      </motion.div>

      {/* Modal for expanded post */}
      {selectedPost && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          onClick={() => setSelectedPost(null)}
          className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            onClick={(e) => e.stopPropagation()}
            className="bg-gradient-to-br from-gray-900 to-purple-900 border border-purple-400/30 rounded-2xl p-8 max-w-3xl w-full max-h-[80vh] overflow-y-auto"
          >
            <div className="flex justify-between items-start mb-6">
              <h2 className="text-3xl font-bold text-white">
                {selectedPost.title}
              </h2>
              <button
                onClick={() => setSelectedPost(null)}
                className="text-gray-400 hover:text-white text-2xl"
              >
                ×
              </button>
            </div>

            <p className="text-gray-400 mb-6">{selectedPost.date}</p>

            <div className="text-gray-200 whitespace-pre-wrap mb-6 leading-relaxed">
              {selectedPost.content}
            </div>

            <div className="flex flex-wrap gap-2">
              {selectedPost.tags.map((tag) => (
                <span
                  key={tag}
                  className="px-3 py-1 bg-purple-500/20 text-purple-300 rounded-full text-sm"
                >
                  #{tag}
                </span>
              ))}
            </div>
          </motion.div>
        </motion.div>
      )}
    </div>
  );
}
