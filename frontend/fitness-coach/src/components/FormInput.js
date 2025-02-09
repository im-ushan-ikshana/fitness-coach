import React, { useState, useEffect } from "react";
import Lottie from "react-lottie";
import loadingAnimation from "../assets/loading.json"; 
import "./FormInput.css"; 

function FormInput({ formData, onChange, onSubmit, loading }) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [blink, setBlink] = useState(true);

  // Handle Change for Gender, Workout Preference, and Experience Level
  const handleSelectChange = (e) => {
    const { name, value } = e.target;

    // Convert specific fields before submission
    let processedValue = value;

    if (name === "gender") {
      processedValue = value === "Male" ? 1 : 0;
    } else if (name === "workout_preference" || name === "experience_level") {
      processedValue = value.toLowerCase(); // Convert dropdown values to lowercase
    }

    // Correctly update state for dropdown selections
    onChange({ target: { name, value: processedValue } });
  };

  // Lottie animation settings
  const defaultOptions = {
    loop: true,
    autoplay: true,
    animationData: loadingAnimation,
    rendererSettings: {
      preserveAspectRatio: "xMidYMid slice"
    }
  };

  // Handle Form Submission with Modal Activation
  const handleSubmit = (e) => {
    e.preventDefault();
    setIsSubmitting(true); // Show modal
    onSubmit(e); // Call the actual submit function
  };

  // Blink effect for the modal text
  useEffect(() => {
    const interval = setInterval(() => {
      setBlink((prev) => !prev);
    }, 600); // Blinking effect every 600ms

    return () => clearInterval(interval);
  }, []);

  return (
    <>
      <form className="form-container" onSubmit={handleSubmit}>
        <label className="form-label">
          Weight (kg):
          <input
            type="number"
            name="weight"
            value={formData.weight}
            onChange={onChange}
            min="30"
            max="300"
            required
            className="form-input"
          />
        </label>

        <label className="form-label">
          Height (cm):
          <input
            type="number"
            name="height"
            value={formData.height}
            onChange={onChange}
            min="100"
            max="250"
            required
            className="form-input"
          />
        </label>

        <label className="form-label">
          Gender:
          <select
            name="gender"
            value={formData.gender === 1 ? "Male" : "Female"}
            onChange={handleSelectChange}
            className="form-select"
          >
            <option value="Male">Male</option>
            <option value="Female">Female</option>
          </select>
        </label>

        <label className="form-label">
          Age:
          <input
            type="number"
            name="age"
            value={formData.age}
            onChange={onChange}
            min="12"
            max="100"
            required
            className="form-input"
          />
        </label>

        <label className="form-label">
          Hypertension:
          <select
            name="hypertension"
            value={formData.hypertension}
            onChange={onChange}
            className="form-select"
          >
            <option value="No">No</option>
            <option value="Yes">Yes</option>
          </select>
        </label>

        <label className="form-label">
          Diabetes:
          <select
            name="diabetes"
            value={formData.diabetes}
            onChange={onChange}
            className="form-select"
          >
            <option value="No">No</option>
            <option value="Yes">Yes</option>
          </select>
        </label>

        <label className="form-label">
          Fitness Goal:
          <input
            type="text"
            name="fitness_goal"
            placeholder="e.g. Muscle Gain"
            value={formData.fitness_goal}
            onChange={onChange}
            required
            className="form-input"
          />
        </label>

        <label className="form-label">
          Workout Preference:
          <select
            name="workout_preference"
            value={formData.workout_preference}
            onChange={handleSelectChange}
            className="form-select"
          >
            <option value="strength training">Strength Training</option>
            <option value="cardio">Cardio</option>
            <option value="mix">Mix</option>
          </select>
        </label>

        <label className="form-label">
          Workout Location:
          <select
            name="workout_location"
            value={formData.workout_location}
            onChange={onChange}
            className="form-select"
          >
            <option value="Gym">Gym</option>
            <option value="Home">Home</option>
          </select>
        </label>

        <label className="form-label">
          Duration:
          <input
            type="text"
            name="duration"
            placeholder="e.g. 1 month"
            value={formData.duration}
            onChange={onChange}
            required
            className="form-input"
          />
        </label>

        <label className="form-label">
          Experience Level:
          <select
            name="experience_level"
            value={formData.experience_level}
            onChange={handleSelectChange}
            className="form-select"
          >
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="expert">Expert</option>
          </select>
        </label>

        <button type="submit" className="form-button" disabled={loading}>
          Generate Workout
        </button>
      </form>

      {/* Submission Modal with Lottie Animation */}
      {isSubmitting && (
        <div className="modal-overlay">
          <div className="modal-content">
            <Lottie options={defaultOptions} height={120} width={120} />
            <p className={`modal-text ${blink ? "blink" : ""}`}>Generating Your Plan...</p>
          </div>
        </div>
      )}
    </>
  );
}

export default FormInput;
