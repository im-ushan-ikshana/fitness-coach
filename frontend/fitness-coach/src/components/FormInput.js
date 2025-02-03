import React from "react";
import "./FormInput.css"; // ✅ Import the CSS file

function FormInput({ formData, onChange, onSubmit, loading }) {
  return (
    <form className="form-container" onSubmit={onSubmit}>
      <label className="form-label">
        Weight (kg):
        <input
          type="number"
          name="weight"
          value={formData.weight}
          onChange={onChange}
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
          required
          className="form-input"
        />
      </label>

      <label className="form-label">
        Gender (0 = Female, 1 = Male):
        <input
          type="number"
          name="gender"
          value={formData.gender}
          onChange={onChange}
          required
          className="form-input"
        />
      </label>

      <label className="form-label">
        Age:
        <input
          type="number"
          name="age"
          value={formData.age}
          onChange={onChange}
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
        <input
          type="text"
          name="workout_preference"
          placeholder="e.g. Strength Training"
          value={formData.workout_preference}
          onChange={onChange}
          required
          className="form-input"
        />
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
        <input
          type="text"
          name="experience_level"
          placeholder="e.g. Intermediate"
          value={formData.experience_level}
          onChange={onChange}
          required
          className="form-input"
        />
      </label>

      <button type="submit" className="form-button" disabled={loading}>
        {loading ? "Generating..." : "Generate Workout"}
      </button>
    </form>
  );
}

export default FormInput;
