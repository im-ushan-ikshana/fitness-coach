import React, { useState } from "react";
import axios from "axios";
import "./App.css"; // ✅ Import the CSS file

// Import our separate components
import FormInput from "./components/FormInput";
import ResultDisplay from "./components/ResultDisplay";

function App() {
  // ------------------------
  // 1. State
  // ------------------------
  const [formData, setFormData] = useState({
    weight: "",
    height: "",
    gender: 0,
    age: "",
    hypertension: "No",
    diabetes: "No",
    fitness_goal: "",
    workout_preference: "",
    workout_location: "Gym",
    duration: "",
    experience_level: "",
  });

  const [loading, setLoading] = useState(false);
  const [sessionData, setSessionData] = useState(null); // Will hold the entire response from backend

  // ------------------------
  // 2. Handlers
  // ------------------------
  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post("http://127.0.0.1:8000/generate-workout", formData);
      setSessionData(response.data);
    } catch (error) {
      console.error("Error generating workout:", error);
      alert("An error occurred while generating the workout plan.");
    } finally {
      setLoading(false);
    }
  };

  const handleNewSession = () => {
    // Reset all data to start a new session
    setFormData({
      weight: "",
      height: "",
      gender: 0,
      age: "",
      hypertension: "No",
      diabetes: "No",
      fitness_goal: "",
      workout_preference: "",
      workout_location: "Gym",
      duration: "",
      experience_level: "",
    });
    setSessionData(null);
    setLoading(false);
  };

  // ------------------------
  // 3. Conditional Rendering
  // ------------------------

  // If we haven't received a workout plan yet, show the form
  if (!sessionData) {
    return (
      <div className="app-container">

        <div className="main-content">
          <h1>Generate Your Workout Plan</h1>
          <p>Fill out the form below to get a personalized workout and nutrition plan.</p>

          <FormInput
            formData={formData}
            loading={loading}
            onChange={handleChange}
            onSubmit={handleSubmit}
          />

          {loading && (
            <div className="loading-container">
              <p className="loading-text">Generating your plan... Please wait.</p>
            </div>
          )}
        </div>
      </div>
    );
  }

  // If we have sessionData, show the results
  return (
    <div className="app-container">
      <div className="main-content">
        <ResultDisplay
          sessionData={sessionData}
          onNewSession={handleNewSession}
        />
      </div>
    </div>
  );
}

export default App;
