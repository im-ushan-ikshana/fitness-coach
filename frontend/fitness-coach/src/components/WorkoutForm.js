import React, { useState } from "react";
import axios from "axios";

const WorkoutForm = () => {
  const [formData, setFormData] = useState({
    weight: "",
    height: "",
    bmi: "",
    gender: "1", // 1 = Male, 0 = Female
    age: "",
    hypertension: "No",
    diabetes: "No",
    fitness_goal: "Muscle Gain",
    workout_preference: "Strength Training",
    duration: "2 weeks",
  });

  const [workoutPlan, setWorkoutPlan] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:8000/generate-workout", formData);
      setWorkoutPlan(response.data.workout_plan);
    } catch (error) {
      console.error("Error generating workout plan", error);
    }
  };

  return (
    <div>
      <h2>Generate Your Custom Workout Plan</h2>
      <form onSubmit={handleSubmit}>
        <input type="number" name="weight" placeholder="Weight (kg)" onChange={handleChange} required />
        <input type="number" name="height" placeholder="Height (cm)" onChange={handleChange} required />
        <input type="number" name="bmi" placeholder="BMI" onChange={handleChange} required />
        <input type="number" name="age" placeholder="Age" onChange={handleChange} required />
        <select name="fitness_goal" onChange={handleChange}>
          <option>Muscle Gain</option>
          <option>Weight Loss</option>
          <option>Weight Gain</option>
        </select>
        <select name="workout_preference" onChange={handleChange}>
          <option>Cardio</option>
          <option>Strength Training</option>
          <option>Mixed</option>
        </select>
        <select name="duration" onChange={handleChange}>
          <option>1 week</option>
          <option>2 weeks</option>
          <option>1 month</option>
        </select>
        <button type="submit">Generate Plan</button>
      </form>

      {workoutPlan && (
        <div>
          <h3>Your Workout Plan:</h3>
          <p>{workoutPlan}</p>
        </div>
      )}
    </div>
  );
};

export default WorkoutForm;
