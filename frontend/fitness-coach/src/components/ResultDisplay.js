import React, { useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import "./ResultDisplay.css";

function ResultDisplay({ sessionData, onNewSession, onExerciseSelect }) {
  const workoutRef = useRef(null);

  useEffect(() => {
    if (workoutRef.current && onExerciseSelect) {
      // Add null check for onExerciseSelect
      const tables = workoutRef.current.getElementsByTagName("table");
      Array.from(tables).forEach((table) => {
        const rows = table.getElementsByTagName("tr");
        // Skip header row
        for (let i = 1; i < rows.length; i++) {
          const row = rows[i];
          const exerciseCell = row.cells[1];
          if (exerciseCell) {
            row.classList.add("clickable-row");
            row.addEventListener("click", () => {
              // Remove highlight from all rows
              Array.from(rows).forEach((r) =>
                r.classList.remove("selected-row")
              );
              // Add highlight to clicked row
              row.classList.add("selected-row");
              // Call the handler with the exercise name
              onExerciseSelect(exerciseCell.textContent.trim());
            });
          }
        }
      });
    }
  }, [sessionData, onExerciseSelect]);

  return (
    <div className="result-container">
      {/* Header with Session ID and New Session button */}
      <header className="result-header">
        <h2 className="session-id">Session ID: {sessionData.session_id}</h2>
        <button className="new-session-button" onClick={onNewSession}>
          New Chat
        </button>
      </header>

      {/* Basic Info */}
      <div className="info-section">
        <p>
          <strong>Your BMI:</strong> {sessionData.bmi}
        </p>
        <p>
          <strong>Recommendation Level:</strong>{" "}
          {sessionData.recommendation_level}
        </p>
      </div>

      {/* Fitness Analysis */}
      <section className="markdown-section">
        <ReactMarkdown
          className="markdown-content"
          remarkPlugins={[remarkGfm]}
          rehypePlugins={[rehypeRaw]}
        >
          {sessionData.fitness_analysis}
        </ReactMarkdown>
      </section>

      {/* Workout Plan */}
      <section className="markdown-section" ref={workoutRef}>
        <h3>Workout Plan</h3>
        <p className="table-instruction">
          Click on any exercise to see video demonstrations
        </p>
        <ReactMarkdown
          className="markdown-content"
          remarkPlugins={[remarkGfm]}
          rehypePlugins={[rehypeRaw]}
        >
          {sessionData.workout_plan}
        </ReactMarkdown>
      </section>

      {/* Nutrition Tips */}
      <section className="markdown-section">
        <h3>Nutrition Tips</h3>
        <ReactMarkdown
          className="markdown-content"
          remarkPlugins={[remarkGfm]}
          rehypePlugins={[rehypeRaw]}
        >
          {sessionData.nutrition_tips}
        </ReactMarkdown>
      </section>
    </div>
  );
}

export default ResultDisplay;
