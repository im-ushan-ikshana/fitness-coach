import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./ResultDisplay.css"; // ✅ Import CSS file for styling

function ResultDisplay({ sessionData, onNewSession }) {
  return (
    <div className="result-container">
      {/* Header with Session ID and New Session button */}
      <header className="result-header">
        <h2 className="session-id">Session ID: {sessionData.session_id}</h2>
        <button className="new-session-button" onClick={onNewSession}>New Chat</button>
      </header>

      {/* Basic Info */}
      <div className="info-section">
        <p><strong>Your BMI:</strong> {sessionData.bmi}</p>
        <p><strong>Recommendation Level:</strong> {sessionData.recommendation_level}</p>
      </div>

      {/* Fitness Analysis */}
      <section className="markdown-section">
        <ReactMarkdown className="markdown-content" remarkPlugins={[remarkGfm]}>
          {sessionData.fitness_analysis}
        </ReactMarkdown>
      </section>

      {/* Workout Plan */}
      <section className="markdown-section">
        <h3>Workout Plan</h3>
        <ReactMarkdown className="markdown-content" remarkPlugins={[remarkGfm]}>
          {sessionData.workout_plan}
        </ReactMarkdown>
      </section>

      {/* Nutrition Tips */}
      <section className="markdown-section">
        <h3>Nutrition Tips</h3>
        <ReactMarkdown className="markdown-content" remarkPlugins={[remarkGfm]}>
          {sessionData.nutrition_tips}
        </ReactMarkdown>
      </section>
    </div>
  );
}

export default ResultDisplay;
